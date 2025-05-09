import joblib
import os

model_path = os.path.join(os.path.dirname(__file__), 'gender_predictor.pkl')
_model = joblib.load(model_path)

def predict_gender(name: str) -> str:
    return _model.predict([name])[0]
