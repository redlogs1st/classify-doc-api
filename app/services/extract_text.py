# app/services/extract_text.py
import os
import tempfile
from io import BytesIO

import pdfplumber
import docx2txt
from fastapi import UploadFile


async def extract_text_from_uploadfile(upload_file: UploadFile) -> str:
    """
    Nhận UploadFile từ FastAPI, trả về text trích xuất.
    Hỗ trợ: .pdf, .docx, .txt
    """
    filename = upload_file.filename or ""
    ext = os.path.splitext(filename)[1].lower()

    # Đọc toàn bộ nội dung file vào memory (bytes)
    file_bytes = await upload_file.read()

    if not file_bytes:
        return ""

    if ext == ".pdf":
        return _extract_text_from_pdf(file_bytes)

    elif ext == ".docx":
        return _extract_text_from_docx(file_bytes, ext)

    elif ext == ".txt":
        return _extract_text_from_txt(file_bytes)

    else:
        # Bạn có thể thêm .doc, .rtf... nếu muốn
        raise ValueError(f"Định dạng file không hỗ trợ: {ext}")


def _extract_text_from_pdf(file_bytes: bytes) -> str:
    """Trích xuất text từ PDF."""
    text_parts: list[str] = []

    with pdfplumber.open(BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            text_parts.append(page_text)

    return "\n".join(text_parts)


def _extract_text_from_docx(file_bytes: bytes, ext: str) -> str:
    """
    docx2txt yêu cầu đường dẫn file,
    nên ta ghi tạm ra file temp rồi đọc.
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name

    try:
        text = docx2txt.process(tmp_path) or ""
    finally:
        # Xoá file tạm
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

    return text


def _extract_text_from_txt(file_bytes: bytes) -> str:
    """Đọc text từ file .txt (UTF-8)."""
    return file_bytes.decode("utf-8", errors="ignore")
