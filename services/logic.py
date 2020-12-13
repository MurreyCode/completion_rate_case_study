from services.predictor import RatePredictor


class PredictorLogic(object):

    def __init__(self, predictor: RatePredictor):
        self.__predictor = predictor

    def execute_predict(self, form_id, form_features):
        """

        :param form_id:
        :param form_features:
        :return:
        """
        return self.__predictor.predict(form_id, form_features)
