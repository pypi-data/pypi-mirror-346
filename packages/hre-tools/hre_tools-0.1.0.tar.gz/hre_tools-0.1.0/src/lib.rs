use pyo3::prelude::*;
use numpy::{PyArray1, PyArray2};
use ndarray::{Array1, Array2};
pub mod tfidf; 
pub mod diversity_scoring;
pub mod normalize_; 
pub mod hnsw; 
pub mod bm25; 
use diversity_scoring::diversity_scoring::{calculate_diversity_scores, l2_norm, dense_cosine_matrix};  
mod combine_scores; 
pub mod batch_encode; 
pub mod hybrid_retriever;
pub mod fractal_db; 
pub mod load_pdf; 

/*

BM25 tokenization and indexing.
Cosine similarity and other matrix operations (e.g., diversity score calculation).
Parallel processing for batch predictions in rerank_documents.
FAISS indexing and search operations.
Document deduplication.
Embedding processing with ndarray or tch-rs for efficient tensor operations.
TfidfVectorizer functionality (for faster computation).
*/


#[pyfunction]
#[pyo3(signature = (vec1, vec2=None, dense_output=true))]
pub fn cosine_similarity_rust(
    py: Python<'_>,
    vec1: &PyArray2<f64>,
    vec2: Option<&PyArray2<f64>>,
    dense_output: bool,
) -> PyResult<Py<PyArray2<f64>>> {
    // Convert PyArray2 (Python object) to Rust ndarray and ensure proper lifetime
    let vec1_readonly = vec1.readonly();
    let vector1 = vec1_readonly.as_array();

    // Use a variable to extend the lifetime of the readonly array
    let vec2_readonly;
    let vec2_array = match vec2 {
        Some(v) => {
            vec2_readonly = v.readonly();
            Some(vec2_readonly.as_array())
        },
        None => None,
    };

    // Normalize the matrices
    let x_normalized = normalize(&vector1.to_owned());

    let y_normalized = match vec2_array {
        Some(v2) => normalize(&v2.to_owned()),
        None => x_normalized.clone(),
    };

    let similarity = x_normalized.dot(&y_normalized.t());

    // Convert the 2D array to a nested Vec structure
    let similarity_vec: Vec<Vec<f64>> = similarity
        .outer_iter()
        .map(|row| row.to_vec())
        .collect();

    // Use from_vec2 with the correct type and convert to Py<PyArray2<f64>>
    if dense_output {
        let result = PyArray2::from_vec2(py, &similarity_vec)?;
        Ok(result.into_py(py))
    } else {
        // Handle the sparse output case if needed, currently returning dense
        let result = PyArray2::from_vec2(py, &similarity_vec)?;
        Ok(result.into_py(py))
    }
}


pub fn normalize(arr: &Array2<f64>) -> Array2<f64> {
    let mut result = Array2::zeros(arr.dim());
    for (i, row) in arr.outer_iter().enumerate() {
        let norm = l2_norm(&row.to_owned());
        if norm > 0.0 {
            for (j, val) in row.iter().enumerate() {
                result[[i, j]] = val / norm;
            }
        }
    }
    result
}


#[pymodule]
fn hre_tools(py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(normalize_::normalize_::normalize_, m)?)?; 
    m.add_function(wrap_pyfunction!(calculate_diversity_scores, m)?)?; 
    m.add_function(wrap_pyfunction!(combine_scores::combine_scores::combine_scores, m)?)?; 
    m.add_function(wrap_pyfunction!(cosine_similarity_rust, m)?)?; 
    m.add_function(wrap_pyfunction!(dense_cosine_matrix, m)?)?; 
    m.add_function(wrap_pyfunction!(batch_encode::batch_encode::batch_encode, m)?)?;
    m.add_function(wrap_pyfunction!(load_pdf::load_pdf::load_documents, m)?)?;
    
    m.add_class::<tfidf::tfidf::TfidfVectorizer>()?;
    m.add_class::<hybrid_retriever::hybrid_retriever::HybridRetriever>()?;
    m.add_class::<fractal_db::fractal_db::FractalDB>()?;
    m.add_class::<bm25::bm25::BM25Index>()?;    
    Ok(())
}





