import numpy as np
import librosa
import noisereduce as nr
import tensorflow as tf
import joblib

# -----------------------------------------
# LOAD MODEL + SCALER + ENCODER
# -----------------------------------------

model = tf.keras.models.load_model(
    "models/emotion_voice_model.h5"
)

scaler = joblib.load(
    "models/scaler.pkl"
)

encoder = joblib.load(
    "models/label_encoder.pkl"
)

# -----------------------------------------
# AUDIO SETTINGS
# -----------------------------------------

SAMPLE_RATE = 16000

# -----------------------------------------
# FEATURE EXTRACTION
# -----------------------------------------

def extract_features(audio_path):

    y, sr = librosa.load(
        audio_path,
        sr=SAMPLE_RATE
    )

    # NOISE REDUCTION

    y = nr.reduce_noise(
        y=y,
        sr=sr,
        stationary=True,
        prop_decrease=0.9
    )

    # NORMALIZATION

    y = librosa.util.normalize(y)

    # MFCC

    mfcc = librosa.feature.mfcc(
        y=y,
        sr=sr,
        n_mfcc=40
    )

    mfcc_mean = np.mean(
        mfcc.T,
        axis=0
    )

    # MEL

    mel = librosa.feature.melspectrogram(
        y=y,
        sr=sr
    )

    mel_mean = np.mean(
        mel.T,
        axis=0
    )

    # CHROMA

    chroma = librosa.feature.chroma_stft(
        y=y,
        sr=sr
    )

    chroma_mean = np.mean(
        chroma.T,
        axis=0
    )

    # RMS

    rms = librosa.feature.rms(
        y=y
    )

    rms_mean = np.mean(
        rms.T,
        axis=0
    )

    # ZCR

    zcr = librosa.feature.zero_crossing_rate(
        y
    )

    zcr_mean = np.mean(
        zcr.T,
        axis=0
    )

    # FINAL FEATURE VECTOR

    features = np.hstack([

        mfcc_mean,

        mel_mean,

        chroma_mean,

        rms_mean,

        zcr_mean
    ])

    return features


# -----------------------------------------
# MAIN PREDICTION FUNCTION
# -----------------------------------------

def predict_emotion(file_path):

    print("\n===================================")
    print(" EmoTrack AI Voice Emotion System ")
    print("===================================\n")

    print("Processing uploaded audio...\n")

    # FEATURE EXTRACTION

    features = extract_features(
        file_path
    )

    # SCALE FEATURES

    features = scaler.transform(
        [features]
    )

    # MODEL PREDICTION

    predictions = model.predict(
        features,
        verbose=0
    )[0]

    # TEMPERATURE SCALING

    temperature = 2.0

    predictions = np.log(
        predictions + 1e-8
    ) / temperature

    predictions = np.exp(
        predictions
    )

    predictions = predictions / np.sum(
        predictions
    )

    # SMOOTHING

    predictions = np.clip(

        predictions,

        0.01,

        0.95
    )

    predictions = predictions / np.sum(
        predictions
    )

    # DOMINANT EMOTION

    predicted_index = np.argmax(
        predictions
    )

    predicted_emotion = encoder.inverse_transform(
        [predicted_index]
    )[0]

    confidence = float(
        np.max(predictions)
    )

    # STRESS SCORE

    stress_index = list(
        encoder.classes_
    ).index("stress")

    stress_prob = predictions[
        stress_index
    ]

    stress_score = int(
        stress_prob * 70
    )

    # FORMAT OUTPUT

    emotion_probs = {}

    for i, emotion in enumerate(
        encoder.classes_
    ):

        emotion_probs[
            str(emotion)
        ] = round(
            float(predictions[i]),
            3
        )

    output = {

        "emotion_probs":
        emotion_probs,

        "confidence":
        round(confidence, 3),

        "stress_score":
        stress_score,

        "dominant_emotion":
        str(predicted_emotion)
    }

    print(output)

    return output