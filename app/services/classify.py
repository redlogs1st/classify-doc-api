# app/services/classify.py
from typing import Optional
from app.core.model_loader import get_model


def predict_text(text: str) -> tuple[str, Optional[float]]:
    model = get_model()

    # Dự đoán nhãn
    label = model.predict([text])[0]

    # Thử lấy xác suất nếu model hỗ trợ
    proba = None
    if hasattr(model, "predict_proba"):
        probs = model.predict_proba([text])[0]
        proba = float(probs.max())

    return label, proba
