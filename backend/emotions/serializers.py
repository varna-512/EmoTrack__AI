from rest_framework import serializers

from .models import EmotionRecord


class EmotionRecordSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = EmotionRecord

        fields = "__all__"