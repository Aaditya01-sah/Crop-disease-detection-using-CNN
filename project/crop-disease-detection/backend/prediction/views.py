import logging

from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .disease_info import get_disease_info
from .model_utils import predict_disease
from .serializers import LeafImageUploadSerializer

logger = logging.getLogger(__name__)


class PredictDiseaseView(APIView):
    """
    POST /api/predict/

    Accepts a multipart image upload (field name: "image"), preprocesses it
    with OpenCV, runs inference through the trained CNN, and returns the
    predicted disease class, confidence score, and a short description --
    exactly the response contract described in section 3.2.3.
    """
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = LeafImageUploadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"error": "invalid_input", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        image_file = serializer.validated_data["image"]

        try:
            image_bytes = image_file.read()
            result = predict_disease(image_bytes, top_k=3)
        except FileNotFoundError as exc:
            logger.error("Model not found: %s", exc)
            return Response(
                {"error": "model_unavailable", "details": str(exc)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        except ValueError as exc:
            return Response(
                {"error": "invalid_image", "details": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as exc:  # noqa: BLE001
            logger.exception("Prediction failed")
            return Response(
                {"error": "prediction_failed", "details": str(exc)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        info = get_disease_info(result["predicted_class"])

        response_payload = {
            "predicted_class": result["predicted_class"],
            "display_name": info["display_name"],
            "is_healthy": info["is_healthy"],
            "confidence": round(result["confidence"] * 100, 2),
            "description": info["description"],
            "recommendation": info["recommendation"],
            "top_predictions": [
                {
                    "display_name": get_disease_info(p["class_name"])["display_name"],
                    "confidence": round(p["confidence"] * 100, 2),
                }
                for p in result["top_predictions"]
            ],
        }
        return Response(response_payload, status=status.HTTP_200_OK)


class HealthCheckView(APIView):
    """GET /api/health/ -- simple liveness probe used by the frontend/deployment."""

    def get(self, request, *args, **kwargs):
        return Response({"status": "ok"})
