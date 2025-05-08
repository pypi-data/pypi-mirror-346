use pyo3::prelude::*;
use pyo3::types::{PyAny, PyDict};
use polars::prelude::*;
// i want it to take in pandas dataframe 

#[pyclass]
pub struct FractalDB {
    data: String
}

