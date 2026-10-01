import os
import sys
import unittest
import pandas as pd
from pathlib import Path

# Add src and backend to path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))
sys.path.insert(0, str(ROOT_DIR / "backend" / "django_project"))

from src.features.engineering import compute_domain_features, ALL_FEATURE_COLUMNS
from backend.django_project.predictions.services import MarineInferenceService

class TestMarineEngineInference(unittest.TestCase):
    def setUp(self):
        self.service = MarineInferenceService.get_instance()
        self.sample_telemetry = {
            "engine_speed_rpm": 850.0,
            "engine_load_pct": 75.0,
            "fuel_rail_pressure_bar": 1100.0,
            "fuel_flow_rate_kgh": 220.0,
            "scavenge_air_press_bar": 2.2,
            "scavenge_air_temp_c": 42.0,
            "turbocharger_rpm": 18500.0,
            "exhaust_temp_cyl1_c": 380.0,
            "exhaust_temp_cyl2_c": 380.0,
            "exhaust_temp_cyl3_c": 380.0,
            "exhaust_temp_cyl4_c": 380.0,
            "exhaust_temp_cyl5_c": 380.0,
            "exhaust_temp_cyl6_c": 380.0,
            "exhaust_temp_inlet_c": 440.0,
            "exhaust_temp_outlet_c": 310.0,
            "coolant_inlet_temp_c": 55.0,
            "coolant_outlet_temp_c": 78.0,
            "coolant_pressure_bar": 3.2,
            "lube_oil_inlet_temp_c": 48.0,
            "lube_oil_outlet_temp_c": 68.0,
            "lube_oil_pressure_bar": 4.5,
            "crankcase_pressure_mbar": 3.5,
            "vibration_amplitude_mms": 2.1
        }

    def test_prediction_output(self):
        result = self.service.predict(self.sample_telemetry)
        self.assertIn("is_anomaly", result)
        self.assertIn("fault_name", result)
        self.assertIn("confidence_pct", result)
        self.assertIn("shap_explanations", result)
        self.assertTrue(len(result["shap_explanations"]) > 0)
        print("\n[TEST RESULT] Sample Normal Prediction:", result["fault_name"], f"({result['confidence_pct']}%)")
        print("[SHAP Top Factor]:", result["shap_explanations"][0])

if __name__ == "__main__":
    unittest.main()
