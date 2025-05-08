use std::collections::HashMap;
use std::path::{Path, PathBuf};
use std::fs;
use rayon::prelude::*;
use pyo3::prelude::*;
use anyhow::{Context, Result};
use walkdir::WalkDir;
use once_cell::sync::Lazy;
use regex::Regex;
use poppler::PopplerDocument;
use memmap2::MmapOptions; 

static WHITESPACE_REGEX: Lazy<Regex> = Lazy::new(|| Regex::new(r"\s+").unwrap());

#[pyclass]
#[derive(Clone)]
pub struct PyDocument {
    #[pyo3(get)]
    page_content: String,
    #[pyo3(get)]
    source: String,
    #[pyo3(get)]
    page: usize,
    #[pyo3(get)]
    metadata: HashMap<String, String>,
}

#[pymethods]
impl PyDocument {
    #[new]
    fn new(
        page_content: String,
        source: String,
        page: usize,
        metadata: Option<HashMap<String, String>>
    ) -> Self {
        let mut metadata = metadata.unwrap_or_default();
        metadata.insert("source".to_string(), source.clone());
        metadata.insert("page".to_string(), page.to_string());
        
        Self {
            page_content,
            source,
            page,
            metadata,
        }
    }

    #[getter]
    fn tokens(&self) -> usize {
        self.page_content.split_whitespace().count()
    }
}

#[pyfunction]
pub fn load_documents(data_dir: &str) -> PyResult<Vec<PyDocument>> {
    let paths = find_files(data_dir)
        .map_err(|e| PyErr::new::<pyo3::exceptions::PyIOError, _>(e.to_string()))?;

    let documents = process_files_parallel(&paths)
        .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))?;

    Ok(documents)
}

fn process_files_parallel(paths: &[PathBuf]) -> Result<Vec<PyDocument>> {
    let pdf_docs = paths.iter()
        .filter(|p| p.extension().map_or(false, |ext| ext == "pdf"))
        .flat_map(|path| process_pdf_poppler(path).unwrap_or_default())
        .collect::<Vec<_>>();


    let txt_docs = paths.par_iter()
        .filter(|p| p.extension().map_or(false, |ext| ext == "txt"))
        .flat_map(|path| process_txt_file_mmap(path).unwrap_or_default())
        .collect::<Vec<_>>();

    Ok([pdf_docs, txt_docs].concat())
}

fn process_pdf_poppler(path: &Path) -> Result<Vec<PyDocument>> {
    let source = path.display().to_string();
    let doc = PopplerDocument::new_from_file(path.to_str().unwrap(), "")
        .with_context(|| format!("Failed to open PDF: {}", path.display()))?;

    let mut documents = Vec::new();
    for page_idx in 0..doc.get_n_pages() {
        let page = doc.get_page(page_idx)
            .with_context(|| format!("Page {} not found in {}", page_idx + 1, path.display()))?;

        let content = extract_page_text(&page)?;
        let mut metadata = HashMap::new();
        metadata.insert("source".to_string(), source.clone());
        metadata.insert("page".to_string(), (page_idx + 1).to_string());

        documents.push(PyDocument::new(
            content,
            source.clone(),
            page_idx + 1,
            Some(metadata)
        ));
    }
    Ok(documents)
}

fn process_txt_file_mmap(path: &Path) -> Result<Vec<PyDocument>> {

    let file = fs::File::open(path)
        .with_context(|| format!("Failed to open TXT file: {}", path.display()))?;
    let mmap = unsafe { MmapOptions::new().map(&file)? };

    
    let content = String::from_utf8_lossy(&mmap);

    let source = path.display().to_string();
    let mut metadata = HashMap::new();
    metadata.insert("source".to_string(), source.clone());

    
    let documents = content.split("\n\n")
        .enumerate()
        .map(|(i, chunk)| {
            PyDocument::new(
                chunk.trim().to_string(),
                source.clone(),
                i + 1,
                Some(metadata.clone())
            )
        })
        .collect();

    Ok(documents)
}

fn extract_page_text(page: &poppler::PopplerPage) -> Result<String> {
    let text = page.get_text().unwrap_or_default();
    Ok(WHITESPACE_REGEX.replace_all(&text, " ").into_owned())
}

fn find_files(data_dir: &str) -> Result<Vec<PathBuf>> {
    WalkDir::new(data_dir)
        .into_iter()
        .filter_map(|e| e.ok())
        .filter(|e| {
            e.path().extension()
                .map_or(false, |ext| ext == "pdf" || ext == "txt")
        })
        .map(|e| Ok(e.path().to_path_buf()))
        .collect()
}
