use pyo3::prelude::*;
use regex::Regex;
use lazy_static::lazy_static;
use std::collections::{HashMap, HashSet};
use std::arch::x86_64::*;
use rayon::prelude::*;

lazy_static! {
    static ref STOPWORDS: HashSet<&'static str> = [
        "a", "an", "the", "and", "or", "but", "if", "in", "on", "at"
    ].iter().cloned().collect();
    static ref TOKEN_RE: Regex = Regex::new(r"\b[\w-]+\b").unwrap();
    static ref STEM_MAP: HashMap<&'static str, &'static str> = [
        ("running", "run"), ("flies", "fly"), ("better", "good")
    ].iter().cloned().collect();
}


#[pyclass]
#[derive(Clone)]
pub struct BM25Index {
    avg_doc_len: f32,
    doc_freqs: HashMap<String, usize>,
    term_freqs: Vec<HashMap<String, usize>>,
    docs: Vec<String>,
    k1: f32,
    b: f32,
    query_adjustment_cache: HashMap<String, (f32, f32)>,
}

impl BM25Index {
    // Advanced tokenization with stemming and domain awareness
    fn tokenize(text: &str) -> Vec<String> {
        TOKEN_RE.find_iter(text)
            .filter_map(|m| {
                let token = m.as_str().to_lowercase();
                if STOPWORDS.contains(token.as_str()) {
                    return None;
                }
                
                STEM_MAP.get(token.as_str())
                    .map(|s| s.to_string())
                    .or_else(|| {
                        if token.contains('-') && token.chars().any(|c| c.is_uppercase()) {
                            Some(token.replace('-', ""))
                        } else {
                            Some(token)
                        }
                    })
            })
            .collect()
    }


    #[target_feature(enable = "avx2")]
    unsafe fn compute_score_avx2(
        idf: f32,
        tf: f32,
        doc_len: f32,
        avg_len: f32,
        k1: f32,
        b: f32
    ) -> f32 {
        let tf_k1 = _mm256_set1_ps(tf * (k1 + 1.0));
        let denominator = tf + k1 * (1.0 - b + b * doc_len / avg_len);
        let inv_denominator = _mm256_rcp_ps(_mm256_set1_ps(denominator));
        let result = _mm256_mul_ps(tf_k1, inv_denominator);
        
        let mut result_scalar = [0.0f32; 8];
        _mm256_storeu_ps(result_scalar.as_mut_ptr(), result);
        idf * result_scalar[0]
    }

    // Unified scoring interface with automatic AVX2 detection
    fn compute_score(&self, idf: f32, tf: f32, doc_len: f32, k1: f32, b: f32) -> f32 {
        if std::is_x86_feature_detected!("avx2") {
            unsafe { Self::compute_score_avx2(idf, tf, doc_len, self.avg_doc_len, k1, b) }
        } else {

            idf * (tf * (k1 + 1.0)) / (tf + k1 * (1.0 - b + b * (doc_len / self.avg_doc_len)))
        }
    }
    
    fn adjust_parameters_for_query(&self, query_terms: &[String]) -> (f32, f32) {
        let query_key = query_terms.join(" ");
        self.query_adjustment_cache.get(&query_key)
            .map(|(k1, b)| (*k1, *b))
            .unwrap_or((self.k1, self.b))
    }
}

#[pymethods]
impl BM25Index {
    #[new]
    pub fn new(docs: Vec<String>, k1: Option<f32>, b: Option<f32>) -> Self {
        let k1 = k1.unwrap_or(1.2);
        let b = b.unwrap_or(0.75);
        
        let term_freqs: Vec<HashMap<String, usize>> = docs.par_iter()
            .map(|doc| {
                let tokens = Self::tokenize(doc);
                let mut tf_map = HashMap::new();
                for token in tokens {
                    *tf_map.entry(token).or_insert(0) += 1;
                }
                tf_map
            })
            .collect();
        
        let total_len: usize = term_freqs.iter()
            .map(|tf_map| tf_map.values().sum::<usize>())
            .sum();

        let mut doc_freqs = HashMap::new();
        for tf_map in &term_freqs {
            for term in tf_map.keys() {
                *doc_freqs.entry(term.clone()).or_insert(0) += 1;
            }
        }

        Self {
            avg_doc_len: total_len as f32 / docs.len() as f32,
            doc_freqs,
            term_freqs,
            docs,
            k1,
            b,
            query_adjustment_cache: HashMap::new(),
        }
    }

    
    pub fn retrieve_batch(&self, queries: Vec<String>, top_k: usize) -> Vec<Vec<(f32, String)>> {
        queries.par_iter()
            .map(|query| {
                let query_terms = Self::tokenize(query);
                let (k1, b) = self.adjust_parameters_for_query(&query_terms);
                
                let scores: Vec<(f32, String)> = self.docs.par_iter()
                    .enumerate()
                    .map(|(doc_idx, doc)| {
                        let doc_len = self.term_freqs[doc_idx].values().sum::<usize>() as f32;
                        let mut score = 0.0;
    
                        for term in &query_terms {
                            if let Some(&df) = self.doc_freqs.get(term) {
                                let idf = ((self.docs.len() as f32 - df as f32 + 0.5) / 
                                          (df as f32 + 0.5)).ln();
                                let tf = *self.term_freqs[doc_idx].get(term).unwrap_or(&0) as f32;
                                score += self.compute_score(idf, tf, doc_len, k1, b);
                            }
                        }
                        (score, doc.clone())
                    })
                    .collect();
    
                let mut sorted_scores = scores;
                sorted_scores.sort_by(|a, b| b.0.partial_cmp(&a.0).unwrap());
                sorted_scores.truncate(top_k);
    
                sorted_scores
            })
            .collect()
    }


    pub fn retrieve(&self, query: String, top_k: usize) -> Vec<(f32, String)> {
        let query_terms = Self::tokenize(&query);
        let (k1, b) = self.adjust_parameters_for_query(&query_terms);
        
        let scores: Vec<(f32, String)> = self.docs.par_iter()
            .enumerate()
            .map(|(doc_idx, doc)| {
                let doc_len = self.term_freqs[doc_idx].values().sum::<usize>() as f32;
                let mut score = 0.0;

                for term in &query_terms {
                    if let Some(&df) = self.doc_freqs.get(term) {
                        let idf = ((self.docs.len() as f32 - df as f32 + 0.5) / 
                                  (df as f32 + 0.5)).ln();
                        let tf = *self.term_freqs[doc_idx].get(term).unwrap_or(&0) as f32;
                        score += self.compute_score(idf, tf, doc_len, k1, b);
                    }
                }
                (score, doc.clone())
            })
            .collect();

        let mut sorted_scores = scores;
        
        sorted_scores.sort_by(|a, b| b.0.partial_cmp(&a.0).unwrap());
        sorted_scores.truncate(top_k);

        sorted_scores
    }

    #[pyo3(text_signature = "($self, feedback)")]
    pub fn update_parameters(&mut self, feedback: Vec<(String, bool)>) {
        for (query, is_relevant) in feedback {
            let terms = Self::tokenize(&query);
            let entry = self.query_adjustment_cache.entry(terms.join(" "))
                .or_insert((self.k1, self.b));
            
            if is_relevant {
                entry.0 *= 0.9;  
                entry.1 *= 1.1;  
            } else {
                entry.0 *= 1.1;
                entry.1 *= 0.9;
            }
        }
    }
}