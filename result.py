import joblib

# Load trained model
model = joblib.load("sentiment_model_oct26.joblib")

# Test with new reviews
reviews = [
    "I strongly advise against visiting this centre. Their approach is completely profit-driven, and they focus more on making money than providing genuine care. They try to impress with big promises and by speaking poorly about other clinics, but in reality, there are no qualified doctors who properly examine or treat pets. The quality of treatment is very disappointing, and I would never recommend this place to anyone.",
]

preds = model.predict(reviews)
probs = model.predict_proba(reviews)

for review, pred, prob in zip(reviews, preds, probs):
    print(f"Review: {review}")
    print(f"Prediction: {'Positive' if pred==1 else 'Negative'} (confidence {max(prob):.2f})\n")
