import React from 'react';
import { Gauge, Flame, Wind, Activity, Droplets, Thermometer, Radio } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';

export default function SensorGauges({ telemetry, onTelemetryChange }) {
  if (!telemetry) return null;

  // Prepare Cylinder Exhaust temperatures for Recharts
  const cylData = [
    { name: 'Cyl 1', temp: telemetry.exhaust_temp_cyl1_c || 380 },
    { name: 'Cyl 2', temp: telemetry.exhaust_temp_cyl2_c || 380 },
    { name: 'Cyl 3', temp: telemetry.exhaust_temp_cyl3_c || 380 },
    { name: 'Cyl 4', temp: telemetry.exhaust_temp_cyl4_c || 380 },
    { name: 'Cyl 5', temp: telemetry.exhaust_temp_cyl5_c || 380 },
    { name: 'Cyl 6', temp: telemetry.exhaust_temp_cyl6_c || 380 },
  ];

  const avgCylTemp = cylData.reduce((acc, curr) => acc + curr.temp, 0) / 6;

  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '20px' }}>
      
      {/* 1. Core Propulsion & Load */}
      <div className="glass-panel" style={{ padding: '20px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '16px' }}>
          <Gauge size={18} color="#00f2fe" />
          <h3 className="font-hud glow-primary" style={{ fontSize: '15px', color: '#00f2fe', letterSpacing: '0.5px' }}>
            MAIN PROPULSION DYNAMICS
          </h3>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '14px' }}>
          <div style={{ background: 'rgba(9, 13, 20, 0.6)', padding: '12px', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.05)' }}>
            <div style={{ fontSize: '11px', color: 'var(--text-dim)', textTransform: 'uppercase' }}>ENGINE SPEED</div>
            <div className="font-mono" style={{ fontSize: '22px', fontWeight: 700, color: '#f8fafc', marginTop: '4px' }}>
              {telemetry.engine_speed_rpm?.toFixed(0)} <span style={{ fontSize: '12px', color: '#00f2fe' }}>RPM</span>
            </div>
            <div style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '4px' }}>Rating: Nominal MCR</div>
          </div>

          <div style={{ background: 'rgba(9, 13, 20, 0.6)', padding: '12px', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.05)' }}>
            <div style={{ fontSize: '11px', color: 'var(--text-dim)', textTransform: 'uppercase' }}>ENGINE LOAD</div>
            <div className="font-mono" style={{ fontSize: '22px', fontWeight: 700, color: '#f8fafc', marginTop: '4px' }}>
              {telemetry.engine_load_pct?.toFixed(1)} <span style={{ fontSize: '12px', color: '#00f2fe' }}>%</span>
            </div>
            <div style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '4px' }}>Propeller Torque Load</div>
          </div>

          <div style={{ background: 'rgba(9, 13, 20, 0.6)', padding: '12px', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.05)' }}>
            <div style={{ fontSize: '11px', color: 'var(--text-dim)', textTransform: 'uppercase' }}>FUEL RAIL PRESSURE</div>
            <div className="font-mono" style={{ fontSize: '20px', fontWeight: 700, color: telemetry.fuel_rail_pressure_bar < 900 ? '#f59e0b' : '#f8fafc', marginTop: '4px' }}>
              {telemetry.fuel_rail_pressure_bar?.toFixed(0)} <span style={{ fontSize: '12px', color: '#00f2fe' }}>bar</span>
            </div>
          </div>

          <div style={{ background: 'rgba(9, 13, 20, 0.6)', padding: '12px', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.05)' }}>
            <div style={{ fontSize: '11px', color: 'var(--text-dim)', textTransform: 'uppercase' }}>FUEL FLOW RATE</div>
            <div className="font-mono" style={{ fontSize: '20px', fontWeight: 700, color: '#f8fafc', marginTop: '4px' }}>
              {telemetry.fuel_flow_rate_kgh?.toFixed(1)} <span style={{ fontSize: '12px', color: '#00f2fe' }}>kg/h</span>
            </div>
          </div>
        </div>
      </div>

      {/* 2. Air Intake & Turbocharger System */}
      <div className="glass-panel" style={{ padding: '20px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '16px' }}>
          <Wind size={18} color="#38bdf8" />
          <h3 className="font-hud" style={{ fontSize: '15px', color: '#38bdf8', letterSpacing: '0.5px' }}>
            SCAVENGE & TURBOCHARGER
          </h3>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '14px' }}>
          <div style={{ background: 'rgba(9, 13, 20, 0.6)', padding: '12px', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.05)' }}>
            <div style={{ fontSize: '11px', color: 'var(--text-dim)', textTransform: 'uppercase' }}>TURBO SPEED</div>
            <div className="font-mono" style={{ fontSize: '20px', fontWeight: 700, color: telemetry.turbocharger_rpm < 14000 ? '#ef4444' : '#f8fafc', marginTop: '4px' }}>
              {telemetry.turbocharger_rpm?.toFixed(0)} <span style={{ fontSize: '12px', color: '#38bdf8' }}>RPM</span>
            </div>
            <div style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '4px' }}>Turbine Turbine Wheel</div>
          </div>

          <div style={{ background: 'rgba(9, 13, 20, 0.6)', padding: '12px', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.05)' }}>
            <div style={{ fontSize: '11px', color: 'var(--text-dim)', textTransform: 'uppercase' }}>SCAVENGE AIR PRESS.</div>
            <div className="font-mono" style={{ fontSize: '20px', fontWeight: 700, color: telemetry.scavenge_air_press_bar < 1.7 ? '#ef4444' : '#f8fafc', marginTop: '4px' }}>
              {telemetry.scavenge_air_press_bar?.toFixed(2)} <span style={{ fontSize: '12px', color: '#38bdf8' }}>bar</span>
            </div>
            <div style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '4px' }}>Manifold Boost</div>
          </div>

          <div style={{ background: 'rgba(9, 13, 20, 0.6)', padding: '12px', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.05)' }}>
            <div style={{ fontSize: '11px', color: 'var(--text-dim)', textTransform: 'uppercase' }}>SCAVENGE AIR TEMP</div>
            <div className="font-mono" style={{ fontSize: '20px', fontWeight: 700, color: telemetry.scavenge_air_temp_c > 65 ? '#ef4444' : '#f8fafc', marginTop: '4px' }}>
              {telemetry.scavenge_air_temp_c?.toFixed(1)} <span style={{ fontSize: '12px', color: '#38bdf8' }}>°C</span>
            </div>
          </div>

          <div style={{ background: 'rgba(9, 13, 20, 0.6)', padding: '12px', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.05)' }}>
            <div style={{ fontSize: '11px', color: 'var(--text-dim)', textTransform: 'uppercase' }}>TURBINE INLET TEMP</div>
            <div className="font-mono" style={{ fontSize: '20px', fontWeight: 700, color: telemetry.exhaust_temp_inlet_c > 500 ? '#ef4444' : '#f8fafc', marginTop: '4px' }}>
              {telemetry.exhaust_temp_inlet_c?.toFixed(1)} <span style={{ fontSize: '12px', color: '#38bdf8' }}>°C</span>
            </div>
          </div>
        </div>
      </div>

      {/* 3. Cylinder Exhaust Gas Temperatures Bar Graph */}
      <div className="glass-panel" style={{ padding: '20px', gridColumn: '1 / -1' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '14px', flexWrap: 'wrap', gap: '10px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Flame size={18} color="#f59e0b" />
            <h3 className="font-hud" style={{ fontSize: '15px', color: '#f59e0b', letterSpacing: '0.5px' }}>
              CYLINDER EXHAUST GAS BALANCE (CYL 1 - 6)
            </h3>
          </div>
          <div style={{ fontSize: '12px', color: 'var(--text-muted)', display: 'flex', gap: '16px' }}>
            <span>Mean Exhaust: <strong style={{ color: '#f1f5f9' }}>{avgCylTemp.toFixed(1)} °C</strong></span>
            <span>Spread (Max-Min): <strong style={{ color: (Math.max(...cylData.map(c => c.temp)) - Math.min(...cylData.map(c => c.temp))) > 50 ? '#ef4444' : '#10b981' }}>
              {(Math.max(...cylData.map(c => c.temp)) - Math.min(...cylData.map(c => c.temp))).toFixed(1)} °C
            </strong></span>
          </div>
        </div>

        <div style={{ height: '180px', width: '100%' }}>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={cylData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
              <XAxis dataKey="name" stroke="#64748b" tick={{ fill: '#94a3b8', fontSize: 12, fontFamily: 'var(--font-hud)' }} />
              <YAxis stroke="#64748b" domain={[200, 550]} tick={{ fill: '#94a3b8', fontSize: 11, fontFamily: 'var(--font-mono)' }} />
              <Tooltip 
                contentStyle={{ background: '#0f172a', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px', color: '#fff' }}
                formatter={(val) => [`${val.toFixed(1)} °C`, 'Exhaust Temp']}
              />
              <Bar dataKey="temp" radius={[4, 4, 0, 0]}>
                {cylData.map((entry, index) => {
                  const dev = Math.abs(entry.temp - avgCylTemp);
                  const barColor = dev > 45 ? '#ef4444' : (dev > 25 ? '#f59e0b' : '#38bdf8');
                  return <Cell key={`cell-${index}`} fill={barColor} />;
                })}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* 4. Cooling & Lubrication Systems */}
      <div className="glass-panel" style={{ padding: '20px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '16px' }}>
          <Droplets size={18} color="#10b981" />
          <h3 className="font-hud" style={{ fontSize: '15px', color: '#10b981', letterSpacing: '0.5px' }}>
            COOLING & LUBRICATION STATUS
          </h3>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
          <div style={{ background: 'rgba(9, 13, 20, 0.6)', padding: '10px 12px', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.05)' }}>
            <div style={{ fontSize: '11px', color: 'var(--text-dim)' }}>COOLANT OUTLET</div>
            <div className="font-mono" style={{ fontSize: '18px', fontWeight: 700, color: telemetry.coolant_outlet_temp_c > 88 ? '#ef4444' : '#f8fafc' }}>
              {telemetry.coolant_outlet_temp_c?.toFixed(1)} <span style={{ fontSize: '11px', color: '#10b981' }}>°C</span>
            </div>
          </div>

          <div style={{ background: 'rgba(9, 13, 20, 0.6)', padding: '10px 12px', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.05)' }}>
            <div style={{ fontSize: '11px', color: 'var(--text-dim)' }}>COOLANT PRESS.</div>
            <div className="font-mono" style={{ fontSize: '18px', fontWeight: 700, color: telemetry.coolant_pressure_bar < 2.2 ? '#ef4444' : '#f8fafc' }}>
              {telemetry.coolant_pressure_bar?.toFixed(2)} <span style={{ fontSize: '11px', color: '#10b981' }}>bar</span>
            </div>
          </div>

          <div style={{ background: 'rgba(9, 13, 20, 0.6)', padding: '10px 12px', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.05)' }}>
            <div style={{ fontSize: '11px', color: 'var(--text-dim)' }}>LUBE OIL OUTLET</div>
            <div className="font-mono" style={{ fontSize: '18px', fontWeight: 700, color: telemetry.lube_oil_outlet_temp_c > 82 ? '#ef4444' : '#f8fafc' }}>
              {telemetry.lube_oil_outlet_temp_c?.toFixed(1)} <span style={{ fontSize: '11px', color: '#10b981' }}>°C</span>
            </div>
          </div>

          <div style={{ background: 'rgba(9, 13, 20, 0.6)', padding: '10px 12px', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.05)' }}>
            <div style={{ fontSize: '11px', color: 'var(--text-dim)' }}>LUBE OIL PRESS.</div>
            <div className="font-mono" style={{ fontSize: '18px', fontWeight: 700, color: telemetry.lube_oil_pressure_bar < 3.0 ? '#ef4444' : '#f8fafc' }}>
              {telemetry.lube_oil_pressure_bar?.toFixed(2)} <span style={{ fontSize: '11px', color: '#10b981' }}>bar</span>
            </div>
          </div>
        </div>
      </div>

      {/* 5. Vibration & Mechanical Stress */}
      <div className="glass-panel" style={{ padding: '20px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '16px' }}>
          <Activity size={18} color="#ec4899" />
          <h3 className="font-hud" style={{ fontSize: '15px', color: '#ec4899', letterSpacing: '0.5px' }}>
            VIBRATION & CRANKCASE
          </h3>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
          <div style={{ background: 'rgba(9, 13, 20, 0.6)', padding: '10px 12px', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.05)' }}>
            <div style={{ fontSize: '11px', color: 'var(--text-dim)' }}>RMS VIBRATION</div>
            <div className="font-mono" style={{ fontSize: '18px', fontWeight: 700, color: telemetry.vibration_amplitude_mms > 4.5 ? '#ef4444' : '#f8fafc' }}>
              {telemetry.vibration_amplitude_mms?.toFixed(2)} <span style={{ fontSize: '11px', color: '#ec4899' }}>mm/s</span>
            </div>
            <div style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '4px' }}>ISO 10816 Limit: 4.5</div>
          </div>

          <div style={{ background: 'rgba(9, 13, 20, 0.6)', padding: '10px 12px', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.05)' }}>
            <div style={{ fontSize: '11px', color: 'var(--text-dim)' }}>CRANKCASE PRESS.</div>
            <div className="font-mono" style={{ fontSize: '18px', fontWeight: 700, color: telemetry.crankcase_pressure_mbar > 8.0 ? '#ef4444' : '#f8fafc' }}>
              {telemetry.crankcase_pressure_mbar?.toFixed(2)} <span style={{ fontSize: '11px', color: '#ec4899' }}>mbar</span>
            </div>
            <div style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '4px' }}>Mist Detector Status: OK</div>
          </div>
        </div>
      </div>

    </div>
  );
}
