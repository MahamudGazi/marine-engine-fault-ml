from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from predictions.models import PredictionHistory
from predictions.services import ml_service
from src.data.loader import FAULT_CLASS_MAP

class DashboardStatsAPIView(APIView):
    def get(self, request):
        total_scans = PredictionHistory.objects.count()
        anomalies_count = PredictionHistory.objects.filter(is_anomaly=True).count()
        normal_count = total_scans - anomalies_count
        
        fault_distribution = list(
            PredictionHistory.objects.values('fault_name')
            .annotate(count=Count('id'))
            .order_by('-count')
        )
        
        recent_records = PredictionHistory.objects.all()[:10]
        recent_health = [
            {
                "timestamp": r.timestamp.strftime("%H:%M:%S"),
                "is_anomaly": r.is_anomaly,
                "confidence": r.confidence_pct,
                "fault": r.fault_name,
                "engine_speed_rpm": r.engine_speed_rpm,
                "exhaust_temp_inlet_c": r.exhaust_temp_inlet_c
            }
            for r in reversed(recent_records)
        ]
        
        return Response({
            "total_scans": total_scans,
            "anomalies_count": anomalies_count,
            "normal_count": normal_count,
            "anomaly_rate_pct": round((anomalies_count / total_scans * 100), 1) if total_scans > 0 else 0.0,
            "fault_distribution": fault_distribution,
            "recent_health": recent_health
        })

class TelemetrySimulatorAPIView(APIView):
    def get(self, request):
        scenario = request.query_params.get("scenario", "normal").lower()
        class_profiles = {
            key: value for key, value in ml_service.simulation_profiles.items()
            if key != "normal"
        }
        scenario_to_code = {
            fault_type: str(code)
            for fault_type, code in FAULT_CLASS_MAP.items()
        }
        code = scenario_to_code.get(scenario)
        if scenario != "normal" and code is None:
            return Response({"error": "Unknown scenario."}, status=status.HTTP_400_BAD_REQUEST)
        profile = ml_service.simulation_profiles.get("normal") if scenario == "normal" else class_profiles.get(code)
        if profile is None:
            return Response({"error": "Simulation profile unavailable; retrain the models."}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        data = {feature: round(float(value), 6) for feature, value in profile.items()}
        data["scenario"] = scenario
        return Response(data, status=status.HTTP_200_OK)
