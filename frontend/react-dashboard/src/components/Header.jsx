import React, { useState, useEffect } from 'react';
import { Activity, Anchor, Cpu, RefreshCw, ShieldAlert, Wifi } from 'lucide-react';

export default function Header({ isOnline, onRefresh }) {
  const [time, setTime] = useState(new Date().toUTCString());

  useEffect(() => {
    const timer = setInterval(() => {
      setTime(new Date().toUTCString());
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  return (
    <header className="glass-panel" style={{ padding: '16px 24px', marginBottom: '24px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '16px' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
        <div style={{ 
          width: '46px', 
          height: '46px', 
          borderRadius: '10px', 
          background: 'linear-gradient(135deg, #00f2fe 0%, #4facfe 100%)', 
          display: 'flex', 
          alignItems: 'center', 
          justifyContent: 'center',
          boxShadow: '0 0 20px rgba(0, 242, 254, 0.4)'
        }}>
          <Anchor size={26} color="#090d14" />
        </div>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <h1 className="font-hud glow-primary" style={{ fontSize: '20px', letterSpacing: '1px', fontWeight: 700, color: '#00f2fe' }}>
              M/V PACIFIC TITAN — TELEMETRY & XAI HUD
            </h1>
            <span style={{ fontSize: '11px', background: 'rgba(0, 242, 254, 0.12)', color: '#00f2fe', padding: '2px 8px', borderRadius: '4px', border: '1px solid rgba(0, 242, 254, 0.3)', fontFamily: 'var(--font-hud)' }}>
              UNIT #1 (MAN B&W 6S50ME)
            </span>
          </div>
          <p style={{ fontSize: '13px', color: 'var(--text-muted)', marginTop: '2px' }}>
            Autonomous Marine Diesel Diagnostics & Explainable AI (SHAP TreeExplainer)
          </p>
        </div>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
        <div style={{ textAlign: 'right' }}>
          <div className="font-mono" style={{ fontSize: '13px', color: '#e2e8f0' }}>{time}</div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', justifyContent: 'flex-end', marginTop: '3px' }}>
            <span style={{ 
              width: '8px', 
              height: '8px', 
              borderRadius: '50%', 
              background: isOnline ? '#10b981' : '#ef4444',
              boxShadow: isOnline ? '0 0 8px #10b981' : '0 0 8px #ef4444'
            }}></span>
            <span className="font-hud" style={{ fontSize: '11px', color: isOnline ? '#10b981' : '#ef4444', textTransform: 'uppercase' }}>
              {isOnline ? 'TELEMETRY LINK ACTIVE' : 'API DISCONNECTED'}
            </span>
          </div>
        </div>

        <button onClick={onRefresh} className="btn-cyber" title="Refresh Live State">
          <RefreshCw size={15} />
          <span>Sync</span>
        </button>
      </div>
    </header>
  );
}
