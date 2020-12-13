import os
import shutil
import pickle
import json
import pandas as pd
from time import time
from statistics import mean

from params import Params

# input files
validation_set_path = os.path.join(os.getenv('DATA_PATH'), os.getenv('VALIDATION_SET_FILENAME'))
model_path = os.path.join(os.getenv('MODEL_PATH'), os.getenv('MODEL_FILENAME'))
metrics_path = os.path.join(os.getenv('MODEL_PATH'), os.getenv('METRICS_FILENAME'))
metrics_prod_path = os.path.join(os.getenv('MODEL_PROD_PATH'), os.getenv('METRICS_FILENAME'))

# output files
model_prod_path = os.path.join(os.getenv('MODEL_PROD_PATH'), os.getenv('MODEL_FILENAME'))


def load_data():
    """
    Loads train set
    :return: validation_set
    """
    print("Loading dataset...")
    return pd.read_csv(validation_set_path, low_memory=True).set_index('form_id')


def load_model():
    """
    Loads trained model
    :return: model
    """
    with open(model_path, 'rb') as loadfile:
        return pickle.load(loadfile).get('model')


def validate_for_prod(metrics):
    """
    Validates model for deployment in production environment
    :param metrics: Candidate model metrics
    :return: validated, reason
    """
    with open(metrics_prod_path, 'r') as metrics_prod_file:
        metrics_prod = json.load(metrics_prod_file)

    model_prod_metric = metrics_prod.get("evaluate").get(Params.METRIC_NAME)
    model_candidate_metric = metrics.get("evaluate").get(Params.METRIC_NAME)
    total_inference_time = metrics.get("validate").get('set_total_inference_time')

    if model_prod_metric > model_candidate_metric:
        return False, "New model hasn't scored better than the model in prod on test set metrics. Aborted deployment"
    elif total_inference_time > eval(os.getenv('MAX_TOTAL_INFERENCE_TIME')):
        return False, "New model inference-time performance does not meet minimum requirements. Aborted deployment"

    return True, None


if __name__ == '__main__':

    time_init = time()
    print("Starting validation stage...")

    validation_set = load_data()
    n_samples, n_features = validation_set.shape

    print("Validation set:")
    print(f"-> {n_samples} samples")
    print(f"-> {n_features} features")

    model_size = os.stat(model_path).st_size
    model = load_model()

    times = []
    for sample in validation_set.iterrows():
        time_start = time()
        _ = model.predict([sample[1]])
        times.append(time()-time_start)

    total_time = round(sum(times), 2)
    mean_time = round(mean(times), 2)
    max_time = round(max(times), 2)

    with open(metrics_path, 'r') as metrics_file:
        metrics = json.load(metrics_file)
    with open(metrics_path, 'w') as metrics_file:
        metrics['validate'] = {
            "model_size": model_size,
            "validation_set_size": n_samples,
            "set_total_inference_time": total_time,
            "mean_inference_time": mean_time,
            "max_inference_time": max_time
        }
        json.dump(metrics, metrics_file)

    print(f"Model size: {model_size} bytes")
    print(f"Set total inference time: {total_time} seconds")
    print(f"Mean inference time: {mean_time} seconds")
    print(f"Max inference time: {max_time} seconds")

    validated, reason = validate_for_prod(metrics)

    if validated:
        print("Loading new model in API environment")
        shutil.copy(model_path, model_prod_path)
        shutil.copy(metrics_path, metrics_prod_path)
    else:
        print(reason)

    print(f"Validation stage finished in {round(time()-time_init, 2)} seconds")
