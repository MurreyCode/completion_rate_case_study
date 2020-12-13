set -e
echo ""

# Build environment
docker-compose -f pipeline.docker-compose.yml up -d --build

# Get data
# docker exec runner sh -c "dvc pull"

# Run pipeline stages
docker exec runner sh -c "dvc repro --single-item prepare_data && dvc push"
docker exec runner sh -c "dvc repro --single-item search_n_train && dvc push"
docker exec runner sh -c "dvc repro --single-item evaluate && dvc push"
docker exec runner sh -c "dvc repro --single-item validate && dvc push"

# Remove container
docker container rm -f runner
echo ""
