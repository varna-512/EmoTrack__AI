def generate_recommendation(emotion, stress_score):

    recommendations = {

        "happy": {
            "activity": "Continue engaging in social activities",
            "music": "Upbeat music",
            "message": "Keep spreading positivity."
        },

        "sad": {
            "activity": "Talk with friends and family",
            "music": "Relaxing instrumental music",
            "message": "Difficult moments do not last forever."
        },

        "stress": {
            "activity": "Practice meditation",
            "music": "Nature sounds",
            "message": "Take a deep breath and focus on one step at a time."
        },

        "angry": {
            "activity": "Take a short walk",
            "music": "Calm ambient music",
            "message": "Pause before reacting."
        }
    }

    return recommendations.get(
        emotion.lower(),
        {
            "activity": "Take care of yourself",
            "music": "Relaxing music",
            "message": "Stay positive."
        }
    )