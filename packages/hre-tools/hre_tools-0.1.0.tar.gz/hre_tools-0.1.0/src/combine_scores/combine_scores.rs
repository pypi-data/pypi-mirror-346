use pyo3::prelude::*;
use numpy::{PyArray1};
use ndarray::{Array1};

#[pyfunction]
pub fn combine_scores(
    py: Python,
    scores: Vec<f64>, 
    text_lengths: Vec<f64>, 
    diversity_scores: Vec<f64>, 
    score_weight: f64, 
    length_weight: f64, 
    diversity_weight: f64
) -> PyResult<Py<PyArray1<f64>>> {
    
    let max_score = scores.iter().fold(0.0, |a, &b| f64::max(a, b));
    let max_length = text_lengths.iter().fold(0.0, |a, &b| f64::max(a, b));
    let max_diversity = diversity_scores.iter().fold(0.0, |a, &b| f64::max(a, b));
    

    let normalized_scores: Vec<f64> = scores.iter()
        .map(|&score| if max_score > 0.0 { score / max_score } else { 1.0 })
        .collect();
    
    let normalized_lengths: Vec<f64> = text_lengths.iter()
        .map(|&length| if max_length > 0.0 { length / max_length } else { 1.0 })
        .collect();
    
    let normalized_diversity: Vec<f64> = diversity_scores.iter()
        .map(|&div| if max_diversity > 0.0 { div / max_diversity } else { 1.0 })
        .collect();
    

    let combined_scores: Vec<f64> = normalized_scores.iter()
        .zip(normalized_lengths.iter())
        .zip(normalized_diversity.iter())
        .map(|((score, length), diversity)| {
            score_weight * score + length_weight * length + diversity_weight * diversity
        })
        .collect();
    
 
    let result = Array1::from(combined_scores);
    let py_array = PyArray1::from_owned_array(py, result);
    
    Ok(py_array.into())
}