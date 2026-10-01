from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TelemetryInputSerializer, PredictionHistorySerializer
from .services import ml_service
from .models import PredictionHistory

class PredictFaultAPIView(APIView):
    """
    Primary Marine Engine Fault Diagnosis & SHAP Explanation Endpoint
    """
    def post(self, request):
        serializer = TelemetryInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        telemetry_data = serializer.validated_data
        
        # ML Inference
        try:
            prediction_result = ml_service.predict(telemetry_data)
        except Exception as e:
            return Response({"error": f"Inference engine failure: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Save to History
        history_entry = PredictionHistory.objects.create(
            is_anomaly=prediction_result["is_anomaly"],
            fault_code=prediction_result["fault_code"],
            fault_name=prediction_result["fault_name"],
            confidence_pct=prediction_result["confidence_pct"],
            engine_speed_rpm=telemetry_data.get("engine_speed_rpm"),
            engine_load_pct=telemetry_data.get("engine_load_pct"),
            exhaust_temp_inlet_c=telemetry_data.get("exhaust_temp_inlet_c"),
            scavenge_air_press_bar=telemetry_data.get("scavenge_air_press_bar"),
            vibration_amplitude_mms=telemetry_data.get("vibration_amplitude_mms"),
            input_telemetry=telemetry_data,
            shap_explanations=prediction_result["shap_explanations"],
            class_probabilities=prediction_result["class_probabilities"]
        )
        
        response_payload = {
            "history_id": history_entry.id,
            "timestamp": history_entry.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            **prediction_result
        }
        
        return Response(response_payload, status=status.HTTP_200_OK)

class PredictionHistoryListView(APIView):
    """
    Get recent prediction logs with pagination / limit
    """
    def get(self, request):
        limit = int(request.query_params.get("limit", 20))
        records = PredictionHistory.objects.all()[:limit]
        serializer = PredictionHistorySerializer(records, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request):
        PredictionHistory.objects.all().delete()
        return Response({"message": "History cleared successfully."}, status=status.HTTP_200_OK)
