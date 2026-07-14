

from .recommendation_service import generate_recommendations, generate_wellness_report

print("Recommendation service imported")
def fuse_emotions(

    voice_result,

    face_result,
    text_result=None,
    pulse=None,
    questionnaire=None
):
    questionnaire = questionnaire or {}

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

    text_probs = {}

    if text_result:

     text_probs = text_result.get(
       "emotion_probs",
        {}
    )


    # =========================
    # HANDLE NO DATA
    # =========================

    if (
     not voice_probs and
     not face_probs and
     not text_probs
    ):

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

    questionnaire_probs = _questionnaire_probabilities(
        questionnaire,
        pulse
    )

    all_emotions = set(
     list(voice_probs.keys()) +
     list(face_probs.keys()) +
     list(text_probs.keys()) +
     list(questionnaire_probs.keys())
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
        text_score = text_probs.get(
           emotion,
           0
        )
        questionnaire_score = questionnaire_probs.get(
            emotion,
            0
        )


        combined_score = (
             voice_score * 0.25 +
             face_score * 0.25 +
             text_score * 0.2 +
             questionnaire_score * 0.3
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

    stress_score = _stress_score(
        combined_probs,
        questionnaire,
        pulse
    )


    # =========================
    # RETURN
    # =========================
    recommendations = generate_recommendations(
    combined_probs,
    stress_score,
    questionnaire,
    pulse=pulse,
    face_result=face_result,
    voice_result=voice_result,
    text_result=text_result
)
    report = generate_wellness_report(
        combined_probs,
        stress_score,
        questionnaire,
        pulse,
        face_result,
        voice_result,
        text_result
    )
    recommendations = report.get(
        "personalized_recommendations",
        recommendations
    )
    return {

        "final_emotion":
        dominant_emotion,

        "confidence":
        confidence,

        "stress_score":
        stress_score,

        "final_probabilities":
        combined_probs,
         "recommendations":
    recommendations,
        "report": report,
        "voice_result":
        voice_result,

        "face_result":
        face_result
    }


def average_prediction_results(results):
    valid_results = [
        result for result in results
        if result and result.get("emotion_probs")
    ]

    if not valid_results:
        return {}

    all_emotions = set()
    for result in valid_results:
        all_emotions.update(result.get("emotion_probs", {}).keys())

    averaged_probs = {}
    for emotion in all_emotions:
        averaged_probs[emotion] = round(
            sum(
                result.get("emotion_probs", {}).get(emotion, 0)
                for result in valid_results
            ) / len(valid_results),
            3
        )

    dominant_emotion = max(
        averaged_probs,
        key=averaged_probs.get
    )

    return {
        "dominant_emotion": dominant_emotion,
        "confidence": averaged_probs[dominant_emotion],
        "emotion_probs": averaged_probs,
        "sample_count": len(valid_results),
        "samples": valid_results,
    }


def _questionnaire_probabilities(questionnaire, pulse):
    stress_map = {
        "Not At All": 0,
        "Slightly": 0.2,
        "Moderately": 0.45,
        "Very": 0.7,
        "Extremely": 0.9,
    }
    day_map = {
        "Excellent": 0.85,
        "Good": 0.7,
        "Average": 0.5,
        "Difficult": 0.25,
        "Very Difficult": 0.1,
    }
    stress = stress_map.get(questionnaire.get("stress_level"), 0.35)
    day = day_map.get(questionnaire.get("day_so_far"), 0.5)
    energy = int(questionnaire.get("energy_level") or 5) / 10
    pulse_value = int(float(pulse or 76))
    pulse_stress = min(1, max(0, (pulse_value - 72) / 45))

    anxious = min(1, (stress * 0.65) + (pulse_stress * 0.35))
    happy = min(1, (day * 0.55) + (energy * 0.45))
    sad = min(1, ((1 - day) * 0.45) + ((1 - energy) * 0.35))
    angry = min(1, stress * 0.25)
    neutral = max(0, 1 - max(anxious, happy, sad, angry))

    return {
        "happy": round(happy, 3),
        "sad": round(sad, 3),
        "angry": round(angry, 3),
        "neutral": round(neutral, 3),
        "anxious": round(anxious, 3),
    }


def _stress_score(combined_probs, questionnaire, pulse):
    stress_map = {
        "Not At All": 5,
        "Slightly": 20,
        "Moderately": 45,
        "Very": 70,
        "Extremely": 90,
    }
    model_stress = (
        combined_probs.get("anxious", 0) * 55 +
        combined_probs.get("angry", 0) * 25 +
        combined_probs.get("sad", 0) * 20
    )
    reported_stress = stress_map.get(
        questionnaire.get("stress_level"),
        model_stress
    )
    pulse_value = int(float(pulse or 76))
    pulse_stress = min(100, max(0, (pulse_value - 60) * 1.6))
    return round(
        (model_stress * 0.45) +
        (reported_stress * 0.4) +
        (pulse_stress * 0.15)
    )
