# model_training/train.py
import os
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

from preprocess import clean_text

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "dataset.csv")
MODEL_DIR = os.path.join(BASE_DIR, "models")

os.makedirs(MODEL_DIR, exist_ok=True)


def load_data():
    df = pd.read_csv(DATA_PATH)
    # Đảm bảo có cột text, label
    df["text"] = df["text"].astype(str).apply(clean_text)
    df["label"] = df["label"].astype(str)
    return df


def train():
    df = load_data()
    X = df["text"].values
    y = df["label"].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Pipeline: TF-IDF + Logistic Regression
    pipeline = Pipeline(
        [
            (
                "tfidf",
                TfidfVectorizer(
                    max_features=5000,
                    ngram_range=(1, 2),  # 1-gram, 2-gram
                ),
            ),
            ("clf", LogisticRegression(max_iter=1000)),
        ]
    )

    pipeline.fit(X_train, y_train)

    # Đánh giá
    y_pred = pipeline.predict(X_test)
    print("=== Classification report ===")
    print(classification_report(y_test, y_pred))

    # Lưu model (pipeline đã gồm cả vectorizer + classifier)
    model_path = os.path.join(MODEL_DIR, "text_classifier.joblib")
    joblib.dump(pipeline, model_path)
    print(f"Saved model to {model_path}")


if __name__ == "__main__":
    train()
