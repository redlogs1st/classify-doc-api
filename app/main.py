# app/main.py
from fastapi import FastAPI
from app.api.router_predict import router as predict_router
from app.api.router_upload import router as upload_router
from app.core.database import Base, engine
import app.models  # quan trọng để load Document model

app = FastAPI(
    title="Document Classifier API",
    description="API phân loại công văn / tài liệu trường học bằng AI",
    version="1.0.0",
)

# Tạo bảng nếu chưa có
Base.metadata.create_all(bind=engine)

# /api/predict  - nhận text
app.include_router(predict_router, prefix="/api")

# /api/upload   - nhận file
app.include_router(upload_router, prefix="/api")
