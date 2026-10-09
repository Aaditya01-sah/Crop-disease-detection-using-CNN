from django.urls import path

from .views import HealthCheckView, PredictDiseaseView

urlpatterns = [
    path("predict/", PredictDiseaseView.as_view(), name="predict-disease"),
    path("health/", HealthCheckView.as_view(), name="health-check"),
]
