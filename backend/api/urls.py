from django.urls import path
from predictions.views import PredictFaultAPIView, PredictionHistoryListView
from dashboard.views import DashboardStatsAPIView, TelemetrySimulatorAPIView

urlpatterns = [
    # Fault Diagnosis & Explainability
    path('predict/', PredictFaultAPIView.as_view(), name='api-predict-fault'),
    path('history/', PredictionHistoryListView.as_view(), name='api-prediction-history'),
    
    # Dashboard & Telemetry Simulator
    path('dashboard/stats/', DashboardStatsAPIView.as_view(), name='api-dashboard-stats'),
    path('telemetry/simulate/', TelemetrySimulatorAPIView.as_view(), name='api-telemetry-simulate'),
]
