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
        self.brands_path = os.path.join(dir,'tensor/brands.labels')
        self.celeb_path = os.path.join(dir,'tensor/celebs.labels')
        self.keras_path = os.path.join(dir,'tensor/models/new_models.h5')
        self.word2vec_path = os.path.join(dir,'tensor/models/new_embedding')
        self.scaler_path = os.path.join(dir,'tensor/models/new_scaler')
        self.gen_labels = None
        self.brand_labels = None
        self.celeb_labels = None

        backend.clear_session()
        self.set_labels()
        self.set_model()

    def set_labels(self):
        with open(self.lab_path, 'r') as f_in:
            self.gen_labels = list(line for line in (l.strip() for l in f_in) if line)
        
        with open(self.brands_path, 'r') as f_in:
            self.brand_labels = list(line for line in (l.strip() for l in f_in) if line)
        
        with open(self.celeb_path, 'r') as f_in:
            self.celeb_labels = list(line for line in (l.strip() for l in f_in) if line)

    def set_model(self):
        self.model = Magpie(
            keras_model=self.keras_path,
            word2vec_model=self.word2vec_path,
            scaler=self.scaler_path,
            labels = self.gen_labels)

    def predict(self, text, percent):
        ml_pred = self.model.predict_from_text(text)
        prediction = [i[0] for i in ml_pred if i[1] > percent]
        if 'sponsored' in prediction: prediction.remove('sponsored')
        results = {'prediction':prediction[:10]}
        return results
    
    def fuzzy_predict(self,text,size=1):
        sublist = [" ".join(text.split(" ")[si:ei+1]) for si in range(len(text.split(" "))) for ei in range (si,len(text.split(" "))) if ei-si<size]
        gen_fuz = defaultdict(int)
        brand_fuz = defaultdict(int)
        celeb_fuz = defaultdict(int)
        for i in sublist:
            gfuz = process.extractOne(i, self.gen_labels, scorer=fuzz.ratio)
            bfuz = process.extractOne(i, self.brand_labels, scorer=fuzz.ratio)
            cfuz = process.extractOne(i, self.celeb_labels, scorer=fuzz.ratio)
            if gfuz[1]>90: gen_fuz[gfuz[0]] += 1
            if bfuz[1]>90: brand_fuz[bfuz[0]] += 1
            if cfuz[1]>90: celeb_fuz[cfuz[0]] += 1
        
        gen_fuzzy_pred = sorted(gen_fuz.items(), key=lambda k_v: k_v[1], reverse=True)
        gen_prediction = [i[0] for i in gen_fuzzy_pred]

        brand_fuzzy_pred = sorted(brand_fuz.items(), key=lambda k_v: k_v[1], reverse=True)
        brand_prediction = [i[0] for i in brand_fuzzy_pred]

        celeb_fuzzy_pred = sorted(celeb_fuz.items(), key=lambda k_v: k_v[1], reverse=True)
        celeb_prediction = [i[0] for i in celeb_fuzzy_pred]

        results = {'predictions':{
            'general':gen_prediction,
            'celebrity':celeb_prediction,
            'brand':brand_prediction
            }}

        return results


