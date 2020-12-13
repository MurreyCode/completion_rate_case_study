node ('ecs') {
    prepare_environment()
    get_data()
    run_pipeline()
    remove_environment()
}

private prepare_environment() {
    sh 'docker-compose -f pipeline.docker-compose.yml up -d --build'
}

private get_data() {
    sh 'docker exec runner sh -c "dvc pull"'
}

private run_pipeline() {

    stage('PrepareData') {
        sh 'docker exec runner sh -c "dvc repro --single-item prepare_data && dvc push"'
    }
    stage('Train') {
        sh 'docker exec runner sh -c "dvc repro --single-item search_n_train && dvc push"'
    }
    stage('Evaluation') {
        sh 'docker exec runner sh -c "dvc repro --single-item evaluate && dvc push"'
    }
    stage('Validation') {
        sh 'docker exec runner sh -c "dvc repro --single-item validate && dvc push"'
    }
}

private remove_environment() {
    sh 'docker container rm -f runner'
}
