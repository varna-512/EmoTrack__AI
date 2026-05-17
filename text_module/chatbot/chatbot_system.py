import joblib

# Load trained model
model = joblib.load(
    "../models/text_emotion_model.pkl"
)

# Emotion keyword dictionary
emotion_keywords = {

    "angry": [
        "angry",
        "furious",
        "hate",
        "fight",
        "kill",
        "hit",
        "hitting",
        "mad"
    ],

    "sad": [
        "sad",
        "lonely",
        "broken",
        "cry",
        "depressed",
        "hurt",
        "bad"
    ],

    "anxious": [
        "fear",
        "scared",
        "afraid",
        "worried",
        "anxious",
        "stress",
        "stressed",
        "studies",
        "exam",
        "pressure"
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
        "gross",
        "dirty",
        "vomit",
        "puking"
    ]
}

# Chatbot questions
questions = [

    "How are you feeling today?",

    "What made you feel this way?",

    "How has your day been emotionally?",

    "What is worrying you recently?"
]

# Emotional responses
responses = {

    "happy":
    "That sounds positive. Tell me more.",

    "sad":
    "I understand. Would you like to share more?",

    "angry":
    "That seems frustrating. What caused this feeling?",

    "anxious":
    "Take your time. What has been stressing you?",

    "disgusted":
    "That sounds uncomfortable. Can you explain more?"
}

print("\n🤖 EmoTrack AI Chatbot Started\n")

# Conversation loop
for question in questions:

    print("Bot:", question)

    user_input = input("You: ").lower()

    found = False

    # Rule-based detection
    for emotion, words in emotion_keywords.items():

        if any(word in user_input for word in words):

            prediction = emotion

            found = True

            break

    # ML fallback
    if not found:

        prediction = model.predict(
            [user_input]
        )[0]

    print(
        "Detected Emotion:",
        prediction
    )

    # Emotional response
    if prediction in responses:

        print(
            "Bot:",
            responses[prediction]
        )

    else:

        print(
            "Bot: Thank you for sharing."
        )

    print()