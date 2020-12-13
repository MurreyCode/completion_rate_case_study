# Completion Rate Case Study

***

### On experimentation pipeline

* To start running the pipeline place `completion_rate.csv` file in `pipeline/data/` folder.
* Run command `sh scripts/run_pipeline.sh` from project root folder in your terminal to:
  * Build and run pipeline docker container
  * Run pipeline stages and track experiment artifacts.
  * Update API model when criteria are met.
  * Remove container when finished.
* All changes in the pipeline datasets, params, dependencies, outputs and metrics related to experiment are tracked with dvc framework following gitflow principles.
* Experiment files tracking is currently done locally in `.dvc_storage` folder.
* Experiments params are set in `Params` class in `pipeline/src/params.py`. 
* Pipeline Stages:
   * `prepare_data`: 
     * Loads dataset, splits it into Train and Test sets, generates Validation Stage set. Save datasets.
   * `search_n_train`:
     * Builds sklearn pipeline, performs params GridSearch, train the model on Train set, saves model artifact, training params and metrics.
   * `evaluate`:
     * Evaluate the model against Test set, saves evaluation metrics.
   * `validate`:
     * Validate model performance against Validation Stage set, compare model metrics with current API loaded model, updates loaded model if candidate model performs better.

### On API

* Run command `sh scripts/run_API.sh` from project root folder in your terminal to:
  * Build and run API docker container
  * Start API
* API is  listening in `http://localhost:5000/`
* GET call `/status` endpoint to check API status.
* POST call `/predict` endpoint with json body format:

```
{
 "form_id": integer,
 "form_features": string containing list of 47 features iin the same order than in the dataset
}
```

* Response format:
  
  ```
  {
    "data":{
        "type": "predictor.form.completion_rate_predicted", 
        "aggregate_id": "2c9ee538-a590-56a2-a857-13777d8fe84c", 
        "data": {
            "form_id": 1123039, 
            "rate_predicted": 0.4863165458406591
        }, 
    "model_id": "5940b8f6-7ca6-4128-b261-869b11562fe6", 
    "occurred_on": "2020-12-13 17:02:37"
    }
  }
  ```
  
* Model file in `model/` folder is watched by tornado API, and hot loaded when it's updated from the pipeline.
* The model artifact contains a unique `version_id` automatically generated everytime the pipeline finishes the training stage.
* Pipeline's Validation Stage only updates the API model when there is a new candidate model that meets the following criteria:
    * Scores better on test set than current loaded model.
    * Process 1500 predictions within 60 seconds.

### On Cloud

* Pipeline can be build and run on demand or automatically triggered by an event on the repository with a CI/CD framework (see a simple `Jenkinsfile` in root directory for reference) on simple AWS ECR + ECS containers. 
* Experiment files tracking can be done remotely in an AWS S3 bucket with minimum changes in the scripts.
* Pipeline output can be published to github PR conversation using cml framework before merging the changes to the default branch. Pipeline container is ready for this. Example: https://github.com/iterative/cml#getting*started
* Ideally, a "merge into default branch" event would trigger a second pipeline to deploy the model in stagging/prod environment.
* As well as the pipeline, the API can be build and run on simple AWS ECR + ECS containers or in bare EC2 instances. Also, as it is a light API and model, it could be deployed in AWS Lambdas and Layers, taking advantage of serverless computing benefits.

### Notebook
`case_study.ipynb` notebook in repository root folder. It contains:

* Dataset Exploration
* Relevant features identification
* Features normalization
* Baseline algorithm selection
* Pipeline model initialization and execution
* API Testing