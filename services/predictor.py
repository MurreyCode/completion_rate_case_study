from datetime import datetime

from services.singleton import Singleton
from services.model_repository import ModelRepository
from services.uuid_generator import UuidGenerator


class RatePredictor(metaclass=Singleton):

    def __init__(self, uuid_gen: UuidGenerator, repository: ModelRepository):
        super().__init__()
        self.__model = repository
        self.uuid_gen = uuid_gen

    def __predict(self, form_features):
        return self.__model.predict(form_features)

    def __build_response(self, form_id, pred):
        created_at = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        aggregate_id = self.uuid_gen.build_uuid(form_id, self.__model.model_id)
        type_ = 'predictor.form.completion_rate_predicted'
        data = {
            "type": type_,
            "aggregate_id": f'{aggregate_id}',
            "data": {
                "form_id": form_id,
                "rate_predicted": pred,
            },
            "model_id": self.__model.model_id,
            "occurred_on": created_at,
        }
        return data

    def predict(self, form_id, form_features):
        pred = self.__predict(form_features)
        return self.__build_response(form_id, pred)
