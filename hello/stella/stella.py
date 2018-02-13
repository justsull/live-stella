from .magpie.magpie.main import Magpie
import os
import sys
import json
import numpy
import math


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.integer):
            return int(obj)
        elif isinstance(obj, numpy.floating):
            return float(obj)
        elif isinstance(obj, numpy.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)


class stella:
    def __init__(self):
        self.model = None
        
        dir = os.path.dirname(__file__)
        self.lab_path = os.path.join(dir,'tensor/general.labels')
        self.keras_path = os.path.join(dir,'tensor/models/gen_models.h5')
        self.word2vec_path = os.path.join(dir,'tensor/models/gen_embedding')
        self.scaler_path = os.path.join(dir,'tensor/models/gen_scaler')
        
        self.set_model()

    def set_model(self):
        l = set()
        with open(self.lab_path, 'r') as f_in:
            labels = list(line for line in (l.strip() for l in f_in) if line)
        
        self.model = Magpie(
            keras_model=self.keras_path,
            word2vec_model=self.word2vec_path,
            scaler=self.scaler_path,
            labels = labels)

    def predict(self, text, percent):
        l = self.model.predict_from_text(text)
        prediction = [i[0] for i in l if  i[1] > percent]
        results = json.dumps({'prediction':prediction}, cls=MyEncoder)
        return results

