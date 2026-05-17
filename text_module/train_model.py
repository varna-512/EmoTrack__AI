import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Load dataset
data = pd.read_csv(
    "train.txt",
    sep=";",
    names=["text", "emotion"]
)

# Merge similar emotions
emotion_map = {
    "joy": "happy",
    "love": "happy",
    "sadness": "sad",
    "anger": "angry",
    "fear": "anxious",
    "surprise": "neutral"
}

data["emotion"] = data["emotion"].map(
    emotion_map
)

# Input text
X = data["text"]

# Output labels
y = data["emotion"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Better NLP Pipeline
model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2)
        )
    ),
    (
        "classifier",
        LogisticRegression(
            max_iter=200
        )
    )
])

# Train model
model.fit(X_train, y_train)

# Predict
predictions = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(
    y_test,
    predictions
)

print("Accuracy:", accuracy)

# Save model
joblib.dump(
    model,
    "models/text_emotion_model.pkl"
)

print("Improved model saved successfully")