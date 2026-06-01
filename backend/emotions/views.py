from collections import Counter

from django.db.models import Avg
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import AssessmentResult
from .services.face_service import get_face_prediction
from .services.voice_service import get_voice_prediction
from .services.fusion_service import fuse_emotions


def _percent(value):
    value = float(value or 0)
    return round(value * 100) if value <= 1 else round(value)


def _serialize_assessment(assessment):
    voice_confidence = float(assessment.voice_confidence or 0)
    face_confidence = float(assessment.face_confidence or 0)
    final_confidence = float(assessment.final_confidence or 0)

    voice_result = {
        "dominant_emotion": assessment.voice_emotion,
        "confidence": voice_confidence,
    }
    face_result = {
        "dominant_emotion": assessment.face_emotion,
        "confidence": face_confidence,
    }
    final_result = {
        "final_emotion": assessment.final_emotion,
        "confidence": final_confidence,
        "stress_score": assessment.stress_score,
    }

    return {
        "id": assessment.id,
        "date": assessment.created_at.isoformat(),
        "created_at": assessment.created_at.isoformat(),
        "voice_emotion": assessment.voice_emotion,
        "voice_confidence": voice_confidence,
        "face_emotion": assessment.face_emotion,
        "face_confidence": face_confidence,
        "final_emotion": assessment.final_emotion,
        "final_confidence": final_confidence,
        "confidence": final_confidence,
        "stress_score": assessment.stress_score,
        "voice_result": voice_result,
        "face_result": face_result,
        "final_result": final_result,
        "result": {
            "voice_result": voice_result,
            "face_result": face_result,
            "final_result": final_result,
        },
    }

class MultimodalPredictionAPIView(APIView):

    def post(self, request):


        print("MULTIMODAL API HIT")

        # =========================
        # GET FILES FROM FRONTEND
        # =========================

        audio_file = request.FILES.get("audio")

        image_file = request.FILES.get("image")

        print("\n====================")
        print("MULTIMODAL REQUEST")
        print("====================")

        print("Audio File:", audio_file)
        print("Image File:", image_file)

        # =========================
        # VALIDATION
        # =========================

        if not audio_file and not image_file:

            return Response({

                "error":
                "No audio or image uploaded"

            })

        # =========================
        # MODEL PREDICTIONS
        # =========================

        voice_result = {}

        face_result = {}

        # =========================
        # VOICE
        # =========================

        if audio_file:

            voice_result = get_voice_prediction(
                audio_file
            )

            print("\nVOICE RESULT:")
            print(voice_result)

        # =========================
        # FACE
        # =========================

        if image_file:

            face_result = get_face_prediction(
                image_file
            )

            print("\nFACE RESULT:")
            print(face_result)

        # =========================
        # FUSION
        # =========================

        final_result = fuse_emotions(

            voice_result,

            face_result

        )

        print("\nFINAL RESULT:")
        print(final_result)

        # =========================
        # SAFE EXTRACTION
        # =========================

        voice_emotion = voice_result.get(
            "dominant_emotion",
            "No Data"
        )

        voice_confidence = voice_result.get(
            "confidence",
            0
        )

        face_emotion = face_result.get(
            "dominant_emotion",
            "No Data"
        )

        face_confidence = face_result.get(
            "confidence",
            0
        )

        # =========================
        # SAVE TO DATABASE
        # =========================

        assessment = AssessmentResult.objects.create(

            voice_emotion=voice_emotion,

            voice_confidence=voice_confidence,

            face_emotion=face_emotion,

            face_confidence=face_confidence,

            final_emotion=final_result["final_emotion"],

            final_confidence=final_result["confidence"],

            stress_score=final_result["stress_score"]

        )

        # =========================
        # RETURN
        # =========================

        return Response({

            "id":
            assessment.id,

            "created_at":
            assessment.created_at.isoformat(),

            "voice_result":
            voice_result,

            "face_result":
            face_result,

            "final_result":
            final_result

        })





