import React from 'react';
import { Play, ShieldCheck, Wind, Droplets, Flame, Gauge } from 'lucide-react';

const scenarios = [
  { id: 'normal', name: 'Healthy reference', icon: ShieldCheck, color: '#10b981' },
  { id: 'air_filter_clogging', name: 'Air-filter clogging', icon: Wind, color: '#f59e0b' },
  { id: 'air_cooler_fouling', name: 'Air-cooler fouling', icon: Wind, color: '#38bdf8' },
  { id: 'injection_valve_nozzle_clogging', name: 'Injector nozzle clogging', icon: Flame, color: '#ef4444' },
  { id: 'cooling_water_pump_cavitation', name: 'Cooling-water pump cavitation', icon: Droplets, color: '#a78bfa' },
  { id: 'turbine_degradation', name: 'Turbine degradation', icon: Gauge, color: '#ec4899' },
];

export default function ScenarioControls({ onSelectScenario, loading, currentScenario }) {
  return (
    <div className="glass-panel" style={{ padding: '20px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '14px' }}>
        <h3 className="font-hud" style={{ fontSize: '15px', color: '#f1f5f9', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Play size={16} color="#00f2fe" /> DATASET SCENARIO PROFILES
        </h3>
        <span style={{ fontSize: '11px', color: 'var(--text-dim)' }}>MODEL-RECOGNIZED TRAINING EXAMPLES</span>
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '12px' }}>
        {scenarios.map(({ id, name, icon: Icon, color }) => {
          const active = currentScenario === id;
          return (
            <button key={id} disabled={loading} onClick={() => onSelectScenario(id)} style={{
              background: active ? 'rgba(0, 242, 254, 0.15)' : 'rgba(9, 13, 20, 0.6)',
              border: `1px solid ${active ? '#00f2fe' : 'rgba(255,255,255,0.08)'}`,
              padding: '14px', borderRadius: '8px', textAlign: 'left', cursor: 'pointer',
              display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '10px', color: '#f1f5f9'
            }}>
              <span style={{ fontSize: '12px' }}>{name}</span><Icon size={16} color={color} />
            </button>
          );
        })}
      </div>
    </div>
  );
}
