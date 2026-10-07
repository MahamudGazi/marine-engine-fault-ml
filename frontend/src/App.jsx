import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import EngineStatusHUD from './components/EngineStatusHUD';
import SensorGauges from './components/SensorGauges';
import ShapExplainerChart from './components/ShapExplainerChart';
import ScenarioControls from './components/ScenarioControls';
import PredictionHistoryTable from './components/PredictionHistoryTable';
import { predictFault, simulateTelemetry, fetchPredictionHistory, clearPredictionHistory } from './services/api';

export default function App() {
  const [telemetry, setTelemetry] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [isOnline, setIsOnline] = useState(true);
  const [currentScenario, setCurrentScenario] = useState('normal');

  // Trigger prediction pipeline given telemetry
  const runDiagnosis = async (telemetryData, scenarioId = 'normal') => {
    setLoading(true);
    try {
      const predResult = await predictFault(telemetryData);
      setPrediction(predResult);
      setIsOnline(true);
      setCurrentScenario(scenarioId);
      
      // Update history
      const historyList = await fetchPredictionHistory(15);
      setHistory(historyList);
    } catch (err) {
      console.error('Diagnosis Error:', err);
      setIsOnline(false);
    } finally {
      setLoading(false);
    }
  };

  // Handle scenario switch
  const handleSelectScenario = async (scenarioId) => {
    try {
      const simData = await simulateTelemetry(scenarioId);
      setTelemetry(simData);
      await runDiagnosis(simData, scenarioId);
    } catch (err) {
      console.error('Simulation Error:', err);
    }
  };

  // Initial load
  useEffect(() => {
    handleSelectScenario('normal');
  }, []);

  const handleClearHistory = async () => {
    try {
      await clearPredictionHistory();
      setHistory([]);
    } catch (err) {
      console.error('Clear history error:', err);
    }
  };

  return (
    <div style={{ maxWidth: '1440px', margin: '0 auto', padding: '24px 20px', minHeight: '100vh' }}>
      {/* 1. Nav & Ship HUD Header */}
      <Header isOnline={isOnline} onRefresh={() => handleSelectScenario(currentScenario)} />

      <main style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
        
        {/* 2. Top Engine Status Banner */}
        <EngineStatusHUD prediction={prediction} loading={loading} />

        {/* 3. Scenario Injector / Testing Controls */}
        <ScenarioControls 
          onSelectScenario={handleSelectScenario} 
          loading={loading} 
          currentScenario={currentScenario} 
        />

        {/* 4. Live Sensor Gauges & Cylinder Balance */}
        <SensorGauges telemetry={telemetry} />

        {/* 5. Explainable AI SHAP Attribution */}
        {prediction && (
          <ShapExplainerChart 
            shapExplanations={prediction.shap_explanations} 
            faultName={prediction.fault_name} 
          />
        )}

        {/* 6. Historical Diagnostic Logs */}
        <PredictionHistoryTable 
          history={history} 
          onClearHistory={handleClearHistory} 
          loading={loading} 
        />

      </main>

      <footer style={{ marginTop: '40px', textAlign: 'center', color: 'var(--text-dim)', fontSize: '12px', borderTop: '1px solid rgba(255, 255, 255, 0.05)', paddingTop: '20px' }}>
        Marine Engine Fault Detection & XAI System • Machine Learning + Mechanical Engineering + Django REST + React
      </footer>
    </div>
  );
}
