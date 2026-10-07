import os
import sys
import unittest
from pathlib import Path

# Add project root and backend package path.
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))
sys.path.insert(0, str(ROOT_DIR / "backend"))

from backend.predictions.services import MarineInferenceService

class TestMarineEngineInference(unittest.TestCase):
    def setUp(self):
        self.service = MarineInferenceService.get_instance()
        self.sample_telemetry = self.service.simulation_profiles["normal"]

    def test_prediction_output(self):
        result = self.service.predict(self.sample_telemetry)
        self.assertIn("is_anomaly", result)
        self.assertIn("fault_name", result)
        self.assertIn("confidence_pct", result)
        self.assertIn("shap_explanations", result)
        self.assertIn("anomaly_probability", result)
        self.assertIsInstance(result["shap_explanations"], list)
        print("\n[TEST RESULT] Dataset profile prediction:", result["fault_name"], f"({result['confidence_pct']}%)")

if __name__ == "__main__":
    unittest.main()
