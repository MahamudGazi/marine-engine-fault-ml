import React from 'react';
import { HelpCircle, Sparkles, TrendingUp, TrendingDown, Info } from 'lucide-react';

export default function ShapExplainerChart({ shapExplanations, faultName }) {
  if (!shapExplanations || shapExplanations.length === 0) {
    return (
      <div className="glass-panel" style={{ padding: '20px', textAlign: 'center', color: 'var(--text-muted)' }}>
        No SHAP attribution data available.
      </div>
    );
  }

  // Find maximum absolute shap value for relative scaling
  const maxShap = Math.max(...shapExplanations.map(s => Math.abs(s.shap_value)), 0.01);

  return (
    <div className="glass-panel" style={{ padding: '24px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '18px', flexWrap: 'wrap', gap: '10px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <Sparkles size={20} color="#00f2fe" />
          <h3 className="font-hud glow-primary" style={{ fontSize: '16px', color: '#00f2fe', letterSpacing: '0.5px' }}>
            AI REASONING & EXPLAINABILITY (SHAP WATERFALL ATTRIBUTION)
          </h3>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px', fontSize: '11px', fontFamily: 'var(--font-hud)' }}>
          <span style={{ display: 'flex', alignItems: 'center', gap: '4px', color: '#ef4444' }}>
            <span style={{ width: '8px', height: '8px', borderRadius: '2px', background: '#ef4444' }}></span>
            + PUSHING TOWARD FAULT
          </span>
          <span style={{ display: 'flex', alignItems: 'center', gap: '4px', color: '#10b981' }}>
            <span style={{ width: '8px', height: '8px', borderRadius: '2px', background: '#10b981' }}></span>
            - STABILIZING / NORMALIZING
          </span>
        </div>
      </div>

      <p style={{ fontSize: '13px', color: 'var(--text-muted)', marginBottom: '16px' }}>
        The SHAP (SHapley Additive exPlanations) engine extracts the exact mechanical and thermal sensor drivers influencing the current diagnosis: <strong style={{ color: '#00f2fe' }}>{faultName}</strong>.
      </p>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
        {shapExplanations.map((item, idx) => {
          const isRisk = item.shap_value > 0;
          const barPct = Math.min((Math.abs(item.shap_value) / maxShap) * 100, 100);
          const barColor = isRisk ? '#ef4444' : '#10b981';

          return (
            <div key={idx} style={{ 
              background: 'rgba(9, 13, 20, 0.5)', 
              padding: '12px 16px', 
              borderRadius: '8px', 
              border: '1px solid rgba(255, 255, 255, 0.05)',
              display: 'grid',
              gridTemplateColumns: '220px 100px 1fr 90px',
              alignItems: 'center',
              gap: '16px'
            }}>
              {/* Feature Name */}
              <div>
                <div className="font-hud" style={{ fontSize: '13px', color: '#e2e8f0', fontWeight: 600 }}>
                  {item.feature.replace(/_/g, ' ').toUpperCase()}
                </div>
                <div style={{ fontSize: '11px', color: 'var(--text-dim)' }}>
                  Rank #{idx + 1} Driver
                </div>
              </div>

              {/* Observed Value */}
              <div className="font-mono" style={{ fontSize: '13px', color: '#00f2fe', background: 'rgba(0, 242, 254, 0.08)', padding: '4px 8px', borderRadius: '4px', textAlign: 'center' }}>
                {item.value}
              </div>

              {/* SHAP Bar */}
              <div style={{ display: 'flex', alignItems: 'center', height: '14px', background: 'rgba(255,255,255,0.05)', borderRadius: '4px', overflow: 'hidden', position: 'relative' }}>
                <div style={{
                  width: `${barPct}%`,
                  height: '100%',
                  background: isRisk 
                    ? 'linear-gradient(90deg, #f87171 0%, #ef4444 100%)' 
                    : 'linear-gradient(90deg, #34d399 0%, #10b981 100%)',
                  borderRadius: '4px',
                  boxShadow: `0 0 8px ${barColor}`,
                  transition: 'width 0.3s ease'
                }} />
              </div>

              {/* SHAP Value */}
              <div className="font-mono" style={{ fontSize: '12px', color: barColor, textAlign: 'right', fontWeight: 700 }}>
                {item.shap_value > 0 ? `+${item.shap_value.toFixed(4)}` : item.shap_value.toFixed(4)}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
