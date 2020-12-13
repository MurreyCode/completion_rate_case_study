# python imports
import unittest
from unittest.mock import Mock, patch

# external imports
from tornado.testing import AsyncHTTPTestCase
from tornado.escape import json_decode

# local imports
from services.model_repository import ModelRepository
from exceptions.predictor_exceptions import PredictorError

"""
python -m unittest -v test.tests_predictor.TestClass.test_name
python -m unittest -v test.tests_predictor.PredictorEndpoint.test_predictor_predict_error
"""


class PredictorEndpoint(AsyncHTTPTestCase):

    @patch('services.predictor.RatePredictor.__init__')
    def get_app(self, mock_predictor):
        mock_predictor.return_value = None
        from services.app import make_app
        return make_app()

    @patch('services.predictor.RatePredictor.predict_and_save')
    @patch('services.predictor.RatePredictor.__init__')
    def test_predictor_predictor_error(self, mock_predictor_init, mock_predict):
        mock_predictor_init.return_value = None
        predictor_error_message = "Something went wrong in the Predictor"
        mock_predict.side_effect = Mock(side_effect=PredictorError(predictor_error_message, 500))
        predictor_response = self.fetch('/predict', method='POST', body=b'')
        self.assertEqual(json_decode(predictor_response.body)["message"], predictor_error_message)
        self.assertEqual(predictor_response.code, 500)

    @patch('services.predictor.RatePredictor.predict_and_save')
    @patch('services.predictor.RatePredictor.__init__')
    def test_predictor_ok(self, mock_predictor_init, mock_predict):
        predictor_preds = {"rate_predicted": 0.99}
        mock_predictor_init.return_value = None
        mock_predict.return_value = predictor_preds
        predictor_response = self.fetch('/predict', method='POST', body=b'')
        self.assertEqual(json_decode(predictor_response.body)["data"], predictor_preds)
        self.assertEqual(predictor_response.code, 200)


class PredictorModelRepository(AsyncHTTPTestCase):

    @patch('services.predictor.RatePredictor.__init__')
    def get_app(self, mock_predictor):
        mock_predictor.return_value = None
        from services.app import make_app
        return make_app()

    def test_predict(self):
        mock_predictor = Mock()
        mock_predictor.predict = [[0, 0.99]]
        predictor = ModelRepository(mock_predictor)
        res = predictor.predict('')
        expected_res = [[0, 0.99]]
        self.assertEqual(res, expected_res)


if __name__ == '__main__':
    unittest.main()
