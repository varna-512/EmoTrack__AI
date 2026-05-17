from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(["POST"])
def predict_emotion(request):

    text = request.data.get("text")

    text = text.lower()

    if "happy" in text or "good" in text or "great" in text:
        emotion = "happy"

    elif "sad" in text or "cry" in text or "depressed" in text:
        emotion = "sad"

    elif "angry" in text or "mad" in text:
        emotion = "angry"

    elif "stress" in text or "tired" in text:
        emotion = "stressed"

    else:
        emotion = "neutral"

    return Response({
        "emotion": emotion
    })