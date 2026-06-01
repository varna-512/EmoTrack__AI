
import os
import pandas as pd

# -----------------------------------
# EMOTION LABEL MAPPING
# -----------------------------------

emotion_map = {
    "01": "neutral",
    "02": "neutral",
    "03": "happy",
    "04": "sad",
    "05": "angry",
    "06": "stress",
    "07": "stress",
    "08": "stress"
}

data = []

dataset_path = "datasets/ravdess"

# -----------------------------------
# READ FILES
# -----------------------------------

for root, dirs, files in os.walk(dataset_path):

    for file in files:

        if file.endswith(".wav"):

            parts = file.split("-")

            emotion_code = parts[2]

            emotion = emotion_map.get(emotion_code)

            full_path = os.path.join(root, file)

            data.append([full_path, emotion])

# -----------------------------------
# CREATE DATAFRAME
# -----------------------------------

df = pd.DataFrame(
    data,
    columns=["audio_path", "emotion"]
)

# -----------------------------------
# BALANCE STRESS CLASS
# -----------------------------------

stress_df = df[df["emotion"] == "stress"]

other_df = df[df["emotion"] != "stress"]

# Reduce stress samples
stress_df = stress_df.sample(
    n=500,
    random_state=42
)

# Combine again
df = pd.concat([
    other_df,
    stress_df
])

# Shuffle dataset
df = df.sample(
    frac=1,
    random_state=42
).reset_index(drop=True)

# -----------------------------------
# SAVE CSV
# -----------------------------------

df.to_csv(
    "processed_dataset.csv",
    index=False
)

print("\nBalanced Dataset Created!\n")

print(df["emotion"].value_counts())
