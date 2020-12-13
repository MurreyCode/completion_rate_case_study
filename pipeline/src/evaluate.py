import os
import pandas as pd
import numpy as np
import pickle
import json
from time import time
from importlib import import_module

from params import Params

metric = getattr(
        import_module(
            Params.METRIC_ORIGIN
        ),
        Params.METRIC_NAME
    )

# input files
test_feat_path = os.path.join(os.getenv('DATA_PATH'), os.getenv('TEST_FEATURES_FILENAME'))
test_labels_path = os.path.join(os.getenv('DATA_PATH'), os.getenv('TEST_LABELS_FILENAME'))
model_path = os.path.join(os.getenv('MODEL_PATH'), os.getenv('MODEL_FILENAME'))

# output files
metrics_path = os.path.join(os.getenv('MODEL_PATH'), os.getenv('METRICS_FILENAME'))
preds_path = os.path.join(os.getenv('MODEL_PATH'), os.getenv('TEST_PREDS_FILENAME'))


def load_data():

    print("Loading dataset...")
    X_test = pd.read_csv(test_feat_path, low_memory=True).set_index('form_id')
    y_test = pd.read_csv(test_labels_path, low_memory=True).set_index('form_id')

    return X_test, y_test


def load_model():
    with open(model_path, 'rb') as loadfile:
        return pickle.load(loadfile).get('model')


if __name__ == "__main__":
    
    time_init = time()
    print("Starting evaluation stage...")

    X_test, y_test = load_data()
    n_samples, n_features = X_test.shape

    print("Test set:")
    print(f"-> {n_samples} samples")
    print(f"-> {n_features} features")
    
    model = load_model()
    preds = model.predict(X_test)
    score = metric(y_test, preds)

    print(f"Score: {Params.METRIC_NAME}: {score}")

    np.savetxt(preds_path, preds, delimiter=',')

    with open(metrics_path, 'r') as metrics_file:
        metrics = json.load(metrics_file)
    with open(metrics_path, 'w') as metrics_file:
        metrics['evaluate'] = {
            Params.METRIC_NAME: score,
            "support": X_test.shape[0]
        }
        json.dump(metrics, metrics_file)

    print(f"Evaluation stage finished in {round(time() - time_init, 2)} seconds")
