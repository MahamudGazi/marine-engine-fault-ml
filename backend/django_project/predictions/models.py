from django.db import models

class PredictionHistory(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    is_anomaly = models.BooleanField(default=False)
    fault_code = models.IntegerField(default=0)
    fault_name = models.CharField(max_length=100, default="Normal Operation")
    confidence_pct = models.FloatField(default=0.0)
    
    # Key mechanical metrics snapshot
    engine_speed_rpm = models.FloatField(null=True, blank=True)
    engine_load_pct = models.FloatField(null=True, blank=True)
    exhaust_temp_inlet_c = models.FloatField(null=True, blank=True)
    scavenge_air_press_bar = models.FloatField(null=True, blank=True)
    vibration_amplitude_mms = models.FloatField(null=True, blank=True)
    
    # Full JSON payloads
    input_telemetry = models.JSONField(default=dict)
    shap_explanations = models.JSONField(default=list)
    class_probabilities = models.JSONField(default=dict)

    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = "Prediction Histories"

    def __str__(self):
        return f"[{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] {self.fault_name} ({self.confidence_pct:.1f}%)"
