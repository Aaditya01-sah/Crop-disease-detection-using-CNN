from rest_framework import serializers

MAX_UPLOAD_SIZE_MB = 10
ALLOWED_CONTENT_TYPES = ("image/jpeg", "image/jpg", "image/png", "image/webp")


class LeafImageUploadSerializer(serializers.Serializer):
    image = serializers.ImageField()

    def validate_image(self, value):
        if value.content_type not in ALLOWED_CONTENT_TYPES:
            raise serializers.ValidationError(
                f"Unsupported file type '{value.content_type}'. "
                "Please upload a JPEG, PNG, or WEBP image."
            )
        if value.size > MAX_UPLOAD_SIZE_MB * 1024 * 1024:
            raise serializers.ValidationError(
                f"Image too large. Maximum size is {MAX_UPLOAD_SIZE_MB} MB."
            )
        return value
