import React from 'react';
import { History, Trash2, CheckCircle2, AlertTriangle } from 'lucide-react';

export default function PredictionHistoryTable({ history, onClearHistory, loading }) {
  return (
    <div className="glass-panel" style={{ padding: '20px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <History size={18} color="#00f2fe" />
          <h3 className="font-hud glow-primary" style={{ fontSize: '15px', color: '#00f2fe', letterSpacing: '0.5px' }}>
            TELEMETRY DIAGNOSTIC EVENT LOG
          </h3>
        </div>

        {history.length > 0 && (
          <button onClick={onClearHistory} className="btn-danger-cyber" style={{ fontSize: '12px', display: 'flex', alignItems: 'center', gap: '6px' }}>
            <Trash2 size={13} />
            <span>Clear Logs</span>
          </button>
        )}
      </div>

      {history.length === 0 ? (
        <div style={{ textAlign: 'center', padding: '24px', color: 'var(--text-dim)', fontSize: '13px' }}>
          No diagnosis events recorded in current session.
        </div>
      ) : (
        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '12px' }}>
            <thead>
              <tr style={{ borderBottom: '1px solid rgba(255, 255, 255, 0.08)', color: 'var(--text-dim)', textAlign: 'left', fontFamily: 'var(--font-hud)' }}>
                <th style={{ padding: '8px 12px' }}>TIMESTAMP (UTC)</th>
                <th style={{ padding: '8px 12px' }}>STATUS</th>
                <th style={{ padding: '8px 12px' }}>DIAGNOSED FAULT</th>
                <th style={{ padding: '8px 12px' }}>CONFIDENCE</th>
                <th style={{ padding: '8px 12px' }}>ENGINE SPEED / BRAKE WEIGHT</th>
                <th style={{ padding: '8px 12px' }}>TURBINE INLET TEMP.</th>
                <th style={{ padding: '8px 12px' }}>CHARGE AIR PRESS.</th>
              </tr>
            </thead>
            <tbody>
              {history.map((row) => {
                const isCrit = row.is_anomaly;
                const badgeBg = isCrit ? 'rgba(239, 68, 68, 0.15)' : 'rgba(16, 185, 129, 0.15)';
                const badgeColor = isCrit ? '#ef4444' : '#10b981';

                return (
                  <tr key={row.id} style={{ borderBottom: '1px solid rgba(255, 255, 255, 0.04)' }}>
                    <td className="font-mono" style={{ padding: '10px 12px', color: '#94a3b8' }}>
                      {row.timestamp_formatted || row.timestamp?.slice(11, 19)}
                    </td>
                    <td style={{ padding: '10px 12px' }}>
                      <span style={{ 
                        background: badgeBg, 
                        color: badgeColor, 
                        padding: '2px 8px', 
                        borderRadius: '4px',
                        fontFamily: 'var(--font-hud)',
                        fontWeight: 600,
                        fontSize: '11px',
                        display: 'inline-flex',
                        alignItems: 'center',
                        gap: '4px'
                      }}>
                        {isCrit ? <AlertTriangle size={12} /> : <CheckCircle2 size={12} />}
                        {isCrit ? 'ANOMALY' : 'NORMAL'}
                      </span>
                    </td>
                    <td style={{ padding: '10px 12px', color: '#f1f5f9', fontWeight: 500 }}>
                      {row.fault_name}
                    </td>
                    <td className="font-mono" style={{ padding: '10px 12px', color: '#00f2fe' }}>
                      {row.confidence_pct?.toFixed(1)}%
                    </td>
                    <td className="font-mono" style={{ padding: '10px 12px', color: '#cbd5e1' }}>
                      {row.engine_speed_rpm?.toFixed(0)} RPM / {row.engine_load_pct?.toFixed(2)}
                    </td>
                    <td className="font-mono" style={{ padding: '10px 12px', color: '#cbd5e1' }}>
                      {row.exhaust_temp_inlet_c?.toFixed(1)} °C
                    </td>
                    <td className="font-mono" style={{ padding: '10px 12px', color: '#cbd5e1' }}>
                      {row.scavenge_air_press_bar?.toFixed(3)}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
