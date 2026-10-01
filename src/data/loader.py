import numpy as np
import pandas as pd
import os

FAULT_CLASSES = {
    0: "Normal Operation",
    1: "Turbocharger / Turbine Fouling",
    2: "Fuel Injector Malfunction",
    3: "Scavenge Fire / High Thermal Load",
    4: "Cooling System Degradation",
    5: "Lube Oil & Bearing Wear"
}

def generate_marine_engine_data(n_samples=6000, random_state=42):
    """
    Generates realistic physics-informed telemetry for a marine 4-stroke 6-cylinder diesel engine.
    Simulates Normal operations and 5 distinct mechanical/thermal fault modes.
    """
    np.random.seed(random_state)

    # Base operating parameters
    engine_load = np.random.uniform(30, 95, size=n_samples) # %
    engine_speed = 450 + (engine_load / 100.0) * 450 + np.random.normal(0, 10, size=n_samples) # 450 - 900 RPM
    
    # Normal physics correlations
    fuel_flow = 60 + 3.2 * engine_load + np.random.normal(0, 3, size=n_samples) # kg/h
    fuel_rail_press = 500 + 10.5 * engine_load + np.random.normal(0, 15, size=n_samples) # bar
    
    scavenge_press = 0.9 + 0.028 * engine_load + np.random.normal(0, 0.05, size=n_samples) # bar
    scavenge_temp = 32 + 0.18 * engine_load + np.random.normal(0, 1.2, size=n_samples) # °C
    
    turbo_rpm = 9000 + 180 * engine_load + np.random.normal(0, 200, size=n_samples)
    
    # Base Cylinder Temperatures
    base_exhaust_temp = 280 + 1.8 * engine_load + np.random.normal(0, 8, size=n_samples)
    cyl1 = base_exhaust_temp + np.random.normal(0, 5, size=n_samples)
    cyl2 = base_exhaust_temp + np.random.normal(0, 5, size=n_samples)
    cyl3 = base_exhaust_temp + np.random.normal(0, 5, size=n_samples)
    cyl4 = base_exhaust_temp + np.random.normal(0, 5, size=n_samples)
    cyl5 = base_exhaust_temp + np.random.normal(0, 5, size=n_samples)
    cyl6 = base_exhaust_temp + np.random.normal(0, 5, size=n_samples)
    
    exhaust_inlet = base_exhaust_temp + 45 + np.random.normal(0, 6, size=n_samples)
    exhaust_outlet = exhaust_inlet - 120 + np.random.normal(0, 5, size=n_samples)
    
    # Cooling System
    coolant_inlet = 50 + 0.1 * engine_load + np.random.normal(0, 1.0, size=n_samples)
    coolant_outlet = coolant_inlet + 18 + 0.08 * engine_load + np.random.normal(0, 1.2, size=n_samples)
    coolant_press = 3.6 - 0.005 * engine_load + np.random.normal(0, 0.1, size=n_samples)
    
    # Lubrication & Vibration
    lube_inlet = 44 + 0.12 * engine_load + np.random.normal(0, 1.0, size=n_samples)
    lube_outlet = lube_inlet + 18 + 0.06 * engine_load + np.random.normal(0, 1.2, size=n_samples)
    lube_press = 4.8 - 0.008 * engine_load + np.random.normal(0, 0.12, size=n_samples)
    
    crankcase_press = 2.0 + 0.02 * engine_load + np.random.normal(0, 0.3, size=n_samples)
    vibration = 1.2 + 0.015 * engine_load + np.random.normal(0, 0.15, size=n_samples)

    # Distribute fault classes: 50% normal, 10% each fault type
    fault_type = np.random.choice([0, 1, 2, 3, 4, 5], size=n_samples, p=[0.50, 0.10, 0.10, 0.10, 0.10, 0.10])
    
    for i in range(n_samples):
        ft = fault_type[i]
        severity = np.random.uniform(0.6, 1.0)
        
        if ft == 1: # Turbocharger / Turbine Fouling
            turbo_rpm[i] -= 3500 * severity
            scavenge_press[i] -= 0.65 * severity
            exhaust_inlet[i] += 75 * severity
            exhaust_outlet[i] += 40 * severity
            fuel_flow[i] += 25 * severity # Inefficient combustion
            
        elif ft == 2: # Fuel Injector Malfunction (e.g. Cyl 3 & 5 imbalance)
            bad_cyl = np.random.choice([1, 2, 3, 4, 5, 6])
            if bad_cyl == 1: cyl1[i] -= 85 * severity
            elif bad_cyl == 2: cyl2[i] += 95 * severity
            elif bad_cyl == 3: cyl3[i] -= 90 * severity
            elif bad_cyl == 4: cyl4[i] += 80 * severity
            elif bad_cyl == 5: cyl5[i] -= 95 * severity
            elif bad_cyl == 6: cyl6[i] += 85 * severity
            fuel_rail_press[i] -= 180 * severity
            vibration[i] += 2.2 * severity
            
        elif ft == 3: # Scavenge Fire / High Thermal Load
            scavenge_temp[i] += 38 * severity
            scavenge_press[i] += 0.4 * severity
            exhaust_inlet[i] += 110 * severity
            crankcase_press[i] += 8.5 * severity
            
        elif ft == 4: # Cooling System Degradation
            coolant_outlet[i] += 22 * severity
            coolant_press[i] -= 1.4 * severity
            lube_outlet[i] += 12 * severity
            
        elif ft == 5: # Lube Oil & Bearing Wear
            lube_press[i] -= 1.9 * severity
            lube_outlet[i] += 20 * severity
            vibration[i] += 5.5 * severity
            crankcase_press[i] += 4.2 * severity

    df = pd.DataFrame({
        "engine_speed_rpm": np.round(engine_speed, 1),
        "engine_load_pct": np.round(engine_load, 1),
        "fuel_rail_pressure_bar": np.round(fuel_rail_press, 1),
        "fuel_flow_rate_kgh": np.round(fuel_flow, 1),
        "scavenge_air_press_bar": np.round(scavenge_press, 2),
        "scavenge_air_temp_c": np.round(scavenge_temp, 1),
        "turbocharger_rpm": np.round(turbo_rpm, 0),
        "exhaust_temp_cyl1_c": np.round(cyl1, 1),
        "exhaust_temp_cyl2_c": np.round(cyl2, 1),
        "exhaust_temp_cyl3_c": np.round(cyl3, 1),
        "exhaust_temp_cyl4_c": np.round(cyl4, 1),
        "exhaust_temp_cyl5_c": np.round(cyl5, 1),
        "exhaust_temp_cyl6_c": np.round(cyl6, 1),
        "exhaust_temp_inlet_c": np.round(exhaust_inlet, 1),
        "exhaust_temp_outlet_c": np.round(exhaust_outlet, 1),
        "coolant_inlet_temp_c": np.round(coolant_inlet, 1),
        "coolant_outlet_temp_c": np.round(coolant_outlet, 1),
        "coolant_pressure_bar": np.round(coolant_press, 2),
        "lube_oil_inlet_temp_c": np.round(lube_inlet, 1),
        "lube_oil_outlet_temp_c": np.round(lube_outlet, 1),
        "lube_oil_pressure_bar": np.round(lube_press, 2),
        "crankcase_pressure_mbar": np.round(crankcase_press, 2),
        "vibration_amplitude_mms": np.round(vibration, 2),
        "is_fault": (fault_type > 0).astype(int),
        "fault_class": fault_type,
        "fault_name": [FAULT_CLASSES[f] for f in fault_type]
    })

    return df

if __name__ == "__main__":
    raw_dir = "data/raw/Marine_Engine_Fault_Data"
    proc_dir = "data/processed"
    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(proc_dir, exist_ok=True)

    print("Generating Marine Engine raw dataset...")
    df = generate_marine_engine_data(n_samples=8000, random_state=42)
    
    raw_csv_path = os.path.join(raw_dir, "marine_engine_telemetry.csv")
    df.to_csv(raw_csv_path, index=False)
    print(f"Saved raw dataset to: {raw_csv_path}")

    # Processed datasets
    detection_path = os.path.join(proc_dir, "detection_dataset.parquet")
    classification_path = os.path.join(proc_dir, "classification_dataset.parquet")
    
    df.drop(columns=["fault_class", "fault_name"]).to_parquet(detection_path, index=False)
    df.drop(columns=["is_fault"]).to_parquet(classification_path, index=False)
    
    print(f"Saved detection dataset to: {detection_path}")
    print(f"Saved classification dataset to: {classification_path}")
