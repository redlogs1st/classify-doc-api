from sqlalchemy.orm import Session
from app.models.documents import Document


def save_document(
    db: Session,
    *,
    text: str,
    label: str,
    confidence: float | None,
    filename: str | None = None,
) -> Document:
    """
    Lưu tài liệu sau khi phân loại vào database.
    Trả về đối tượng Document đã lưu.
    """

    doc = Document(
        filename=filename,
        text=text,
        label=label,
        confidence=confidence,
    )

    db.add(doc)
    db.commit()
    db.refresh(doc)  # lấy id trả về

    return doc
