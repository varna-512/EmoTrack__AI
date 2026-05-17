import time

print("\n⌨️ Typing Behavior Tracker Started\n")

# Start typing timer
start_time = time.time()

# User input
text = input("Type your sentence: ")

# End typing timer
end_time = time.time()

# Total typing time
typing_time = end_time - start_time

# Word count
word_count = len(text.split())

# Typing speed
typing_speed = word_count / typing_time

# Pause score
pause_score = typing_time / max(word_count, 1)

print("\n--- Typing Analysis ---")

print(
    "Typing Time:",
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

# Typing pattern detection

if typing_speed < 0.5:

    speed_level = "Slow Typing"

elif typing_speed < 1:

    speed_level = "Medium Typing"

else:

    speed_level = "Fast Typing"

# Behavior emotion detection

if typing_speed < 0.4 and pause_score > 2:

    behavior_emotion = "Anxious"

elif typing_speed < 0.8:

    behavior_emotion = "Stressed"

else:

    behavior_emotion = "Happy / Calm"

print(
    "\nTyping Pattern:",
    speed_level
)

print(
    "Behavior Emotion:",
    behavior_emotion
)