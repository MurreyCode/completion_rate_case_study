import logging
import os
import traceback
import json
from abc import ABC
from pickle import load
from tornado.web import Application, RequestHandler

from services.predictor import RatePredictor
from services.logic import PredictorLogic
from services.model_repository import ModelRepository
from exceptions.predictor_exceptions import PredictorError
from services.uuid_generator import UuidGenerator


def handle_exception(request_handler_inst, exception, status_error=500):
    error_msg = str(exception) if str(exception) != '' else str(type(exception))
    request_handler_inst.write({"message": error_msg})
    request_handler_inst.set_status(status_error)
    logging.error(request_handler_inst.get("message"))


class PredictHandler(RequestHandler, ABC):
    """
    /predict endpoint request handler
    """

    def initialize(self, predictor):
        self.predictor = predictor

    def post(self):

        try:
            data = json.loads(self.request.body)
            form_id = data.get('form_id')
            form_features = eval(data.get('form_features'))
            predictor_logic = PredictorLogic(self.predictor)
            predictions = predictor_logic.execute_predict(form_id, form_features)
            self.write({"data": predictions})
            self.set_status(200)

        except PredictorError as predictor_error:
            message = str(predictor_error) if str(predictor_error) != '' else str(type(predictor_error))
            logging.error(message)
            self.write(message)
            self.set_status(500)

        except Exception:
            logging.error(traceback.format_exc())
            self.write(traceback.format_exc())
            self.set_status(500)


class StatusHandler(RequestHandler, ABC):
    """
    /status endpoint request handler
    """

    def get(self):
        self.set_status(200)


def make_app(debug=True):

    models_path = os.path.join(os.path.dirname(__file__), '..', os.getenv('MODELS_PATH'))
    with open(models_path, "rb") as model_bytes:
        repository = ModelRepository(load(model_bytes))
    predictor = RatePredictor(UuidGenerator(), repository)

    urls = [
        ("/predict", PredictHandler, dict(predictor=predictor)),
        ("/status", StatusHandler)
         ]
    app = Application(urls, debug=debug)

    return app
