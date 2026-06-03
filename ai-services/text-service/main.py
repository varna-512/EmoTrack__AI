from fastapi import FastAPI
import joblib

app = FastAPI()

model = joblib.load(
    "models/text_emotion_model.pkl"
)

@app.get("/")
def home():
    return {
        "message": "Text Service Running"
    }

@app.post("/predict")
def predict(data: dict):

    text = data.get("text", "")

    prediction = model.predict([text])[0]

    probabilities = model.predict_proba([text])[0]

    classes = model.classes_

    emotion_probs = {}

    for emotion, prob in zip(
        classes,
        probabilities
    ):
        emotion_probs[emotion] = float(prob)

    confidence = float(
        max(probabilities)
    )

    return {
        "dominant_emotion": prediction,
        "confidence": confidence,
        "emotion_probs": emotion_probs
    }