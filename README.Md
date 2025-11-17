
```bash
cd document_classifier

# Tạo venv (nên dùng Python 3.10+)
python -m venv .venv
# Windows:
.\.venv\Scripts\activate
# Linux/WSL:
source .venv/bin/activate

# Cài thư viện cần thiết
pip install -r requirements.txt
```
## Cấu trúc thư mục
app : FastAPI
data : dataset 
model_training: tiền xử lý & train mô hình

## Chuẩn bị dữ liệu huấn luyện (CSV)
data/dataset.csv
- text: nội dung công văn (hoặc tóm tắt)
- label: nhãn (tự đặt, không dấu, viết liền)
## Viết code tiền xử lý & train mô hình
- File tiền xử lý: model_training/preprocess.py
- File train mô hình: model_training/train.py
    ```bash
        # Đảm bảo đang activate venv
        cd model_training
        python train.py
    ```
- Kết quả:
- Bảng classification_report in ra
- File model_training/models/text_classifier.joblib được tạo

## Xây dựng API với FastAPI
app/core/model_loader.py

## Chạy FastAPI server

```bash
uvicorn app.main:app --reload
```

## Daataabase lưu trữ tài liệu đã phân loại
- Sử dụng SQLite (file: document_db.sqlite3)

## File upload tài liệu để phân loại
- Endpoint: /upload
- Hỗ trợ file: PDF, DOCX, TXT
- Trả về: nhãn phân loại, độ tin cậy, document_id (ID tài liệu trong database)
- File: data/raw/