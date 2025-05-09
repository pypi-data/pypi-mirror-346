import pickle
import os

# Load model only once
model = None
model_path = os.path.join(os.path.dirname(__file__), 'gender_predictor.pkl')
with open(model_path, 'rb') as f:
    model = pickle.load(f)

def predict_gender(name):
    return model.predict([name])[0]
