import React from 'react';
import { Play, AlertCircle, ShieldCheck, Flame, Cpu, Wind, Droplets, Activity } from 'lucide-react';

export default function ScenarioControls({ onSelectScenario, loading, currentScenario }) {
  const scenarios = [
    { id: 'normal', name: 'Nominal Sea Cruise', desc: 'Standard MCR (850 RPM, 75% load)', icon: ShieldCheck, color: '#10b981' },
    { id: 'turbine', name: 'Turbocharger Fouling', desc: 'Low scavenge boost, high exhaust inlet', icon: Wind, color: '#f59e0b' },
    { id: 'injector', name: 'Injector Malfunction', desc: 'Cylinder 3 & 5 temperature imbalance', icon: Flame, color: '#ef4444' },
    { id: 'scavenge_fire', name: 'Scavenge Air Fire', desc: 'High manifold temp & thermal load', icon: Flame, color: '#ef4444' },
    { id: 'cooling', name: 'Cooling Degradation', desc: 'Elevated outlet temperature & low pressure', icon: Droplets, color: '#f59e0b' },
    { id: 'bearing', name: 'Lube Oil & Bearing Wear', desc: 'Low oil pressure & high RMS vibration', icon: Activity, color: '#ec4899' },
  ];

  return (
    <div className="glass-panel" style={{ padding: '20px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '14px' }}>
        <h3 className="font-hud" style={{ fontSize: '15px', color: '#f1f5f9', letterSpacing: '0.5px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Play size={16} color="#00f2fe" />
          TELEMETRY FAULT INJECTOR & TEST RIG
        </h3>
        <span style={{ fontSize: '11px', color: 'var(--text-dim)', fontFamily: 'var(--font-hud)' }}>
          REAL-TIME SIMULATION
        </span>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '12px' }}>
        {scenarios.map((sc) => {
          const Icon = sc.icon;
          const isActive = currentScenario === sc.id;
          return (
            <button
              key={sc.id}
              disabled={loading}
              onClick={() => onSelectScenario(sc.id)}
              style={{
                background: isActive ? `rgba(0, 242, 254, 0.15)` : 'rgba(9, 13, 20, 0.6)',
                border: `1px solid ${isActive ? '#00f2fe' : 'rgba(255, 255, 255, 0.08)'}`,
                padding: '14px',
                borderRadius: '8px',
                textAlign: 'left',
                cursor: 'pointer',
                transition: 'all 0.2s ease',
                display: 'flex',
                flexDirection: 'column',
                gap: '6px',
                position: 'relative',
                overflow: 'hidden'
              }}
              onMouseEnter={(e) => {
                if (!isActive) e.currentTarget.style.borderColor = sc.color;
              }}
              onMouseLeave={(e) => {
                if (!isActive) e.currentTarget.style.borderColor = 'rgba(255, 255, 255, 0.08)';
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <span className="font-hud" style={{ fontSize: '13px', fontWeight: 600, color: isActive ? '#00f2fe' : '#f1f5f9' }}>
                  {sc.name}
                </span>
                <Icon size={16} color={sc.color} />
              </div>
              <span style={{ fontSize: '11px', color: 'var(--text-muted)', lineHeight: '1.3' }}>
                {sc.desc}
              </span>
            </button>
          );
        })}
      </div>
    </div>
  );
}
