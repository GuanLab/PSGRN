"""
Copyright (C) 2023  GlaxoSmithKline plc - Mathieu Chevalley;

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

import json
import os
import time
import numpy as np
import pandas as pd
import slingpy as sp
from  slingpy.utils import logging
from causalscbench.apps.utils.run_utils import (
    create_experiment_folder, get_if_valid_custom_function_file)
from causalscbench.data_access.create_dataset import CreateDataset
from causalscbench.data_access.create_evaluation_datasets import \
    CreateEvaluationDatasets
from causalscbench.data_access.utils.splitting import DatasetSplitter
from causalscbench.evaluation import (biological_evaluation,
                                      statistical_evaluation)
from causalscbench.models import training_regimes
from causalscbench.models.arboreto_baselines import GENIE, GRNBoost
from causalscbench.models.causallearn_models import GES, PC
from causalscbench.models.dcdi_models import DCDI, DCDFG
from causalscbench.models.feature_selection import (
    LassoFeatureSelection, RandomForestFeatureSelection)
from causalscbench.models.gies import GIES
from causalscbench.models.notears import NotearsLin, NotearsMLP
from causalscbench.models.random_network import FullyConnected, RandomWithSize
from causalscbench.models.sparsest_permutations import (
    GreedySparsestPermutation,
    InterventionalGreedySparsestPermutation,
)
from causalscbench.models.varsortability import Sortnregress


METHODS = [
    "random100",
    "random1000",
    "random10000",
    "fully-connected",
    "lasso",
    "random_forest",
    "grnboost",
    "genie",
    "ges",
    "gies",
    "pc",
    "mvpc",
    "gsp",
    "igsp",
    "notears-lin",
    "notears-lin-sparse",
    "notears-mlp",
    "notears-mlp-sparse",
    "DCDI-G",
    "DCDI-DSF",
    "DCDFG-LIN",
    "DCDFG-MLP",
    "sortnregress",
]


class MainApp:
    def __init__(
        self,
        output_directory: str,
        beeline_dataset_path: str, ##BEELINE
        model_name: str = METHODS[0],
        inference_function_file_path: str = "",
        model_seed: int = 0,
        exp_id: str = "",
    ):  
        """
        Main full training pipeline.

        Args:
            output_directory (str): Directory for output results
            data_directory (str): Directory to store the datasets
            model_name (str, optional): Which method to run. Defaults to METHODS[0].
            inference_function_file_path (str, optional): Path to file for custom inference function. Default to empty string.
            dataset_name (List[str], optional): Which dataset to use. Defaults to DATASET_NAMES[0].
            model_seed (int, optional): Seed for model reproducibility. Defaults to 0.
            training_regime (training_regimes.TrainingRegime, optional): Choice of training regime. Defaults to training_regimes.Interventional.
            partial_intervention_seed (int, optional): If training_regime is partial intervention, seed for random selection of perturbed genes. Defaults to 0.
            fraction_partial_intervention (float, optional):  If training_regime is partial intervention, fraction of genes which should have interventional data. Defaults to 1.0.
            subset_data (float, optional): Option to subset the whole dataset for easier training. Defaults to 1.0.
            exp_id (str, optional): Unique experiment id (6 digit number). Default to randomly generated.
            max_path_length (int, optional): Maximum length of path to consider for statistical evaluation. Default to -1 (all paths).
            omission_estimation_size (int, optional): Number of negative samples to draw to estimate the false omission rate. If 0, the FOR is not checked. 
        """
        self.output_directory = create_experiment_folder(exp_id, output_directory)
        self.inference_function_file_path = inference_function_file_path
        self.model_name = model_name
        self.model_seed = model_seed
        self.exp_id = exp_id
        self.model = None
        self.beeline_dataset_path = beeline_dataset_path #BEELINE

    def load_model(self):
        models_dict = {
            "random100": RandomWithSize(100),
            "random1000": RandomWithSize(1000),
            "random10000": RandomWithSize(10000),
            "fully-connected": FullyConnected(),
            "lasso": LassoFeatureSelection(),
            "random_forest": RandomForestFeatureSelection(),
            "grnboost": GRNBoost(),
            "genie": GENIE(),
            "ges": GES(),
            "gies": GIES(),
            "pc": PC(missing_value=False),
            "mvpc": PC(missing_value=True),
            "gsp": GreedySparsestPermutation(),
            "igsp": InterventionalGreedySparsestPermutation(),
            "notears-lin": NotearsLin(lambda1=0.0),
            "notears-lin-sparse": NotearsLin(lambda1=0.001),
            "notears-mlp": NotearsMLP(lambda1=0.0),
            "notears-mlp-sparse": NotearsMLP(lambda1=0.001),
            "DCDI-G": DCDI("DCDI-G"),
            "DCDI-DSF": DCDI("DCDI-DSF"),
            "DCDFG-LIN": DCDFG("linear"),
            "DCDFG-MLP": DCDFG("mlplr"),
            "sortnregress": Sortnregress(),
        }
        if self.model_name not in METHODS:
            raise NotImplementedError()
        if self.model_name == "custom":
            self.model = get_if_valid_custom_function_file(
                self.inference_function_file_path
            )()
        else:
            self.model = models_dict[self.model_name]


    def train_and_evaluate(self):
        gsd = pd.read_csv(f"{self.beeline_dataset_path}")
        expression_matrix_train = np.array(gsd.iloc[:,1:], dtype=np.float32).T
        interventions_train = ["non-targeting"] * expression_matrix_train.shape[0]
        gene_names = np.array(gsd.iloc[:,0])

        output_network = self.model(
            expression_matrix_train,
            list(interventions_train),
            gene_names,
            self.training_regime,
            self.model_seed,
        )

        logging.info("Model training finished.")
        end_time = time.time()
        logging.info("Evaluating model.")
        pd.DataFrame(output_network).to_csv(
            os.path.join(self.output_directory, "output_network.csv")
        )
        return None
    
    def run(self):
        logging.info("Loading model.")
        self.load_model()
        self.train_and_evaluate()


def main():
    app = sp.instantiate_from_command_line(MainApp)
    results = app.run()


if __name__ == "__main__":
    main()
