"""
Copyright (C) 2022  GlaxoSmithKline plc - Mathieu Chevalley;

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from typing import Dict, List, Set, Tuple

import numpy as np
from causalscbench.models.training_regimes import TrainingRegime


class Evaluator(object):
    def __init__(self, ground_truth_network: Set[Tuple[str]]) -> None:
        """
        Evaluation module to biologically evaluate a network using ground-truth biological data.

        Args:
            ground_truth_network: list of know gene-gene interactions
        """
        self.ground_truth_network = ground_truth_network

    def __call__(
        self,
        expression_matrix: np.array,
        interventions: List[str],
        gene_names: List[str],
        training_regime: TrainingRegime,
        seed: int = 0,
    ) -> List[Tuple]:
        edges = set()
        gene_names = set(gene_names)
        for i, j in self.ground_truth_network:
            if i in gene_names and j in gene_names and i != j:
                edges.add((i, j))
        return list(edges)

    # def evaluate_network(self, network: List[Tuple], directed: bool = False) -> Dict:
    #     true_positives = 0
    #     if not directed:
    #         network_undirected = set()
    #         for i, j in network:
    #             network_undirected.add((i, j))
    #             network_undirected.add((j, i))
    #         network = network_undirected
    #     for edge in network:
    #         if edge in self.ground_truth_network:
    #             true_positives += 1
    #     return {
    #         "true_positives": true_positives if directed else true_positives / 2,
    #     }
        
    def evaluate_network(self, network: List[Tuple], directed: bool = False, gene_names: List[str] = None) -> Dict:
        true_positives, false_positives, false_negatives = 0, 0, 0
        ground_truth_subnetwork = set()
        for i, j in self.ground_truth_network:
            if i in gene_names and j in gene_names:
                ground_truth_subnetwork.add((i, j))
                
        if not directed:
            network_undirected = set()
            for i, j in network:
                network_undirected.add((i, j))
                network_undirected.add((j, i))
            network = network_undirected
        
        for edge in network:
            if edge in ground_truth_subnetwork:
                true_positives += 1
            else:
                false_positives += 1
                
        for edge in ground_truth_subnetwork:
            if edge not in network:
                false_negatives += 1
                
        return {
            "true_positives": true_positives if directed else true_positives / 2,
            "false_positives": false_positives if directed else false_positives / 2,
            "false_negatives": false_negatives if directed else false_negatives / 2,
        }
            
        
