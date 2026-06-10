from django.db import models


class AssessmentResult(models.Model):

    # =========================
    # VOICE
    # =========================

    voice_emotion = models.CharField(
        max_length=50
    )

    voice_confidence = models.FloatField()

    # =========================
    # FACE
    # =========================

    face_emotion = models.CharField(
        max_length=50
    )

    face_confidence = models.FloatField()

    # =========================
    # TEXT
    # =========================

    text_emotion = models.CharField(
        max_length=50,
        default="No Data"
    )

    text_confidence = models.FloatField(
        default=0
    )

    # =========================
    # FINAL FUSION
    # =========================

    final_emotion = models.CharField(
        max_length=50
    )

    final_confidence = models.FloatField()

    stress_score = models.IntegerField()

    # =========================
    # TIMESTAMP
    # =========================

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return (
            f"{self.final_emotion} - "
            f"{self.stress_score}"
        )