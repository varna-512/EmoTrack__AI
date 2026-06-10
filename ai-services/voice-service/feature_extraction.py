import pandas as pd
import numpy as np
import librosa
from tqdm import tqdm
from sklearn.preprocessing import LabelEncoder
import joblib

# ---------------------------------------
# LOAD DATASET CSV
# ---------------------------------------

df = pd.read_csv("processed_dataset.csv")

# ---------------------------------------
# FEATURE EXTRACTION FUNCTION
# ---------------------------------------

def extract_features(file_path):

    try:
        y, sr = librosa.load(file_path, sr=16000)

        # -------------------------------
        # MFCC
        # -------------------------------

        mfcc = librosa.feature.mfcc(
            y=y,
            sr=sr,
            n_mfcc=40
        )

        mfcc_mean = np.mean(mfcc.T, axis=0)

        # -------------------------------
        # MEL SPECTROGRAM
        # -------------------------------

        mel = librosa.feature.melspectrogram(
            y=y,
            sr=sr
        )

        mel_mean = np.mean(mel.T, axis=0)

        # -------------------------------
        # CHROMA
        # -------------------------------

        chroma = librosa.feature.chroma_stft(
            y=y,
            sr=sr
        )

        chroma_mean = np.mean(chroma.T, axis=0)

        # -------------------------------
        # RMS ENERGY
        # -------------------------------

        rms = librosa.feature.rms(y=y)

        rms_mean = np.mean(rms.T, axis=0)

        # -------------------------------
        # ZERO CROSSING RATE
        # -------------------------------

        zcr = librosa.feature.zero_crossing_rate(y)

        zcr_mean = np.mean(zcr.T, axis=0)

        # -------------------------------
        # COMBINE FEATURES
        # -------------------------------

        features = np.hstack([
            mfcc_mean,
            mel_mean,
            chroma_mean,
            rms_mean,
            zcr_mean
        ])

        return features

    except Exception as e:

        print(f"Error processing {file_path}")
        print(e)

        return None

# ---------------------------------------
# EXTRACT FEATURES
# ---------------------------------------

X = []
y = []

print("Extracting features...")

for index, row in tqdm(df.iterrows(), total=len(df)):

    features = extract_features(row["audio_path"])

    if features is not None:

        X.append(features)
        y.append(row["emotion"])

# ---------------------------------------
# CONVERT TO NUMPY
# ---------------------------------------

X = np.array(X)
y = np.array(y)

print("\nFeature Shape:", X.shape)
print("Labels Shape:", y.shape)

# ---------------------------------------
# LABEL ENCODING
# ---------------------------------------

encoder = LabelEncoder()

y_encoded = encoder.fit_transform(y)

# Save encoder
joblib.dump(encoder, "models/label_encoder.pkl")

# ---------------------------------------
# SAVE FEATURES
# ---------------------------------------

np.save("features/X_features.npy", X)
np.save("features/y_labels.npy", y_encoded)

print("\nFeatures saved successfully!")
print("Label Encoder saved!")