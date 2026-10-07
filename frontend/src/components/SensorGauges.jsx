import React from 'react';

const prettyName = (name) => name.replaceAll('_', ' ');

export default function SensorGauges({ telemetry }) {
  if (!telemetry) return null;
  const entries = Object.entries(telemetry).filter(([key, value]) => key !== 'scenario' && Number.isFinite(Number(value)));
  return (
    <section className="glass-panel" style={{ padding: '20px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: '10px', marginBottom: '16px', flexWrap: 'wrap' }}>
        <h3 className="font-hud" style={{ fontSize: '15px', color: '#00f2fe', margin: 0 }}>MARINE DATASET SENSOR VECTOR</h3>
        <span style={{ fontSize: '11px', color: 'var(--text-dim)' }}>{entries.length} model inputs</span>
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(185px, 1fr))', gap: '10px' }}>
        {entries.map(([key, value]) => (
          <div key={key} title={key} style={{ background: 'rgba(9,13,20,0.6)', padding: '11px 12px', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.05)', minWidth: 0 }}>
            <div style={{ color: 'var(--text-dim)', fontSize: '10px', textTransform: 'uppercase', lineHeight: 1.4, minHeight: '28px' }}>{prettyName(key)}</div>
            <div className="font-mono" style={{ color: '#f8fafc', fontSize: '17px', fontWeight: 700, overflowWrap: 'anywhere' }}>{Number(value).toLocaleString(undefined, { maximumFractionDigits: 3 })}</div>
          </div>
        ))}
      </div>
      <p style={{ color: 'var(--text-dim)', fontSize: '11px', margin: '14px 0 0' }}>
        Scenario values are representative training records selected because the fitted models recognize the intended scenario. They are demo examples, not live vessel readings.
      </p>
    </section>
  );
}
