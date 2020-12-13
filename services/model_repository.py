class ModelRepository(object):

    def __init__(self, model):
        self.__model, self.model_id, self.__relevant_feats = model.values()

    def predict(self, form_features):
        input_feats = [form_features[idx] for idx in eval(self.__relevant_feats)]
        pred = self.__model.predict([input_feats])[0]
        print(pred)
        return pred
