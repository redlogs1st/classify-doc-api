# app/api/router_upload.py
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.response import PredictionResponse
from app.services.classify import predict_text
from app.services.extract_text import extract_text_from_uploadfile
from app.services.db_document import save_document
from app.core.database import get_db


router = APIRouter(tags=["upload"])


@router.post("/upload", response_model=PredictionResponse)
async def upload_and_classify(
    file: UploadFile = File(...), db: Session = Depends(get_db)
):
    """
    Nhận file tài liệu (PDF/DOCX/TXT), trích xuất text, rồi phân loại.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="Không có file được upload.")

    try:
        text = await extract_text_from_uploadfile(file)
    except ValueError as e:
        # Lỗi do định dạng không hỗ trợ
        raise HTTPException(status_code=400, detail=str(e))

    if not text or not text.strip():
        raise HTTPException(
            status_code=400,
            detail="Không trích xuất được nội dung từ file (file rỗng hoặc không đọc được).",
        )

    label, confidence = predict_text(text)
    saved = save_document(
        db,
        text=text,
        label=label,
        confidence=confidence,
        filename=file.filename,
    )

    return PredictionResponse(
        label=label,
        confidence=confidence,
        document_id=saved.id,
    )
