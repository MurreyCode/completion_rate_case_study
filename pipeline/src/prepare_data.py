import os
import pandas as pd
from time import time
from sklearn.model_selection import train_test_split

from params import Params


def save_set(path, filename, ds):
    """
    Saves dataset in given path and filename
    :param path: to save the dataset
    :param filename: to give to the saved file
    :param ds: to be saved
    :return: None
    """
    save_path = os.path.join(path, filename)
    ds.to_csv(path_or_buf=save_path)


# input files
dataset_path = os.path.join(os.getenv('DATA_PATH'), Params.DATASET_FILENAME)


if __name__ == '__main__':

    time_init = time()
    print("Starting data prep stage...")

    dataset = pd.read_csv(dataset_path, low_memory=False)
    dataset.set_index('form_id', inplace=True)

    print("Dataset loaded. Generating dependent feature and splitting into train and test sets...")
    labels = dataset.pop('submissions')/dataset.pop('views')
    X = dataset[eval(Params.RELEVANT_FEATS_NAMES)]

    X_train, X_test, y_train, y_test = train_test_split(X, labels,
                                                        test_size=Params.TEST_SIZE,
                                                        random_state=Params.SEED)

    n_features = X.shape[1]
    train_samples = X_train.shape[0]
    test_samples = X_test.shape[0]
    print(f"Dataset features: {n_features}")
    print(f"Train set: {train_samples} samples")
    print(f"Test set: {test_samples} samples")

    print("Dataset split. Generating validation stage set...")
    validation_set = X_train.sample(n=Params.VALIDATION_SET_SIZE,
                                    random_state=Params.SEED)
    n_samples, _ = validation_set.shape
    print(f"Validation set: {n_samples} samples")

    print("Saving data...")
    save_set(os.getenv('DATA_PATH'), os.getenv('TRAIN_FEATURES_FILENAME'), X_train)
    save_set(os.getenv('DATA_PATH'), os.getenv('TEST_FEATURES_FILENAME'), X_test)
    save_set(os.getenv('DATA_PATH'), os.getenv('TRAIN_LABELS_FILENAME'), y_train)
    save_set(os.getenv('DATA_PATH'), os.getenv('TEST_LABELS_FILENAME'), y_test)
    save_set(os.getenv('DATA_PATH'), os.getenv('VALIDATION_SET_FILENAME'), validation_set)

    print(f"Data prep stage finished in {round(time() - time_init, 2)} seconds")
