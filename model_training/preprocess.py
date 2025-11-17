import re


def clean_text(text: str) -> str:
    """
    Làm sạch text cơ bản.
    Sau này bạn có thể thêm:
    - bỏ tiêu đề 'CỘNG HOÀ XÃ HỘI CHỦ NGHĨA VIỆT NAM'...
    """
    if not isinstance(text, str):
        return ""

    text = text.strip()
    # Đưa về lowercase
    text = text.lower()
    # Bỏ ký tự thừa (giữ chữ, số, dấu cách, dấu chấm phẩy cơ bản)
    text = re.sub(r"[^0-9a-zA-ZÀ-Ỹà-ỹ\s\.,:/-]", " ", text)
    # Gom nhiều dấu cách thành 1
    text = re.sub(r"\s+", " ", text)
    return text
