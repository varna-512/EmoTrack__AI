
from django.urls import path

from .views import (
    AssessmentHistoryAPIView,
    DashboardAPIView,
    MultimodalPredictionAPIView,
)

urlpatterns = [

    path(
        'multimodal/predict/',
        MultimodalPredictionAPIView.as_view(),
    ),
    path(
        'history/',
        AssessmentHistoryAPIView.as_view(),
    ),
    path(
        'dashboard/',
        DashboardAPIView.as_view(),
    ),
    
]
