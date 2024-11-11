# PSGRN: Gene regulatory network inference from single-cell perturbational data through self-training with synthetic gold standards

This repository includes the codes of our winning solution on the [CausalBench Challenge](https://www.gsk.ai/causalbench-challenge/), and for our paper "PerturbGBM: Self-training with Synthetic Gold Standard of Single Cell Data to Infer Gene Regulatory Networks". The method was developed by Kaiwen Deng ([dengkw@umich.edu](mailto:dengkw@umich.edu)) and Yuanfang Guan ([gyuanfan@umich.edu](mailto:gyuanfan@umich.edu)). Please contact us if you have any questions or suggestions.

[CausalBench](https://arxiv.org/abs/2210.17283) is a comprehensive benchmark suite for evaluating network inference methods on perturbational single-cell gene expression data. 
CausalBench introduces several biologically meaningful performance metrics and operates on two large, curated and openly available benchmark data sets for evaluating methods on the inference of gene regulatory networks from single-cell data generated under perturbations.

## Install

* Use conda:
    ```bash
    conda env create -f environment.yml
    ```

* Use pip:
    ```bash
    pip install causalbench=1.1.2
    pip install lightgbm
    pip uninstall causalbench  # we only need its dependencies 
    ```

## Usage

### Setup

- Create a data directory. This will hold any preprocessed and downloaded datasets for faster future invocation.
  - `$ mkdir /path/to/data/`
  - _Replace the above with your desired cache directory location._
- Create an output directory. This will hold all program outputs and results.
  - `$ mkdir /path/to/output/`
  - _Replace the above with your desired output directory location._


### Run the full benchmark suite to replicate the paper results

* **PerturbGBM**

    ```bash
    python causalscbench/apps/main_app.py \
            --dataset_name "weissmann_rpe1" \  
            --output_directory "/path/to/output/" \
            --data_directory "/path/to/data/" \
            --training_regime "partial_interventional" \
            --partial_intervention_seed 0 \
            --fraction_partial_intervention 1.0 \
            --model_name "custom" \
            --inference_function_file_path "./src/main.py" \
            --subset_data 1.0 \
            --model_seed 0 \
            --omission_estimation_size 2000 \
            --do_filter
    ```
    * `--dataset_name` could also be "weissmann_k562" to run on the K562 dataset

    * We use different `--fraction_partial_intervention` with 0, 0.05, 0.15, 0.25, 0.5, 0.75, 1.0 to study the model's scalability under different fractions of interventional data. 0 means no interventional data, *i.e*, purely observational data

    * We use different `--partial_intervention_seed` to subsample different interventional data when the fraction is not 0 or 1

    * We use different `--subset_data` to study the model's scalability to different sample sizes

    * `--do_filter` controls whether to select only the strong perturbations

    * User can modify the `N` in `./src/main.py` to control how many gene regulatory pairs should be inferred. PerturbGBM 1K is `N = 1000`, and PerturbGBM 5K is `N = 5000`

* **Other GRN or causal inference methods**

    To run the benchmark suit for the other methods, users can simply type the model name after `--model_name` to replace "custom" and delete the parameter `--inference_function_file_path`

    For example:
    ```bash
    python causalscbench/apps/main_app.py \
            --dataset_name "weissmann_rpe1" \  
            --output_directory "/path/to/output/" \
            --data_directory "/path/to/data/" \
            --training_regime "partial_interventional" \
            --partial_intervention_seed 0 \
            --fraction_partial_intervention 1.0 \
            --model_name "grnboost" \
            --subset_data 1.0 \
            --model_seed 0 \
            --omission_estimation_size 2000 \
            --do_filter
    ```
    Available method names can be found in `causalscbench/apps/main_app.py`

### Benchmark with BEELINE data and evaluation pipeline

We have two approaches to run PerturbGBM within the BEELINE evaluation framework:

1. **Integrating PerturbGBM directly into BEELINE**:  
   You can add our PerturbGBM method to the BEELINE pipeline by following the developer guide available [here](https://murali-group.github.io/Beeline/BEELINE.html#developer-guide). This involves modifying the existing BEELINE codebase to include our method for gene regulatory network (GRN) inference.

2. **Using BEELINE-provided data in the PerturbGBM pipeline**:  
   Alternatively, you can use the data provided by BEELINE within our PerturbGBM pipeline. After generating GRN predictions, incorporate the results into the BEELINE pipeline to compute the evaluation metrics.

   Here is an example of using the data from BEELINE to make inferences
   ```bash
   python causalscbench/apps/beeline_app.py \
            --beeline_dataset_path "example/GSD/ExpressionData.csv" \  
            --output_directory "/path/to/output/" \
            --model_name "custom" \
            --inference_function_file_path "./src/main.py" \
            --model_seed 0
   ```

## Reference
[https://github.com/causalbench/causalbench-starter](https://github.com/causalbench/causalbench-starter)

[https://github.com/Murali-group/Beeline](https://github.com/Murali-group/Beeline)

Codes in `causalscbench` folder are from [https://github.com/causalbench/causalbench](https://github.com/causalbench/causalbench). We modified the `biological_evaluation.py` so it can now provide data for calculation precisions and recalls. We also added a `beeline_app.py` to run on the external datasets based on the `main_app.py`
