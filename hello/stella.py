from magpie import Magpie
import os

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
        results = [i for i in l if  i[1] > percent]
        return results