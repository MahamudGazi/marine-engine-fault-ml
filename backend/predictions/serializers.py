import math

from rest_framework import serializers
from .models import PredictionHistory
from .services import ml_service


class TelemetryInputSerializer(serializers.Serializer):
    """Validate the sensor vector against the feature schema in the models."""

    def to_internal_value(self, data):
        if not isinstance(data, dict):
            raise serializers.ValidationError("Expected a JSON object of sensor values.")
        missing = [name for name in ml_service.feature_columns if name not in data]
        if missing:
            raise serializers.ValidationError({
                "missing_fields": missing,
                "detail": "Provide every sensor field expected by the trained model.",
            })
        parsed = {}
        errors = {}
        for name in ml_service.feature_columns:
            try:
                value = float(data[name])
                if not math.isfinite(value):
                    raise ValueError("Must be finite.")
                parsed[name] = value
            except (TypeError, ValueError):
                errors[name] = "A finite numeric value is required."
        if errors:
            raise serializers.ValidationError(errors)
        return parsed


class PredictionHistorySerializer(serializers.ModelSerializer):
    timestamp_formatted = serializers.SerializerMethodField()

    class Meta:
        model = PredictionHistory
        fields = "__all__"

    def get_timestamp_formatted(self, obj):
        return obj.timestamp.strftime("%Y-%m-%d %H:%M:%S")
