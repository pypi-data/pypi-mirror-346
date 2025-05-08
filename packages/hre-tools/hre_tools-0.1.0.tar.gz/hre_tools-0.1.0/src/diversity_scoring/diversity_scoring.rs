
use pyo3::prelude::*;
use numpy::{PyArray1, PyArray2, PyReadonlyArray1, PyReadonlyArray2};
use ndarray::{Array1, Array2,  ArrayView2, ArrayView1, Zip};
use numpy::ToPyArray;
use rayon::prelude::*;

pub fn l2_norm(vec: &Array1<f64>) -> f64 { 
    vec.mapv(|x| x.powi(2)).sum().sqrt()
 
}


/// Calculate the cosine similarity between two vectors
pub fn cosine_similarity(vec_a: &Array1<f64>, vec_b: &Array1<f64>) -> f64 {
    let dot_product = vec_a.dot(vec_b);
    let norm_a = l2_norm(vec_a);
    let norm_b = l2_norm(vec_b);

    dot_product / (norm_a * norm_b)
}


/// Parallel cosine similarity matrix calculation
fn cosine_similarity_matrix(embeddings: ArrayView2<f64>) -> Array2<f64> {
    let n_docs = embeddings.shape()[0];
    let mut similarity_matrix = Array2::<f64>::zeros((n_docs, n_docs));

    Zip::indexed(similarity_matrix.rows_mut())
        .par_for_each(|i, mut row| {
            let vec_a = embeddings.row(i);
            for j in 0..n_docs {
                if i != j {
                    let vec_b = embeddings.row(j);
                    row[j] = vec_a.dot(&vec_b) / 
                            (vec_a.dot(&vec_a).sqrt() * vec_b.dot(&vec_b).sqrt());
                }
            }
        });

    similarity_matrix
}

#[pyfunction]
pub fn calculate_diversity_scores(
    py: Python<'_>,
    embeddings: &PyArray2<f64>,
) -> PyResult<Py<PyArray1<f64>>> {
   
    // Fix the temporary value issue
    let binding = embeddings.readonly();
    let embeddings = binding.as_array();
    
    let similarity_matrix = cosine_similarity_matrix(embeddings);
    
    let diversity_scores = similarity_matrix
        .axis_iter(ndarray::Axis(0))
        .map(|row| 1.0 - row.mean().unwrap_or(0.0))
        .collect::<Array1<f64>>();

    Ok(diversity_scores.to_pyarray(py).to_owned())
}



/// Fast cosine similarity for dense vectors
pub fn dense_cosine(a: ArrayView1<f64>, b: ArrayView1<f64>) -> f64 {
    let dot = a.dot(&b);
    let norm_a = a.dot(&a).sqrt();
    let norm_b = b.dot(&b).sqrt();
    
    // Handle zero norms
    if norm_a <= f64::EPSILON || norm_b <= f64::EPSILON {
        0.0
    } else {
        dot / (norm_a * norm_b)
    }
}

#[pyfunction]
pub fn dense_cosine_matrix(
    py: Python<'_>,
    query: PyReadonlyArray1<f64>,  // Accept NumPy arrays directly
    docs: PyReadonlyArray2<f64>,
) -> PyResult<Py<PyArray1<f64>>> {  // Return PyO3-compatible type
    let query_view = query.as_array();
    let docs_view = docs.as_array();
    
    let scores: Array1<f64> = docs_view
        .outer_iter()
        .map(|doc| dense_cosine(query_view, doc))
        .collect();
    
    Ok(scores.to_pyarray(py).to_owned())
}

