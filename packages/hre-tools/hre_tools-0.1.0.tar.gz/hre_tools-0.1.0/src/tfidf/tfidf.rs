use std::collections::{HashMap, HashSet};
use std::sync::atomic::{AtomicUsize, Ordering};
use std::sync::Mutex;
use regex::Regex;
use ndarray::Array2;
use numpy::{PyArray2, IntoPyArray};
use pyo3::prelude::*;
use rayon::prelude::*;
use once_cell::sync::Lazy;

static TOKENIZER: Lazy<Regex> = Lazy::new(|| Regex::new(r"\w+").unwrap());

#[pyclass]
#[derive(Clone)]
pub struct TfidfVectorizer {
    pub vocabulary: HashMap<String, usize>,
    pub idf: HashMap<String, f64>,
    pub avg_doc_len: f64,
}


#[pymethods]
impl TfidfVectorizer {
    #[new]
    pub fn new() -> Self {
        TfidfVectorizer {
            vocabulary: HashMap::new(),
            idf: HashMap::new(),
            avg_doc_len: 0.0,
        }
    }

    pub fn fit(&mut self, raw_documents: Vec<String>) -> PyResult<()> {
        let doc_count = raw_documents.len();
        if doc_count == 0 {
            return Err(pyo3::exceptions::PyValueError::new_err(
                "Cannot fit on empty document collection"
            ));
        }

        let (vocab, total_len) = self.build_vocabulary_and_stats(&raw_documents);
        self.vocabulary = vocab;
        self.avg_doc_len = total_len as f64 / doc_count as f64;
        self.calculate_idf(&raw_documents);
        Ok(())
    }

 
    pub fn transform<'py>(&self, py: Python<'py>, raw_documents: Vec<String>) -> PyResult<&'py PyArray2<f64>> {
        let vocab_size = self.vocabulary.len();
        let doc_count = raw_documents.len();
        let mut tfidf_matrix = Array2::zeros((doc_count, vocab_size));

        let results: Vec<(usize, Vec<(usize, f64)>)> = raw_documents.par_iter().enumerate()
            .map(|(row_idx, doc)| {
                let words = self.tokenize(doc);
                let word_count = words.len() as f64;
                let mut tf: HashMap<&str, f64> = HashMap::new();
                let mut row_results = Vec::new();
    
                for word in &words {
                    *tf.entry(word.as_str()).or_insert(0.0) += 1.0 / word_count;
                }

                for (word, tf_val) in tf {
                    if let Some(&col) = self.vocabulary.get(word) {
                        if let Some(&idf) = self.idf.get(word) {
                            row_results.push((col, tf_val * idf));
                        }
                    }
                }
                
                (row_idx, row_results)
            })
            .collect();
        

        for (row_idx, row_data) in results {
            for (col, value) in row_data {
                tfidf_matrix[[row_idx, col]] = value;
            }
        }
    
        Ok(tfidf_matrix.into_pyarray(py))
    }


    #[pyo3(name = "transform_sparse")]
    pub fn transform_sparse(&self, _py: Python<'_>, raw_documents: Vec<String>) -> PyResult<Vec<(usize, usize, f64)>> {
        let vocab = &self.vocabulary;
        let idf = &self.idf;

        let results: Vec<_> = raw_documents.into_par_iter().enumerate()
            .flat_map(|(row_idx, doc)| {
                let words = self.tokenize(&doc);
                let word_count = words.len() as f64;
                let mut tf: HashMap<&str, f64> = HashMap::new();

                for word in &words {
                    *tf.entry(word.as_str()).or_insert(0.0) += 1.0 / word_count;
                }

                tf.into_iter()
                    .filter_map(|(word, tf_val)| {
                        let col = *vocab.get(word)?;
                        let idf_val = idf.get(word)?;
                        Some((row_idx, col, tf_val * idf_val))
                    })
                    .collect::<Vec<_>>()
            })
            .collect();

        Ok(results)
    }

    pub fn tokenize(&self, document: &str) -> Vec<String> {
        TOKENIZER
            .find_iter(document)
            .map(|mat| mat.as_str().to_lowercase())
            .collect()
    }
}

impl TfidfVectorizer {
    fn build_vocabulary_and_stats(&self, docs: &[String]) -> (HashMap<String, usize>, usize) {
        let vocab = Mutex::new(HashMap::new());
        let total_len = AtomicUsize::new(0);
        let next_index = AtomicUsize::new(0);

        docs.par_iter().for_each(|doc| {
            let words = self.tokenize(doc);
            total_len.fetch_add(words.len(), Ordering::Relaxed);
            
            let mut vocab_lock = vocab.lock().unwrap();
            for word in words {
                vocab_lock.entry(word).or_insert_with(|| {
                    next_index.fetch_add(1, Ordering::Relaxed)
                });
            }
        });

        (vocab.into_inner().unwrap(), total_len.into_inner())
    }

    fn calculate_idf(&mut self, docs: &[String]) {
        let doc_count = docs.len();
        let term_doc_count = Mutex::new(HashMap::new());

        docs.par_iter().for_each(|doc| {
            let words = self.tokenize(doc);
            let unique_words: HashSet<_> = words.into_iter().collect();
            
            let mut counts = term_doc_count.lock().unwrap();
            for word in unique_words {
                *counts.entry(word).or_insert(0) += 1;
            }
        });

        self.idf = term_doc_count.into_inner().unwrap()
            .into_par_iter()
            .map(|(term, count)| (term, (doc_count as f64 / count as f64).ln()))
            .collect();
    }
}

