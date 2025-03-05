#!/bin/bash

python causalscbench/apps/main_app.py \
        --dataset_name "weissmann_rpe1" \
        --output_directory "rpe1_output/" \
        --exp_id "psgrn_fast_rpe1_0.25_1" \
        --data_directory "data/" \
        --training_regime "partial_interventional" \
        --partial_intervention_seed 0 \
        --fraction_partial_intervention 0.25 \
        --model_name "custom" \
        --inference_function_file_path "./src/main_fast.py" \
        --subset_data 1.0 \
        --model_seed 0 \
        --omission_estimation_size 2000 \
        --do_filter

python causalscbench/apps/main_app.py \
        --dataset_name "weissmann_rpe1" \
        --output_directory "rpe1_output" \
        --exp_id "grnboost_rpe1_0.25_1" \
        --data_directory "data/" \
        --training_regime "partial_interventional" \
        --partial_intervention_seed 0 \
        --fraction_partial_intervention 0.25 \
        --model_name "grnboost" \
        --subset_data 1.0 \
        --model_seed 0 \
        --omission_estimation_size 2000 \
        --do_filter