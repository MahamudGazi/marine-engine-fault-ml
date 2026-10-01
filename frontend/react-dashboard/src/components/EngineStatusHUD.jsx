import React from 'react';
import { AlertTriangle, CheckCircle2, ShieldAlert, Cpu, Gauge, Zap } from 'lucide-react';

export default function EngineStatusHUD({ prediction, loading }) {
  if (!prediction) {
    return (
      <div className="glass-panel" style={{ padding: '24px', textAlign: 'center', color: 'var(--text-muted)' }}>
        Awaiting telemetry stream initialization...
      </div>
    );
  }

  const { is_anomaly, fault_name, confidence_pct, class_probabilities, anomaly_probability } = prediction;

  const isCritical = is_anomaly;
  const statusColor = isCritical ? '#ef4444' : '#10b981';
  const statusGlow = isCritical ? 'glow-danger' : 'glow-success';

  return (
    <div className="glass-panel" style={{ 
      padding: '24px', 
      borderLeft: `4px solid ${statusColor}`,
      position: 'relative',
      overflow: 'hidden'
    }}>
      {/* Background ambient gradient */}
      <div style={{
        position: 'absolute',
        top: 0,
        right: 0,
        width: '280px',
        height: '100%',
        background: `radial-gradient(circle at top right, ${isCritical ? 'rgba(239, 68, 68, 0.12)' : 'rgba(16, 185, 129, 0.12)'} 0%, transparent 70%)`,
        pointerEvents: 'none'
      }} />

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '24px', alignItems: 'center' }}>
        
        {/* Left Status Banner */}
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '8px' }}>
            <div style={{
              width: '14px',
              height: '14px',
              borderRadius: '50%',
              backgroundColor: statusColor,
              boxShadow: `0 0 12px ${statusColor}`
            }} className="animate-pulse-glow" />
            <span className="font-hud" style={{ fontSize: '12px', letterSpacing: '1.5px', color: statusColor, textTransform: 'uppercase', fontWeight: 600 }}>
              {isCritical ? 'CRITICAL ANOMALY DETECTED' : 'SYSTEM NOMINAL / ALL CLEAR'}
            </span>
          </div>

          <div className={`font-hud ${statusGlow}`} style={{ fontSize: '28px', fontWeight: 700, color: statusColor, letterSpacing: '0.5px' }}>
            {fault_name}
          </div>

          <p style={{ fontSize: '13px', color: 'var(--text-muted)', marginTop: '6px' }}>
            {isCritical 
              ? 'Immediate corrective engineering action recommended to prevent mechanical trip or thermal damage.'
              : 'All mechanical and thermal combustion parameters are within standard maritime limits.'}
          </p>
        </div>

        {/* Confidence & Anomaly Score */}
        <div style={{ background: 'rgba(9, 13, 20, 0.6)', padding: '16px 20px', borderRadius: '10px', border: '1px solid rgba(255, 255, 255, 0.05)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
            <span className="font-hud" style={{ fontSize: '13px', color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: '6px' }}>
              <Zap size={15} color="#00f2fe" /> AI DIAGNOSIS CONFIDENCE
            </span>
            <span className="font-mono" style={{ fontSize: '18px', fontWeight: 700, color: '#00f2fe' }}>
              {confidence_pct?.toFixed(1)}%
            </span>
          </div>

          <div style={{ width: '100%', height: '8px', background: 'rgba(255, 255, 255, 0.1)', borderRadius: '4px', overflow: 'hidden' }}>
            <div style={{
              width: `${confidence_pct || 0}%`,
              height: '100%',
              background: 'linear-gradient(90deg, #00f2fe 0%, #4facfe 100%)',
              boxShadow: '0 0 10px rgba(0, 242, 254, 0.6)',
              transition: 'width 0.4s ease'
            }} />
          </div>

          <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '14px', fontSize: '12px', color: 'var(--text-dim)' }}>
            <span>Anomaly Probability: <strong style={{ color: isCritical ? '#ef4444' : '#10b981' }}>{anomaly_probability || (is_anomaly ? 99.8 : 0.2)}%</strong></span>
            <span>Latency: <strong style={{ color: '#00f2fe' }}>~12ms</strong></span>
          </div>
        </div>

        {/* Probabilities Distribution */}
        <div>
          <div className="font-hud" style={{ fontSize: '11px', color: 'var(--text-dim)', letterSpacing: '1px', textTransform: 'uppercase', marginBottom: '8px' }}>
            CLASSIFIER PROBABILITY SPECTRUM
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
            {class_probabilities && Object.entries(class_probabilities).map(([clsName, prob]) => {
              const isTop = clsName === fault_name;
              return (
                <div key={clsName} style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', fontSize: '11px' }}>
                  <span style={{ color: isTop ? '#00f2fe' : 'var(--text-muted)', fontWeight: isTop ? 600 : 400, maxWidth: '180px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                    {clsName}
                  </span>
                  <span className="font-mono" style={{ color: isTop ? '#00f2fe' : 'var(--text-dim)', fontWeight: isTop ? 700 : 400 }}>
                    {prob}%
                  </span>
                </div>
              );
            })}
          </div>
        </div>

      </div>
    </div>
  );
}
