def fuse_emotions(

    voice_result,

    face_result
):

    # =========================
    # SAFE EXTRACTION
    # =========================

    voice_probs = voice_result.get(

        "emotion_probs",

        {}
    )

    face_probs = face_result.get(

        "emotion_probs",

        {}
    )


    # =========================
    # HANDLE NO DATA
    # =========================

    if not voice_probs and not face_probs:

        return {

            "final_emotion":
            "No emotion detected",

            "confidence":
            0,

            "stress_score":
            0,

            "final_probabilities":
            {}
        }


    # =========================
    # COMBINE ALL EMOTIONS
    # =========================

    all_emotions = set(

        list(voice_probs.keys()) +

        list(face_probs.keys())
    )


    combined_probs = {}


    # =========================
    # WEIGHTED FUSION
    # =========================

    for emotion in all_emotions:

        voice_score = voice_probs.get(

            emotion,

            0
        )

        face_score = face_probs.get(

            emotion,

            0
        )


        # 50-50 weighting

        combined_score = (

            voice_score * 0.5 +

            face_score * 0.5
        )


        combined_probs[emotion] = round(

            combined_score,

            3
        )


    # =========================
    # DOMINANT EMOTION
    # =========================

    dominant_emotion = max(

        combined_probs,

        key=combined_probs.get
    )


    confidence = combined_probs[
        dominant_emotion
    ]


    # =========================
    # STRESS SCORE
    # =========================

    stress_score = 0


    if "stress" in combined_probs:

        stress_score = int(

            combined_probs["stress"] * 100
        )


    # =========================
    # RETURN
    # =========================

    return {

        "final_emotion":
        dominant_emotion,

        "confidence":
        confidence,

        "stress_score":
        stress_score,

        "final_probabilities":
        combined_probs,

        "voice_result":
        voice_result,

        "face_result":
        face_result
    }