set -e

# Build environment
docker-compose -f pipeline.docker-compose.yml up -d --build

# Force dvc initialization
docker exec runner sh -c "dvc init --force"

docker exec runner sh -c "dvc remote add dvc_storage .dvc_storage/ -d"

# Create prepare_data DVC stage
docker exec runner sh -c "dvc run -n prepare_data \
                          -p pipeline/src/params.py:Params.SEED \
                          -p pipeline/src/params.py:Params.RELEVANT_FEATS_NAMES \
                          -p pipeline/src/params.py:Params.RELEVANT_FEATS_IDX \
                          -p pipeline/src/params.py:Params.TEST_SIZE \
                          -p pipeline/src/params.py:Params.VALIDATION_SET_SIZE \
                          -d pipeline/data/completion_rate.csv \
                          -d pipeline/src/prepare_data.py \
                          -o pipeline/data/train_features.csv \
                          -o pipeline/data/train_labels.csv \
                          -o pipeline/data/test_features.csv \
                          -o pipeline/data/test_labels.csv \
                          -o pipeline/data/validation.csv \
                          --no-exec --force --external \
                          python pipeline/src/prepare_data.py"

# Create train DVC stage
docker exec runner sh -c "dvc run -n search_n_train \
                          -p pipeline/src/params.py:Params.SEED \
                          -p pipeline/src/params.py:Params.PARAMS_GRID \
                          -p pipeline/src/params.py:Params.CV \
                          -p pipeline/src/params.py:Params.SCALER_NAME \
                          -p pipeline/src/params.py:Params.SCALER_ORIGIN \
                          -p pipeline/src/params.py:Params.METRIC_NAME \
                          -p pipeline/src/params.py:Params.METRIC_ORIGIN \
                          -p pipeline/src/params.py:Params.ALGO_NAME \
                          -p pipeline/src/params.py:Params.ALGO_ORIGIN \
                          -d pipeline/src/search_n_train.py \
                          -d pipeline/data/train_features.csv \
                          -d pipeline/data/train_labels.csv \
                          -o pipeline/model/model.p \
                          -o pipeline/model/train_params.json \
                          -m pipeline/model/metrics.json \
                          --no-exec --force --external \
                          python pipeline/src/search_n_train.py"

# Create evaluate DVC stage
docker exec runner sh -c "dvc run -n evaluate \
                          -p pipeline/src/params.py:Params.METRIC_NAME \
                          -p pipeline/src/params.py:Params.METRIC_ORIGIN \
                          -d pipeline/src/evaluate.py \
                          -d pipeline/data/test_features.csv \
                          -d pipeline/data/test_labels.csv \
                          -d pipeline/model/model.p \
                          -d pipeline/model/metrics.json \
                          -o pipeline/model/test_preds.csv \
                          --no-exec --force --external \
                          python pipeline/src/evaluate.py"

# Create validate DVC stage
docker exec runner sh -c "dvc run -n validate \
                          -p pipeline/src/params.py:Params.METRIC_NAME \
                          -d pipeline/src/validate.py \
                          -d pipeline/data/validation.csv \
                          -d pipeline/model/model.p \
                          -d pipeline/model/metrics.json \
                          --no-exec --force --external \
                          python pipeline/src/validate.py"

# Save cached files
docker exec runner sh -c "dvc push"

echo "PIPELINE HAS BEEN INITIALIZED. PLEASE CONSIDER COMMIT CHANGES TO ORIGIN REPOSITORY :)"
