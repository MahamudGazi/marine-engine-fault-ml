import numpy as np
import pandas as pd

def compute_domain_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes thermodynamic and mechanical engineering features for Marine Engine diagnostics:
    1. Exhaust gas thermal deviation across cylinders (std and max spread)
    2. Turbine temperature drop ratio (Inlet vs Outlet)
    3. Scavenge to fuel mass ratio (proxy for air-fuel ratio)
    4. Coolant temperature rise (Delta T)
    5. Lube oil temperature rise (Delta T)
    6. Specific mechanical load efficiency
    """
    data = df.copy()
    
    cyl_cols = [
        "exhaust_temp_cyl1_c", "exhaust_temp_cyl2_c", "exhaust_temp_cyl3_c",
        "exhaust_temp_cyl4_c", "exhaust_temp_cyl5_c", "exhaust_temp_cyl6_c"
    ]
    
    # 1. Cylinder Thermal Balance
    data["cyl_temp_mean"] = data[cyl_cols].mean(axis=1)
    data["cyl_temp_std"] = data[cyl_cols].std(axis=1)
    data["cyl_temp_max_spread"] = data[cyl_cols].max(axis=1) - data[cyl_cols].min(axis=1)
    
    # 2. Turbine Thermal Gradient
    data["turbine_delta_temp"] = data["exhaust_temp_inlet_c"] - data["exhaust_temp_outlet_c"]
    data["turbine_temp_ratio"] = data["exhaust_temp_inlet_c"] / (data["exhaust_temp_outlet_c"] + 1e-5)
    
    # 3. Turbocharger Compression Ratio Proxy
    data["turbo_pressure_ratio"] = data["scavenge_air_press_bar"] / 1.013 # vs atmospheric
    data["turbo_speed_to_scavenge"] = data["turbocharger_rpm"] / (data["scavenge_air_press_bar"] + 1e-5)
    
    # 4. Cooling System Thermal Rise
    data["coolant_delta_t"] = data["coolant_outlet_temp_c"] - data["coolant_inlet_temp_c"]
    
    # 5. Lubrication System Thermal Rise
    data["lube_oil_delta_t"] = data["lube_oil_outlet_temp_c"] - data["lube_oil_inlet_temp_c"]
    
    # 6. Specific Fuel Consumption Proxy
    data["fuel_to_load_ratio"] = data["fuel_flow_rate_kgh"] / (data["engine_load_pct"] + 1e-5)
    
    return data

RAW_FEATURE_COLUMNS = [
    "engine_speed_rpm",
    "engine_load_pct",
    "fuel_rail_pressure_bar",
    "fuel_flow_rate_kgh",
    "scavenge_air_press_bar",
    "scavenge_air_temp_c",
    "turbocharger_rpm",
    "exhaust_temp_cyl1_c",
    "exhaust_temp_cyl2_c",
    "exhaust_temp_cyl3_c",
    "exhaust_temp_cyl4_c",
    "exhaust_temp_cyl5_c",
    "exhaust_temp_cyl6_c",
    "exhaust_temp_inlet_c",
    "exhaust_temp_outlet_c",
    "coolant_inlet_temp_c",
    "coolant_outlet_temp_c",
    "coolant_pressure_bar",
    "lube_oil_inlet_temp_c",
    "lube_oil_outlet_temp_c",
    "lube_oil_pressure_bar",
    "crankcase_pressure_mbar",
    "vibration_amplitude_mms"
]

ENGINEERED_FEATURE_COLUMNS = [
    "cyl_temp_mean",
    "cyl_temp_std",
    "cyl_temp_max_spread",
    "turbine_delta_temp",
    "turbine_temp_ratio",
    "turbo_pressure_ratio",
    "turbo_speed_to_scavenge",
    "coolant_delta_t",
    "lube_oil_delta_t",
    "fuel_to_load_ratio"
]

ALL_FEATURE_COLUMNS = RAW_FEATURE_COLUMNS + ENGINEERED_FEATURE_COLUMNS
