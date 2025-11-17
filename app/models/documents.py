from sqlalchemy import Column, Integer, String, Text, Float, DateTime, func
from app.core.database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=True)
    text = Column(Text, nullable=False)
    label = Column(String(100), nullable=False, index=True)
    confidence = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
