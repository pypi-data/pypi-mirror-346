use pyo3::{prelude::*, exceptions::PyValueError, types::{PyDict, PyList}};
use ndarray::{Array2, Array1, Axis};
use numpy::PyReadonlyArray2;
use std::collections::HashMap;
use crate::bm25::BM25Index;
use crate::tfidf::TfidfVectorizer;
use rayon::prelude::*;
use hnsw_rs::prelude::*;
use std::path::Path;


// just for rust 
#[pyclass]
pub struct HybridRetriever {
    embeddings: Array2<f32>,
    doc_texts: Vec<String>,
    bm25_index: BM25Index,
    tfidf_vectorizer: TfidfVectorizer,
    tfidf_matrix: Array2<f64>,
    hnsw_index: Option<Hnsw<'static, f32, DistCosine>>, 
    source_filename: String,
    batch_size: usize,
    alpha: f64,  
    cross_encoder: String,
    corpus: Vec<String>,
    bm25_doc_lookup: HashMap<String, usize>,
}



// all of the rust interaction
impl HybridRetriever {


    fn cosine_similarity(a: &Array1<f64>, b: &Array1<f64>) -> f64 {
        let dot = a.dot(b);
        let norm_a = a.dot(a).sqrt();
        let norm_b = b.dot(b).sqrt();
        dot / (norm_a * norm_b).max(1e-8)
    }

    fn normalize_embeddings(embeddings: &Array2<f32>) -> Array2<f32> {
        let mut normalized = Array2::zeros(embeddings.dim());
        for (mut row, emb_row) in normalized.rows_mut().into_iter().zip(embeddings.rows()) {
            let norm = emb_row.dot(&emb_row).sqrt().max(1e-8);
            row.assign(&(emb_row.to_owned() / norm));;
        }
        normalized
    }

    fn build_hnsw_index(embeddings: &Array2<f32>) -> Hnsw<'static, f32, DistCosine> {
        let dim = embeddings.shape()[1];
        let mut hnsw = Hnsw::new(32, embeddings.shape()[0], dim, 200, DistCosine::default());
        
        for (id, vec) in embeddings.rows().into_iter().enumerate() {
            hnsw.insert((&vec.to_vec(), id));
        }
        
        hnsw
    }


    fn compute_tfidf_rust(&self, py: Python<'_>, query: &str) -> PyResult<Vec<f64>> {
        let query_vec = self.tfidf_vectorizer.transform(py, vec![query.to_string()])?
            .to_owned_array();
        let query_vec = query_vec.index_axis(Axis(0), 0).to_owned();
    
        Ok(self.tfidf_matrix
            .axis_iter(Axis(0))
            .map(|doc_vec| Self::cosine_similarity(&query_vec, &doc_vec.to_owned()))
            .collect())
    }
}



