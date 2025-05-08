use pyo3::prelude::*;
use numpy::{PyArray1};
use ndarray::{Array1};
use numpy::ToPyArray;
#[pyfunction]
pub fn normalize_(py: Python<'_>, scores: &PyArray1<f64>) -> PyResult<Py<PyArray1<f64>>> {
    // Convert PyArray to ndarray
    let scores_view = unsafe { scores.as_slice()? };
    
    // Convert slice to ndarray
    let scores_array = Array1::from(scores_view.to_vec());

    // Compute peak-to-peak (max - min)
    let ptp = scores_array.iter().copied().max_by(|a, b| a.partial_cmp(b).unwrap())
        .unwrap_or(0.0) - scores_array.iter().copied().min_by(|a, b| a.partial_cmp(b).unwrap())
        .unwrap_or(0.0);

    // Normalize the array
    let normalized = if ptp > 0.0 {
        let min_val = scores_array.iter().copied().min_by(|a, b| a.partial_cmp(b).unwrap()).unwrap_or(0.0);
        scores_array.mapv(|x| (x - min_val) / ptp) 
    } else {
        Array1::zeros(scores_array.raw_dim())
    };

    let py_array = normalized.to_pyarray(py);

    Ok(py_array.to_owned())
}