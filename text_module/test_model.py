import joblib

# Load trained model
model = joblib.load(
    "models/text_emotion_model.pkl"
)

# Emotion keyword dictionary
emotion_keywords = {

    "angry": [
        "angry",
        "furious",
        "hate",
        "fight",
        "kill",
        "hitting",
        "hit",
        "mad"
    ],

    "sad": [
        "sad",
        "lonely",
        "broken",
        "cry",
        "depressed",
        "hurt",
        "upset"
    ],

    "anxious": [
        "fear",
        "scared",
        "afraid",
        "worried",
        "anxious",
        "stress",
        "stressed",
        "nervous"
    ],

    "happy": [
        "happy",
        "joy",
        "excited",
        "love",
        "great",
        "good",
        "awesome"
    ],

    "disgusted": [
        "disgust",
        "disgusted",
        "gross",
        "puking",
        "vomit",
        "dirty"
    ]
}

while True:

    text = input(
        "Enter text: "
    ).lower()

    found = False

    # Rule-based detection
    for emotion, words in emotion_keywords.items():

        if any(word in text for word in words):

            print(
                "Predicted Emotion:",
                emotion
            )

            found = True

            break

    # ML prediction fallback
    if not found:

        prediction = model.predict([text])[0]

        print(
            "Predicted Emotion:",
            prediction
        )