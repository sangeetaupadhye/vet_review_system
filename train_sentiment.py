import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
import joblib
import argparse

# train_sentiment.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
import joblib
import argparse


def train_model(input_csv, model_out):
    # Load dataset
    df = pd.read_csv(input_csv)

    # ✅ Rename column
    if "Review" in df.columns:
        df.rename(columns={"Review": "review"}, inplace=True)

    if "review" not in df.columns or "label" not in df.columns:
        raise ValueError("CSV must contain 'review' and 'label' columns")

    # ✅ Clean data
    df = df[df["review"].notnull()]               # remove NaN
    df["review"] = df["review"].astype(str)       # convert all to string
    df = df[df["review"].str.strip() != ""]       # remove empty strings
    df = df[df["review"].str.lower() != "nan"]    # remove literal "nan"
    df = df[df["label"].notnull()]                # ensure labels exist

    print(f"✅ Cleaned dataset size: {len(df)} rows")

    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(
        df["review"], df["label"], test_size=0.2, stratify=df["label"], random_state=42
    )

    # Build model pipeline
    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=2, stop_words="english")),
        ("clf", LogisticRegression(max_iter=500, class_weight="balanced"))
    ])

    # Train
    pipeline.fit(X_train, y_train)

    # Evaluate
    y_pred = pipeline.predict(X_test)
    print("\n📊 Classification Report:")
    print(classification_report(y_test, y_pred))

    # Save model
    joblib.dump(pipeline, model_out)
    print(f"\n✅ Model saved to {model_out}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train a sentiment analysis model")
    parser.add_argument("--data", type=str, required=True, help="Path to CSV dataset (with 'review','label')")
    parser.add_argument("--out", type=str, default="sentiment_model.joblib", help="Output model file path")
    args = parser.parse_args()

    train_model(args.data, args.out)
