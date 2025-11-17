# app/api/router_predict.py
from fastapi import APIRouter, Depends
from app.schemas.request import DocumentInput
from app.schemas.response import PredictionResponse
from app.services.classify import predict_text
from app.core.database import get_db
from sqlalchemy.orm import Session
from app.services.db_document import save_document

router = APIRouter(tags=["classification"])


@router.post("/predict", response_model=PredictionResponse)
def classify_document(
    doc: DocumentInput,
    db: Session = Depends(get_db),
):
    label, confidence = predict_text(doc.text)
    saved = save_document(
        db,
        text=doc.text,
        label=label,
        confidence=confidence,
        filename=None,
    )
    return PredictionResponse(
        label=label,
        confidence=confidence,
        document_id=saved.id,
    )
