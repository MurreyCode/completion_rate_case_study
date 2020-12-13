class Params:

    SEED = 6
    VALIDATION_SET_SIZE = 1500
    DATASET_FILENAME = 'completion_rate.csv'
    RELEVANT_FEATS_NAMES = "['feat_33', 'feat_19', 'feat_06', 'feat_34', 'feat_38', \
                            'feat_36', 'feat_40', 'feat_07', 'feat_30', 'feat_27']"
    RELEVANT_FEATS_IDX = "[32, 18, 5, 33, 37, 35, 39, 6, 29, 26]"
    TEST_SIZE = 0.2
    CV = 5
    SCALER_NAME = 'MinMaxScaler'
    SCALER_ORIGIN = 'sklearn.preprocessing'
    METRIC_NAME = 'mean_squared_error'
    METRIC_ORIGIN = 'sklearn.metrics'
    ALGO_NAME = 'GradientBoostingRegressor'
    ALGO_ORIGIN = 'sklearn.ensemble'
    PARAMS_GRID = '''{
        'model__n_estimators': [25],
        'model__learning_rate': [0.1],
        'model__max_depth': [2],
        'model__random_state': [Params.SEED]
    }'''
