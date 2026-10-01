import urllib.request
import json

BASE_URL = "http://localhost:8000/api"

def test_api():
    scenarios = ["normal", "turbine", "injector", "scavenge_fire", "cooling", "bearing"]
    
    print("--- 1. Testing Telemetry Simulator & Predictions ---")
    for sc in scenarios:
        # 1. Fetch simulation
        sim_url = f"{BASE_URL}/telemetry/simulate/?scenario={sc}"
        req = urllib.request.urlopen(sim_url)
        sim_data = json.loads(req.read().decode())
        print(f"\n[SCENARIO: {sc.upper()}] Speed: {sim_data['engine_speed_rpm']} RPM, Load: {sim_data['engine_load_pct']}%")
        
        # 2. Predict
        post_data = json.dumps(sim_data).encode("utf-8")
        pred_req = urllib.request.Request(
            f"{BASE_URL}/predict/",
            data=post_data,
            headers={"Content-Type": "application/json"}
        )
        pred_res = urllib.request.urlopen(pred_req)
        pred_data = json.loads(pred_res.read().decode())
        
        print(f" -> Diagnosed: {pred_data['fault_name']} (Confidence: {pred_data['confidence_pct']}%, Anomaly: {pred_data['is_anomaly']})")
        print(f" -> Top SHAP Driver: {pred_data['shap_explanations'][0]['feature']} (Impact: {pred_data['shap_explanations'][0]['shap_value']})")

    # 3. Test Dashboard Stats
    print("\n--- 2. Testing Dashboard Stats ---")
    stats_req = urllib.request.urlopen(f"{BASE_URL}/dashboard/stats/")
    stats = json.loads(stats_req.read().decode())
    print(f"Total Scans in DB: {stats['total_scans']}, Anomalies: {stats['anomalies_count']}, Anomaly Rate: {stats['anomaly_rate_pct']}%")

    # 4. Test History
    print("\n--- 3. Testing History List ---")
    hist_req = urllib.request.urlopen(f"{BASE_URL}/history/?limit=5")
    hist = json.loads(hist_req.read().decode())
    print(f"Retrieved {len(hist)} history records successfully.")

    print("\n[SUCCESS] All Backend Endpoints Passed Successfully!")

if __name__ == "__main__":
    test_api()
