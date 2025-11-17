# app/core/model_loader.py
import os
import joblib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(
    BASE_DIR, "..", "model_training", "models", "text_classifier.joblib"
)

_model = None


def get_model():
    global _model
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                f"Model file not found at {MODEL_PATH}. Hãy train mô hình trước."
            )
        _model = joblib.load(MODEL_PATH)
    return _model
