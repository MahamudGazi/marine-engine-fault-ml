from rest_framework import serializers
from .models import PredictionHistory

class TelemetryInputSerializer(serializers.Serializer):
    engine_speed_rpm = serializers.FloatField(default=850.0)
    engine_load_pct = serializers.FloatField(default=75.0)
    fuel_rail_pressure_bar = serializers.FloatField(default=1100.0)
    fuel_flow_rate_kgh = serializers.FloatField(default=220.0)
    scavenge_air_press_bar = serializers.FloatField(default=2.2)
    scavenge_air_temp_c = serializers.FloatField(default=42.0)
    turbocharger_rpm = serializers.FloatField(default=18500.0)
    exhaust_temp_cyl1_c = serializers.FloatField(default=380.0)
    exhaust_temp_cyl2_c = serializers.FloatField(default=380.0)
    exhaust_temp_cyl3_c = serializers.FloatField(default=380.0)
    exhaust_temp_cyl4_c = serializers.FloatField(default=380.0)
    exhaust_temp_cyl5_c = serializers.FloatField(default=380.0)
    exhaust_temp_cyl6_c = serializers.FloatField(default=380.0)
    exhaust_temp_inlet_c = serializers.FloatField(default=440.0)
    exhaust_temp_outlet_c = serializers.FloatField(default=310.0)
    coolant_inlet_temp_c = serializers.FloatField(default=55.0)
    coolant_outlet_temp_c = serializers.FloatField(default=78.0)
    coolant_pressure_bar = serializers.FloatField(default=3.2)
    lube_oil_inlet_temp_c = serializers.FloatField(default=48.0)
    lube_oil_outlet_temp_c = serializers.FloatField(default=68.0)
    lube_oil_pressure_bar = serializers.FloatField(default=4.5)
    crankcase_pressure_mbar = serializers.FloatField(default=3.5)
    vibration_amplitude_mms = serializers.FloatField(default=2.1)

class PredictionHistorySerializer(serializers.ModelSerializer):
    timestamp_formatted = serializers.SerializerMethodField()

    class Meta:
        model = PredictionHistory
        fields = '__all__'

    def get_timestamp_formatted(self, obj):
        return obj.timestamp.strftime("%Y-%m-%d %H:%M:%S")
