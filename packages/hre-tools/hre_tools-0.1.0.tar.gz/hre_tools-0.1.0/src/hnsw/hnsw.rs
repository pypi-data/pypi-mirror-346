use ndarray::Array2;
use rayon::prelude::*;
use std::collections::{HashMap, HashSet, BinaryHeap};
use std::sync::{Arc, Mutex};
use std::cmp::Ordering;
use rand::Rng;
use rand_distr::{Distribution, Exp};
use dashmap::DashSet;

pub trait DistanceCalculator {
    fn distance(&self, a: &[f32], b: &[f32]) -> f32;
}

pub struct DistCosine;

impl DistCosine {
    pub fn default() -> Self {
        DistCosine
    }
}

impl DistanceCalculator for DistCosine {
    fn distance(&self, a: &[f32], b: &[f32]) -> f32 {
        let dot_product = a.iter().zip(b.iter()).map(|(x, y)| x * y).sum::<f32>();
        let norm_a = a.iter().map(|x| x * x).sum::<f32>().sqrt();
        let norm_b = b.iter().map(|x| x * x).sum::<f32>().sqrt();
        1.0 - (dot_product / (norm_a * norm_b))
    }
}

#[derive(Copy, Clone, Debug)]
struct DistancedId {
    id: usize,
    distance: f32,
}

impl PartialEq for DistancedId {
    fn eq(&self, other: &Self) -> bool {
        self.distance.eq(&other.distance)
    }
}

impl Eq for DistancedId {}

impl PartialOrd for DistancedId {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        other.distance.partial_cmp(&self.distance)
    }
}

impl Ord for DistancedId {
    fn cmp(&self, other: &Self) -> Ordering {
        self.partial_cmp(other).unwrap_or(Ordering::Equal)
    }
}

#[derive(Clone, Debug)]
pub struct Node {
    id: usize,
    vector: Vec<f32>,
    neighbors: Vec<Vec<usize>>,
    layer: usize,
}

pub struct HNSW {
    normalized_embeddings: Array2<f32>,
    nodes: Arc<Mutex<HashMap<usize, Node>>>,
    entry_point: Option<usize>,
    m: usize,
    m_max0: usize,
    ef_construction: usize,
    max_layer: usize,
    distance_calculator: DistCosine,
    level_probability: f32,
}

impl HNSW {
    pub fn new(m: usize, ef_construction: usize, normalized_embeddings: Array2<f32>) -> Self {
        let m_max0 = 2 * m;

        HNSW {
            normalized_embeddings,
            nodes: Arc::new(Mutex::new(HashMap::new())),
            entry_point: None,
            m,
            m_max0,
            ef_construction,
            max_layer: 0,
            distance_calculator: DistCosine::default(),
            level_probability: 1.0 / std::f32::consts::E,
        }
    }

    fn get_random_layer(&self) -> usize {
        let exp = Exp::new(self.level_probability).unwrap();
        let mut rng = rand::thread_rng();
        exp.sample(&mut rng).floor() as usize
    }

    pub fn insert(&mut self, vector: &[f32], id: usize) {
        let random_layer = self.get_random_layer();
        let mut node = Node {
            id,
            vector: vector.to_vec(),
            neighbors: vec![Vec::new(); random_layer + 1],
            layer: random_layer,
        };

        let mut nodes = self.nodes.lock().unwrap();

        if nodes.is_empty() {
            nodes.insert(id, node);
            self.entry_point = Some(id);
            return;
        }

        let mut entry_point_id = match self.entry_point {
            Some(ep) => ep,
            None => {
                let first_id = *nodes.keys().next().unwrap();
                self.entry_point = Some(first_id);
                first_id
            }
        };

        if random_layer > self.max_layer {
            self.max_layer = random_layer;
            nodes.insert(id, node.clone());
            self.entry_point = Some(id);
            return;
        }

        let mut curr_layer = self.max_layer;
        let mut ep_to_connect = if curr_layer > random_layer {
            let mut ep_candidates = vec![entry_point_id];
            while curr_layer > random_layer {
                ep_candidates = self.search_layer(vector, &ep_candidates, 1, curr_layer);
                curr_layer -= 1;
            }
            ep_candidates
        } else {
            vec![entry_point_id]
        };

        drop(nodes);

        for layer in (0..=random_layer).rev() {
            let neighbors_at_layer = self.search_layer(vector, &ep_to_connect, self.ef_construction, layer);
            node.neighbors[layer] = self.select_neighbors(vector, &neighbors_at_layer, self.m, layer);

            let mut nodes = self.nodes.lock().unwrap();

            if layer == 0 {
                nodes.insert(id, node.clone());
            }

            for &neighbor_id in &node.neighbors[layer] {
                if let Some(neighbor_node) = nodes.get_mut(&neighbor_id) {
                    while neighbor_node.neighbors.len() <= layer {
                        neighbor_node.neighbors.push(Vec::new());
                    }

                    let m_max = if layer == 0 { self.m_max0 } else { self.m };

                    neighbor_node.neighbors[layer].push(id);

                    if neighbor_node.neighbors[layer].len() > m_max {
                        let neighbor_vector = &neighbor_node.vector;
                        let new_neighbors = self.select_neighbors(
                            neighbor_vector,
                            &neighbor_node.neighbors[layer],
                            m_max,
                            layer,
                        );
                        neighbor_node.neighbors[layer] = new_neighbors;
                    }
                }
            }

            ep_to_connect = neighbors_at_layer;
        }
    }

