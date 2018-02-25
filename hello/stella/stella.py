from magpie import Magpie
import os
import sys
import json
import numpy
import math
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from collections import defaultdict
from keras import backend


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
        self.keras_path = os.path.join(dir,'tensor/models/new_models.h5')
        self.word2vec_path = os.path.join(dir,'tensor/models/new_embedding')
        self.scaler_path = os.path.join(dir,'tensor/models/new_scaler')
        self.labels = None

        backend.clear_session()
        
        self.set_model()

    def set_model(self):
        # l = set()
        with open(self.lab_path, 'r') as f_in:
            self.labels = list(line for line in (l.strip() for l in f_in) if line)

        self.model = Magpie(
            keras_model=self.keras_path,
            word2vec_model=self.word2vec_path,
            scaler=self.scaler_path,
            labels = self.labels)

    def predict(self, text, percent):
        ml_pred = self.model.predict_from_text(text)
        prediction = [i[0] for i in ml_pred if i[1] > percent]
        if 'sponsored' in prediction: prediction.remove('sponsored')
        results = {'prediction':prediction[:10]}
        return results
    
    def fuzzy_predict(self,text,size=1):
        sublist = [" ".join(text.split(" ")[si:ei+1]) for si in range(len(text.split(" "))) for ei in range (si,len(text.split(" "))) if ei-si<size]
        fuzzies = defaultdict(int)
        for i in sublist:
            fuz = process.extractOne(i, self.labels, scorer=fuzz.ratio)
            if fuz[1]>90:
                fuzzies[fuz[0]] += 1
        fuzzy_pred = sorted(fuzzies.items(), key=lambda k_v: k_v[1], reverse=True)
        prediction = [i[0] for i in fuzzy_pred]
        results = {'prediction':prediction}
        return results


