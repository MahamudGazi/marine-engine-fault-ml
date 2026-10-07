import React, { useState, useEffect } from 'react';
import { Activity, Anchor, Cpu, RefreshCw, ShieldAlert, Wifi } from 'lucide-react';

export default function Header({ isOnline, onRefresh }) {
  const [time, setTime] = useState(new Date().toUTCString());

  useEffect(() => {
    const timer = setInterval(() => {
      // setTime(new Date().toUTCString());
      setTime(new Date().toLocaleString('en-US', { timeZone: 'Asia/Dhaka' }));
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  return (
    <header className="glass-panel" style={{ padding: '16px', marginBottom: '20px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '14px' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px', minWidth: '260px', flex: '1 1 300px' }}>
        <div style={{ 
          width: '42px', 
          height: '42px', 
          minWidth: '42px',
          borderRadius: '10px', 
          background: 'linear-gradient(135deg, #00f2fe 0%, #4facfe 100%)', 
          display: 'flex', 
          alignItems: 'center', 
          justifyContent: 'center',
          boxShadow: '0 0 20px rgba(0, 242, 254, 0.4)'
        }}>
          <Anchor size={22} color="#090d14" />
        </div>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexWrap: 'wrap' }}>
            <h1 className="font-hud glow-primary hud-title" style={{ fontSize: '18px', letterSpacing: '0.5px', fontWeight: 700, color: '#00f2fe' }}>
              M/V PACIFIC TITAN
            </h1>
            <span style={{ fontSize: '10px', background: 'rgba(0, 242, 254, 0.12)', color: '#00f2fe', padding: '2px 6px', borderRadius: '4px', border: '1px solid rgba(0, 242, 254, 0.3)', fontFamily: 'var(--font-hud)' }}>
              UNIT #1 (MAN B&W)
            </span>
          </div>
          <p style={{ fontSize: '12px', color: 'var(--text-muted)', marginTop: '2px' }}>
            Autonomous Marine Diesel Diagnostics & Explainable AI (SHAP)
          </p>
        </div>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '14px', flexWrap: 'wrap', justifyContent: 'space-between' }}>
        <div>
          <div className="font-mono" style={{ fontSize: '11px', color: '#cbd5e1' }}>{time}</div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginTop: '2px' }}>
            <span style={{ 
              width: '8px', 
              height: '8px', 
              borderRadius: '50%', 
              background: isOnline ? '#10b981' : '#ef4444',
              boxShadow: isOnline ? '0 0 8px #10b981' : '0 0 8px #ef4444'
            }}></span>
            <span className="font-hud" style={{ fontSize: '10px', color: isOnline ? '#10b981' : '#ef4444', textTransform: 'uppercase' }}>
              {isOnline ? 'TELEMETRY ACTIVE' : 'RECONNECTING'}
            </span>
          </div>
        </div>

        <button onClick={onRefresh} className="btn-cyber" style={{ padding: '6px 12px', fontSize: '12px' }} title="Refresh Live State">
          <RefreshCw size={14} />
          <span>Sync</span>
        </button>
      </div>
    </header>
  );
}
