import random
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from predictions.models import PredictionHistory

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
    """
    Simulates realistic marine engine operating conditions and specific fault scenarios
    """
    def get(self, request):
        scenario = request.query_params.get("scenario", "normal").lower()
        load = float(request.query_params.get("load", random.uniform(65, 85)))
        speed = 450 + (load / 100.0) * 450 + random.uniform(-5, 5)
        
        fuel_flow = 60 + 3.2 * load + random.uniform(-2, 2)
        fuel_rail = 500 + 10.5 * load + random.uniform(-10, 10)
        scavenge_p = 0.9 + 0.028 * load + random.uniform(-0.02, 0.02)
        scavenge_t = 32 + 0.18 * load + random.uniform(-0.8, 0.8)
        turbo_rpm = 9000 + 180 * load + random.uniform(-100, 100)
        
        base_ex = 280 + 1.8 * load + random.uniform(-4, 4)
        cyl1 = base_ex + random.uniform(-3, 3)
        cyl2 = base_ex + random.uniform(-3, 3)
        cyl3 = base_ex + random.uniform(-3, 3)
        cyl4 = base_ex + random.uniform(-3, 3)
        cyl5 = base_ex + random.uniform(-3, 3)
        cyl6 = base_ex + random.uniform(-3, 3)
        
        ex_inlet = base_ex + 45 + random.uniform(-3, 3)
        ex_outlet = ex_inlet - 120 + random.uniform(-3, 3)
        
        cool_in = 50 + 0.1 * load + random.uniform(-0.5, 0.5)
        cool_out = cool_in + 18 + 0.08 * load + random.uniform(-0.5, 0.5)
        cool_p = 3.6 - 0.005 * load + random.uniform(-0.05, 0.05)
        
        lube_in = 44 + 0.12 * load + random.uniform(-0.5, 0.5)
        lube_out = lube_in + 18 + 0.06 * load + random.uniform(-0.5, 0.5)
        lube_p = 4.8 - 0.008 * load + random.uniform(-0.05, 0.05)
        
        crankcase_p = 2.0 + 0.02 * load + random.uniform(-0.1, 0.1)
        vib = 1.2 + 0.015 * load + random.uniform(-0.1, 0.1)
        
        # Inject scenario mutations
        if scenario in ["turbine", "turbocharger", "turbine_fault"]:
            turbo_rpm -= 3600
            scavenge_p -= 0.68
            ex_inlet += 85
            ex_outlet += 45
            fuel_flow += 24
        elif scenario in ["injector", "fuel_injector"]:
            cyl3 -= 98
            cyl5 += 88
            fuel_rail -= 210
            vib += 2.4
        elif scenario in ["scavenge_fire", "fire"]:
            scavenge_t += 42
            scavenge_p += 0.45
            ex_inlet += 120
            crankcase_p += 9.2
        elif scenario in ["cooling", "cooling_degradation"]:
            cool_out += 24
            cool_p -= 1.6
            lube_out += 14
        elif scenario in ["bearing", "lube_wear", "lube_oil"]:
            lube_p -= 2.1
            lube_out += 22
            vib += 6.2
            crankcase_p += 4.5
            
        data = {
            "engine_speed_rpm": round(speed, 1),
            "engine_load_pct": round(load, 1),
            "fuel_rail_pressure_bar": round(fuel_rail, 1),
            "fuel_flow_rate_kgh": round(fuel_flow, 1),
            "scavenge_air_press_bar": round(scavenge_p, 2),
            "scavenge_air_temp_c": round(scavenge_t, 1),
            "turbocharger_rpm": round(turbo_rpm, 0),
            "exhaust_temp_cyl1_c": round(cyl1, 1),
            "exhaust_temp_cyl2_c": round(cyl2, 1),
            "exhaust_temp_cyl3_c": round(cyl3, 1),
            "exhaust_temp_cyl4_c": round(cyl4, 1),
            "exhaust_temp_cyl5_c": round(cyl5, 1),
            "exhaust_temp_cyl6_c": round(cyl6, 1),
            "exhaust_temp_inlet_c": round(ex_inlet, 1),
            "exhaust_temp_outlet_c": round(ex_outlet, 1),
            "coolant_inlet_temp_c": round(cool_in, 1),
            "coolant_outlet_temp_c": round(cool_out, 1),
            "coolant_pressure_bar": round(cool_p, 2),
            "lube_oil_inlet_temp_c": round(lube_in, 1),
            "lube_oil_outlet_temp_c": round(lube_out, 1),
            "lube_oil_pressure_bar": round(lube_p, 2),
            "crankcase_pressure_mbar": round(crankcase_p, 2),
            "vibration_amplitude_mms": round(vib, 2),
            "scenario": scenario
        }
        
        return Response(data, status=status.HTTP_200_OK)