    fn search_layer(&self, query_vector: &[f32], entry_points: &[usize], ef: usize, layer: usize) -> Vec<usize> {
        let nodes = self.nodes.lock().unwrap();
        let visited = DashSet::new();
        
        let mut candidates: BinaryHeap<DistancedId> = entry_points.par_iter()
            .filter_map(|&ep_id| {
                nodes.get(&ep_id).map(|node| {
                    let distance = self.distance_calculator.distance(query_vector, &node.vector);
                    visited.insert(ep_id);
                    DistancedId { id: ep_id, distance }
                })
            })
            .collect();
        
        let results = Arc::new(Mutex::new(BinaryHeap::new()));
        
      
        while let Some(current) = candidates.pop() {
            results.lock().unwrap().push(current);
            
            if results.lock().unwrap().len() >= ef {
                break;
            }
            
            if let Some(current_node) = nodes.get(&current.id) {
                if current_node.neighbors.len() > layer {
                 
                    let new_candidates: Vec<_> = current_node.neighbors[layer].par_iter()
                        .filter(|&&neighbor_id| visited.insert(neighbor_id))
                        .filter_map(|&neighbor_id| {
                            nodes.get(&neighbor_id).map(|neighbor_node| {
                                let distance = self.distance_calculator.distance(query_vector, &neighbor_node.vector);
                                DistancedId { id: neighbor_id, distance }
                            })
                        })
                        .collect();
                    
    
                    for candidate in new_candidates {
                        candidates.push(candidate);
                    }
                }
            }
        }
        
       
        let mut result_ids = Vec::with_capacity(ef);
        while let Some(result) = results.lock().unwrap().pop() {
            result_ids.push(result.id);
        }
        
        result_ids
    }
    



    fn select_neighbors(&self, query_vector: &[f32], candidates: &[usize], m: usize, _layer: usize) -> Vec<usize> {
        if candidates.len() <= m {
            return candidates.to_vec();
        }

        let nodes = self.nodes.lock().unwrap();
        let mut candidate_with_distances: Vec<DistancedId> = candidates
            .par_iter()
            .filter_map(|&candidate_id| {
                nodes.get(&candidate_id).map(|candidate_node| {
                    let distance = self.distance_calculator.distance(query_vector, &candidate_node.vector);
                    DistancedId { id: candidate_id, distance }
                })
            })
            .collect();

        candidate_with_distances.par_sort_by(|a, b| a.distance.partial_cmp(&b.distance).unwrap());
        candidate_with_distances.iter().take(m).map(|c| c.id).collect()
    }

    
    pub fn build_hnsw_index(embeddings: &Array2<f32>, m: usize, ef_construction: usize) -> HNSW {
        let num_points = embeddings.shape()[0];
        let mut hnsw = HNSW::new(m, ef_construction, embeddings.clone());
        let embeddings_clone = embeddings.clone();

        (0..num_points).for_each(|id| {
            let binding = embeddings_clone.row(id); 
            let vector = binding.as_slice().unwrap();  
            hnsw.insert(vector, id);
           
        });

        hnsw
    }

    pub fn search(&self, query_vector: &[f32], k: usize) -> Vec<(usize, f32)> {
        if self.entry_point.is_none() {
            return Vec::new();
        }

        let entry_point_id = self.entry_point.unwrap();
        let mut curr_layer = self.max_layer;
        let mut ep = vec![entry_point_id];

        while curr_layer > 0 {
            ep = self.search_layer(query_vector, &ep, 1, curr_layer);
            curr_layer -= 1;
        }

        let neighbors = self.search_layer(query_vector, &ep, k.max(self.ef_construction), 0);

        let nodes = self.nodes.lock().unwrap();
        let mut results = neighbors
            .iter()
            .filter_map(|&neighbor_id| {
                nodes.get(&neighbor_id).map(|node| {
                    let distance = self.distance_calculator.distance(query_vector, &node.vector);
                    (neighbor_id, distance)
                })
            })
            .collect::<Vec<_>>();

        results.sort_by(|a, b| a.1.partial_cmp(&b.1).unwrap());
        results.truncate(k);
        results
    }
}
