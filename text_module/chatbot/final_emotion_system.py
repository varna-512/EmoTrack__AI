import time
import joblib

# Load ML model
model = joblib.load(
    "../models/text_emotion_model.pkl"
)

print("\n🤖 EmoTrack AI Started\n")

# Start typing timer
start_time = time.time()

# User input
text = input("How are you feeling today? ").lower()

# End typing timer
end_time = time.time()

# Typing calculations
typing_time = end_time - start_time

word_count = len(text.split())

typing_speed = word_count / typing_time

pause_score = typing_time / max(word_count, 1)

# -----------------------------
# TEXT EMOTION DETECTION
# -----------------------------

emotion_keywords = {

    "angry": [
        "angry",
        "hate",
        "fight",
        "mad",
        "furious"
    ],

    "sad": [
        "sad",
        "lonely",
        "broken",
        "cry",
        "depressed"
    ],

    "anxious": [
        "stress",
        "stressed",
        "worried",
        "scared",
        "afraid",
        "exam",
        "studies"
    ],

    "happy": [
        "happy",
        "excited",
        "joy",
        "love",
        "great"
    ]
}

found = False

for emotion, words in emotion_keywords.items():

    if any(word in text for word in words):

        text_emotion = emotion

        found = True

        break

# ML fallback
if not found:

    text_emotion = model.predict([text])[0]

# -----------------------------
# TYPING PATTERN
# -----------------------------

if typing_speed < 0.4:

    typing_pattern = "Slow Typing"

elif typing_speed < 0.8:

    typing_pattern = "Medium Typing"

else:

    typing_pattern = "Fast Typing"

# -----------------------------
# BEHAVIOR EMOTION
# -----------------------------

if typing_speed < 0.4 and pause_score > 2:

    behavior_emotion = "Anxious"

elif typing_speed < 0.8:

    behavior_emotion = "Stressed"

else:

    behavior_emotion = "Calm"

# -----------------------------
# FINAL EMOTION FUSION
# -----------------------------

if text_emotion == "sad":

    final_emotion = "Sad"

elif text_emotion == "angry":

    final_emotion = "Angry"

elif text_emotion == "anxious":

    final_emotion = "Anxious"

elif text_emotion == "happy" and behavior_emotion == "Calm":

    final_emotion = "Happy"

elif text_emotion == "happy" and behavior_emotion != "Calm":

    final_emotion = "Emotionally Unstable"

else:

    final_emotion = text_emotion

# -----------------------------
# FINAL OUTPUT
# -----------------------------

print("\n========== EmoTrack AI Report ==========")

print(
    "\nText Emotion:",
    text_emotion
)

print(
    "Typing Pattern:",
    typing_pattern
)

print(
    "Behavior Emotion:",
    behavior_emotion
)

print(
    "\nFinal Detected Emotion:",
    final_emotion
)

print(
    "\nTyping Time:",
    round(typing_time, 2),
    "seconds"
)

print(
    "Typing Speed:",
    round(typing_speed, 2),
    "words/sec"
)

print(
    "Pause Score:",
    round(pause_score, 2)
)

print("\n========================================")