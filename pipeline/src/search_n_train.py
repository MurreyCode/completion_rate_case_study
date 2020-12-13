import os
import pandas as pd
import numpy as np
import pickle
import json
from uuid import uuid4
from time import time
from importlib import import_module
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import make_scorer

from params import Params

# input files
train_feat_path = os.path.join(os.getenv('DATA_PATH'), os.getenv('TRAIN_FEATURES_FILENAME'))
train_labels_path = os.path.join(os.getenv('DATA_PATH'), os.getenv('TRAIN_LABELS_FILENAME'))

# output files
model_path = os.path.join(os.getenv('MODEL_PATH'), os.getenv('MODEL_FILENAME'))
best_params_path = os.path.join(os.getenv('MODEL_PATH'), os.getenv('BEST_PARAMS_FILENAME'))
metrics_path = os.path.join(os.getenv('MODEL_PATH'), os.getenv('METRICS_FILENAME'))


def load_data():
    """
    Loads train set
    :return: X_train, y_train
    """

    print("Loading dataset...")
    X_train = pd.read_csv(train_feat_path, low_memory=True).set_index('form_id')
    y_train = pd.read_csv(train_labels_path, low_memory=True).set_index('form_id')

    return X_train, y_train


def load_pipeline():
    """
    Loads training pipeline
    :return: Pipeline, scorer
    """

    Scaler = getattr(
        import_module(
            Params.SCALER_ORIGIN
        ),
        Params.SCALER_NAME
    )

    Model = getattr(
        import_module(
            Params.ALGO_ORIGIN
        ),
        Params.ALGO_NAME
    )

    scorer = make_scorer(
        getattr(
            import_module(
                Params.METRIC_ORIGIN
            ),
            Params.METRIC_NAME
        )
    )

    return Pipeline([('scaler', Scaler()), ('model', Model())]), scorer


if __name__ == "__main__":

    time_init = time()
    print("Starting training stage...")

    X_train, y_train = load_data()
    n_samples, n_features = X_train.shape

    print("Train set:")
    print(f"-> {n_samples} samples")
    print(f"-> {n_features} features")

    pipeline, scorer = load_pipeline()
    model = GridSearchCV(pipeline,
                         param_grid=eval(Params.PARAMS_GRID),
                         cv=Params.CV,
                         scoring=scorer,
                         verbose=1)

    print("Performing grid search...")
    print("Pipeline:", [name for name, _ in pipeline.steps])
    print("Parameters:")
    print(eval(Params.PARAMS_GRID))
    t0 = time()

    model.fit(X_train, y_train.values.ravel())
    print(f"Done in {round((time() - t0), 3)} seconds")
    print()

    model_id = str(uuid4())
    best_parameters = model.best_estimator_.get_params()
    best_score = model.best_score_

    print(f"Trained model ID: {model_id}")
    print(f"Best score on {Params.METRIC_NAME}: {best_score}")
    print("Best parameters set:")
    best_params_dict = {"model_id": model_id}
    for param_name in sorted(best_parameters.keys()):
        if '__' in param_name:
            best_params_dict[param_name.split('__')[1]] = best_parameters[param_name]
            print("\t%s: %r" % (param_name.split('__')[1], best_parameters[param_name]))

    with open(model_path, 'wb') as outfile:
        versioned_model = {
            "model": model,
            "model_id": model_id,
            "feats_idx": Params.RELEVANT_FEATS_IDX}
        pickle.dump(versioned_model, outfile)

    with open(best_params_path, 'w') as outfile:
        json.dump(best_params_dict, outfile)

    metrics = {
        "model_id": model_id,
        "train": {
            Params.METRIC_NAME: best_score,
            "support": X_train.shape[0],
        }
    }

    with open(metrics_path, 'w') as outfile:
        json.dump(metrics, outfile)

    print(f"Training stage finished in {round(time() - time_init, 2)} seconds")
