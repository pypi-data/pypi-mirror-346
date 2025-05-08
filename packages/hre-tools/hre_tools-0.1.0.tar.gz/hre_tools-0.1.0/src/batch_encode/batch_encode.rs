use tract_onnx::prelude::*;
use tokenizers::Tokenizer;
use ndarray::Array2;
use pyo3::prelude::*;
use numpy::{PyArray2, IntoPyArray};
use rayon::iter::{IntoParallelRefIterator, ParallelIterator};
use pyo3::exceptions::PyRuntimeError;
use crate::bm25::BM25Index;

#[pyfunction]
pub fn batch_encode(
    py: Python<'_>,
    texts: Vec<String>,
    model_path: String,
    tokenizer_path: String,
    batch_size: usize,
) -> PyResult<Py<PyArray2<f32>>> {

    let result = py.allow_threads(move || {

        let tokenizer = Tokenizer::from_pretrained(&tokenizer_path, None)
            .map_err(|e| format!("Failed to load tokenizer: {}", e))?;

        let model = tract_onnx::onnx()
            .model_for_path(&model_path)
            .map_err(|e| format!("Failed to load model: {}", e))?
            .into_optimized()
            .map_err(|e| format!("Failed to optimize model: {}", e))?
            .into_runnable()
            .map_err(|e| format!("Failed to make model executable: {}", e))?;

        let mut all_embeddings = Vec::new();

        for chunk in texts.chunks(batch_size) {
            let encodings = tokenizer.encode_batch(chunk.to_vec(), true)
                .map_err(|e| format!("Tokenization failed: {}", e))?;

            let batch_embeddings: Vec<Vec<f32>> = encodings
                .par_iter()
                .map(|encoding| {
                    let ids: Vec<i64> = encoding.get_ids().iter().map(|&id| id as i64).collect();
                    let mask: Vec<i64> = vec![1; ids.len()];
                    let types: Vec<i64> = vec![0; ids.len()];

                    let inputs = tvec!(
                        Tensor::from_shape(&[1, ids.len()], &ids)
                            .map_err(|e| format!("Shape error: {}", e))?,
                        Tensor::from_shape(&[1, mask.len()], &mask)
                            .map_err(|e| format!("Shape error: {}", e))?,
                        Tensor::from_shape(&[1, types.len()], &types)
                            .map_err(|e| format!("Shape error: {}", e))?
                    );

                    let outputs = model.run(inputs)
                        .map_err(|e| format!("Model execution failed: {}", e))?;

                    let embedding = outputs[0]
                        .to_array_view::<f32>()
                        .map_err(|e| format!("Array conversion error: {}", e))?
                        .to_owned()
                        .into_raw_vec();

                    let target_dim = 384;
                    let embedding_len = embedding.len();

                    if embedding_len < target_dim {
                        let mut padded_embedding = embedding.clone();
                        padded_embedding.resize(target_dim, 0.0); // Pad with zeros
                        Ok(padded_embedding)
                    }
                    // If the embedding length is greater than 384, truncate it
                    else if embedding_len > target_dim {
                        Ok(embedding[0..target_dim].to_vec())
                    }
                    // If the embedding length is already 384, return as is
                    else {
                        Ok(embedding)
                    }
                })
                .collect::<Result<Vec<Vec<f32>>, String>>()?;

            all_embeddings.extend(batch_embeddings);
        }

        let embedding_dim = all_embeddings.first().map(|v: &Vec<f32>| v.len()).unwrap_or(0);
        Array2::from_shape_vec(
            (all_embeddings.len(), embedding_dim),
            all_embeddings.into_iter().flatten().collect()
        )
        .map_err(|e| format!("Failed to create output array: {}", e))
    });

    match result {
        Ok(array) => Ok(array.into_pyarray(py).to_owned()),
        Err(e) => Err(PyRuntimeError::new_err::<String>(e)),
    }
}