// whats seen in the python side
#[pymethods]
impl HybridRetriever {
    #[new]
    #[pyo3(signature = (
        embeddings,
        documents,
        cross_encoder,
        source_filename,
        batch_size = None,
        alpha = None
    ))]
    fn new(
        py: Python<'_>,  
        embeddings: PyReadonlyArray2<f32>,
        documents: &PyAny,
        cross_encoder: String,
        source_filename: String,
        batch_size: Option<usize>,
        alpha: Option<f64>,
    ) -> PyResult<Self> {
        let alpha = alpha.unwrap_or(0.5);
        if !(0.0..=1.0).contains(&alpha) {
            return Err(PyValueError::new_err("Alpha must be between 0.0 and 1.0"));
        }

        let embeddings = embeddings.as_array().to_owned();
        let normalized_embeddings = Self::normalize_embeddings(&embeddings);
        let batch_size = batch_size.unwrap_or(32);

        let doc_texts = if let Ok(str_list) = documents.extract::<Vec<String>>() {
            if str_list.is_empty() {
                return Err(PyValueError::new_err("Documents list cannot be empty"));
            }
            str_list
        } else {
            let py_list: &PyList = documents.downcast()?;
            if py_list.is_empty() {
                return Err(PyValueError::new_err("Documents list cannot be empty"));
            }
            py_list.iter()
                .map(|doc| doc.getattr("page_content")?.extract())
                .collect::<PyResult<_>>()?
        };

        if embeddings.nrows() != doc_texts.len() {
            return Err(PyValueError::new_err(
                "Number of embeddings must match number of documents"
            ));
        }

        let bm25_doc_lookup = doc_texts.iter()
            .enumerate()
            .map(|(idx, text)| (text.clone(), idx))
            .collect();

        let corpus = doc_texts.clone();
        let bm25_index = BM25Index::new(corpus.clone(), None, None); 

        let mut tfidf_vectorizer = TfidfVectorizer::new();
        tfidf_vectorizer.fit(doc_texts.clone())?;
        
        let tfidf_matrix = tfidf_vectorizer.transform(py, doc_texts.clone())?
            .to_owned_array();
        


        let hnsw_index = Some(Self::build_hnsw_index(&normalized_embeddings)); 
        let path = Path::new("./index_storage");
        std::fs::create_dir_all(path).unwrap();

        if let Some(index) = &hnsw_index {
        let basename = index.file_dump(path, &source_filename).unwrap();
        }
        
       
     
        Ok(Self {
            embeddings,
            doc_texts,
            bm25_index,
            tfidf_vectorizer,
            tfidf_matrix,
            hnsw_index,
            batch_size,
            alpha,
            cross_encoder,
            corpus,
            bm25_doc_lookup,
            source_filename
        })
    }

    #[staticmethod]
    fn normalize(scores: Vec<f64>) -> Vec<f64> {
        if scores.is_empty() { return Vec::new(); }

        let (min, max) = scores
            .par_iter()
            .fold(|| (f64::INFINITY, f64::NEG_INFINITY),
                |(min, max), &x| (min.min(x), max.max(x)))
            .reduce(|| (f64::INFINITY, f64::NEG_INFINITY),
                |(a_min, a_max), (b_min, b_max)| (a_min.min(b_min), a_max.max(b_max)));
        
        let ptp = max - min;
        if ptp > 0.0 {
            scores.par_iter().map(|&x| (x - min) / ptp).collect()
        } else {
            vec![0.0; scores.len()]
        }
    }

    fn compute_tfidf(&self, py: Python<'_>, query: String) -> PyResult<Vec<f64>> {
        let query_vec = self.tfidf_vectorizer.transform(py, vec![query])?.to_owned_array();
        let query_vec = query_vec.index_axis(Axis(0), 0).to_owned();

        let scores: Vec<f64> = self
            .tfidf_matrix
            .axis_iter(Axis(0))
            .map(|doc_vec| Self::cosine_similarity(&query_vec, &doc_vec.to_owned()))
            .collect();

        Ok(scores)
    }

    fn compute_bm25_batch(&self, queries: Vec<String>) -> PyResult<Vec<Vec<f64>>> {
       
        let scored_docs_batch = self.bm25_index.retrieve_batch(queries, self.doc_texts.len());
    
        let mut all_bm25_scores = Vec::new();
    
        for scored_docs in scored_docs_batch {
            let mut bm25_scores = vec![0.0; self.doc_texts.len()];
    
            for (score, doc_text) in scored_docs {
                if let Some(&doc_idx) = self.bm25_doc_lookup.get(&doc_text) {
                    bm25_scores[doc_idx] = score as f64;
                }
            }
    
            all_bm25_scores.push(Self::normalize(bm25_scores));
        }
    
        Ok(all_bm25_scores)
    }
    

    fn compute_bm25(&self, query: String) -> PyResult<Vec<f64>> {
        let scored_docs = self.bm25_index.retrieve(query, self.doc_texts.len());
        let mut bm25_scores = vec![0.0; self.doc_texts.len()];

        for (score, doc_text) in scored_docs {
            if let Some(&doc_idx) = self.bm25_doc_lookup.get(&doc_text) {
                bm25_scores[doc_idx] = score as f64;
            }
        }
        
        Ok(Self::normalize(bm25_scores))
    }
    
    fn retrieve(&self, py: Python<'_>, query_text: String, top_k: usize) -> PyResult<(Vec<String>, Vec<f64>)> {
        
        let tfidf_scores = self.compute_tfidf(py, query_text.clone())?;    
        let bm25_scores = self.compute_bm25(query_text)?;

        let combined_scores: Vec<f64> = tfidf_scores.par_iter()
            .zip(bm25_scores.par_iter())
            .map(|(t, b)| (t + b) / 2.0)
            .collect();

        let mut scored_docs: Vec<(usize, f64)> = combined_scores.iter()
            .enumerate()
            .map(|(idx, &score)| (idx, score))
            .collect();

        scored_docs.par_sort_unstable_by(|a, b| b.1.partial_cmp(&a.1).unwrap());

        let top_results: Vec<String> = scored_docs.iter()
            .take(top_k)
            .map(|&(idx, _)| self.doc_texts[idx].clone())
            .collect();

        let top_scores: Vec<f64> = scored_docs.iter()
            .take(top_k)
            .map(|&(_, score)| score)
            .collect();

        Ok((top_results, top_scores))
    }

    fn hybrid_search(
        &self,
        py: Python<'_>,
        query_embedding: PyReadonlyArray2<f32>,
        query_text: String,
        top_k: usize,
    ) -> PyResult<(Vec<String>, Vec<f64>)> {

        let query_array = query_embedding.as_array().to_owned();
        let normalized_query = Self::normalize_embeddings(&query_array);
        let query_slice = normalized_query.index_axis(Axis(0), 0).to_vec();
        
        
        let vector_results = if let Some(index) = &self.hnsw_index {
            index.search(&query_slice, top_k * 2, 100)
                .into_iter()
                .map(|n| (n.d_id, 1.0 - n.distance as f64))
                .collect::<Vec<_>>()
        } else {
            Vec::new()
        };

      
        let tfidf_scores = self.compute_tfidf(py, query_text.clone())?;
        let bm25_scores = self.compute_bm25(query_text)?;

       
        let mut combined = Vec::with_capacity(self.doc_texts.len());
        for i in 0..self.doc_texts.len() {
            let vector_score = vector_results.iter()
                .find(|(id, _)| *id == i)
                .map(|(_, s)| s * self.alpha)
                .unwrap_or(0.0);
                
            let text_score = (tfidf_scores[i] + bm25_scores[i]) / 2.0 * (1.0 - self.alpha);
            
            combined.push((i, vector_score + text_score));
        }

        
        combined.sort_unstable_by(|a, b| b.1.partial_cmp(&a.1).unwrap());
        let results = combined.iter()
            .take(top_k)
            .map(|(i, _)| self.doc_texts[*i].clone())
            .collect();
        let scores = combined.iter()
            .take(top_k)
            .map(|(_, s)| *s)
            .collect();

        Ok((results, scores))
    }

    #[getter]
    fn doc_texts(&self) -> Vec<String> {
        self.doc_texts.clone()
    }

    #[getter]
    fn corpus(&self) -> Vec<String> {
        self.corpus.clone()
    }

    #[getter]
    fn bm25_doc_lookup(&self, py: Python) -> PyResult<Py<PyDict>> {
        let dict = PyDict::new(py);
        for (text, idx) in &self.bm25_doc_lookup {
            dict.set_item(text, idx)?;
        }
        Ok(dict.into())
    }

    #[getter]
    fn dimension(&self) -> usize {
        self.embeddings.shape()[1]
    }
    
 
}

