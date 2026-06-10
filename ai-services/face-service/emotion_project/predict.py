import cv2

import numpy as np

from tensorflow.keras.models import load_model


# ======================================================
# LOAD MODEL
# ======================================================

model = load_model(
    "face_emotion_model.h5"
)


# ======================================================
# EMOTION LABELS
# ======================================================

emotions = [

    "angry",

    "disgusted",

    "fearful",

    "happy",

    "neutral",

    "sad",

    "surprised"
]


# ======================================================
# FACE DETECTOR
# ======================================================

face_cascade = cv2.CascadeClassifier(

    cv2.data.haarcascades +

    "haarcascade_frontalface_default.xml"
)


# ======================================================
# PREDICT FUNCTION
# ======================================================

def predict_face_emotion(image_path):

    try:

        # =========================
        # READ IMAGE
        # =========================

        frame = cv2.imread(
            image_path
        )


        # =========================
        # IMAGE CHECK
        # =========================

        if frame is None:

            return {

                "error":
                "Could not read image"
            }


        # =========================
        # DEBUG SAVE
        # =========================

        cv2.imwrite(
            "debug_image.jpg",
            frame
        )


        # =========================
        # CONVERT TO GRAYSCALE
        # =========================

        gray = cv2.cvtColor(

            frame,

            cv2.COLOR_BGR2GRAY
        )


        # =========================
        # FACE DETECTION
        # =========================

        faces = face_cascade.detectMultiScale(

            gray,

            scaleFactor=1.1,

            minNeighbors=3,

            minSize=(30, 30)
        )


        print(
            "Faces detected:",
            len(faces)
        )


        # =========================
        # NO FACE FOUND
        # =========================

        if len(faces) == 0:

            return {

                "error":
                "No face detected"
            }


        # =========================
        # TAKE FIRST FACE
        # =========================

        (x, y, w, h) = faces[0]


        # =========================
        # CROP FACE
        # =========================

        face = gray[
            y:y+h,
            x:x+w
        ]


        # =========================
        # RESIZE
        # =========================

        face = cv2.resize(

            face,

            (48, 48)
        )


        # =========================
        # NORMALIZE
        # =========================

        face_array = face / 255.0


        # =========================
        # RESHAPE
        # =========================

        face_array = face_array.reshape(

            1,

            48,

            48,

            1
        )


        # =========================
        # PREDICTION
        # =========================

        predictions = model.predict(

            face_array,

            verbose=0
        )[0]


        # =========================
        # PROBABILITIES
        # =========================

        emotion_probs = {}

        for emotion, prob in zip(

            emotions,

            predictions
        ):

            emotion_probs[emotion] = round(

                float(prob),

                3
            )


        # =========================
        # DOMINANT EMOTION
        # =========================

        predicted_index = np.argmax(
            predictions
        )

        dominant_emotion = emotions[
            predicted_index
        ]

        confidence = float(
            np.max(predictions)
        )


        # =========================
        # RETURN
        # =========================

        return {

            "emotion_probs":
            emotion_probs,

            "dominant_emotion":
            dominant_emotion,

            "confidence":
            round(confidence, 3)
        }


    except Exception as e:

        return {

            "error":
            str(e)
        }