class AssessmentHistoryAPIView(APIView):

    def get(self, request):

        assessments = AssessmentResult.objects.order_by(
            "-created_at"
        )

        data = []

        for item in assessments:

            data.append({

                "id": item.id,

                "date": item.created_at,

                "final_emotion": item.final_emotion,

                "stress_score": item.stress_score,

                "confidence": item.final_confidence,

                "voice_emotion": item.voice_emotion,

                "face_emotion": item.face_emotion
            })

        return Response(data)


class DashboardAPIView(APIView):

    def get(self, request):
        assessments = list(
            AssessmentResult.objects.order_by("-created_at")
        )

        if not assessments:
            return Response({
                "total_assessments": 0,
                "latest_emotion": None,
                "latest_confidence": 0,
                "latest_stress": 0,
                "average_stress": 0,
                "wellness_score": 0,
                "emotional_stability": 0,
                "trend_data": [],
                "emotion_distribution": [],
                "recent_activity": [],
                "modality_scores": [],
                "wellness_metrics": [],
                "latest_result": None,
            })

        latest = assessments[0]
        average_stress = AssessmentResult.objects.aggregate(
            average=Avg("stress_score")
        )["average"] or 0
        wellness_score = max(0, 100 - round(average_stress))
        latest_result = _serialize_assessment(latest)

        oldest_first = list(reversed(assessments[:7]))
        trend_data = [
            {
                "day": assessment.created_at.strftime("%d %b"),
                "mood": max(0, 100 - int(assessment.stress_score or 0)),
                "stress": int(assessment.stress_score or 0),
                "emotion": assessment.final_emotion,
            }
            for assessment in oldest_first
        ]

        emotion_counts = Counter(
            assessment.final_emotion
            for assessment in assessments
            if assessment.final_emotion
        )
        total = sum(emotion_counts.values()) or 1
        colors = [
            "#14b8a6",
            "#6366f1",
            "#f97316",
            "#64748b",
            "#22c55e",
            "#ef4444",
        ]
        emotion_distribution = [
            {
                "name": emotion,
                "value": round((count / total) * 100),
                "color": colors[index % len(colors)],
            }
            for index, (emotion, count) in enumerate(
                emotion_counts.most_common()
            )
        ]

        recent_activity = [
            {
                "label": f"Completed {assessment.final_emotion} assessment",
                "time": timezone.localtime(
                    assessment.created_at
                ).strftime("%d %b, %I:%M %p"),
            }
            for assessment in assessments[:3]
        ]

        modality_scores = [
            {
                "metric": "Face",
                "score": _percent(latest.face_confidence),
            },
            {
                "metric": "Voice",
                "score": _percent(latest.voice_confidence),
            },
            {
                "metric": "Fusion",
                "score": _percent(latest.final_confidence),
            },
        ]

        wellness_metrics = [
            {
                "label": "Stress Score",
                "value": int(latest.stress_score or 0),
            },
            {
                "label": "Wellness Score",
                "value": max(0, 100 - int(latest.stress_score or 0)),
            },
            {
                "label": "Emotional Stability",
                "value": wellness_score,
            },
            {
                "label": "Face Confidence",
                "value": _percent(latest.face_confidence),
            },
            {
                "label": "Voice Confidence",
                "value": _percent(latest.voice_confidence),
            },
        ]

        return Response({
            "total_assessments": len(assessments),
            "latest_emotion": latest.final_emotion,
            "latest_confidence": latest.final_confidence,
            "latest_stress": latest.stress_score,
            "average_stress": round(average_stress),
            "wellness_score": wellness_score,
            "emotional_stability": wellness_score,
            "trend_data": trend_data,
            "emotion_distribution": emotion_distribution,
            "recent_activity": recent_activity,
            "modality_scores": modality_scores,
            "wellness_metrics": wellness_metrics,
            "latest_result": latest_result["result"],
        })
