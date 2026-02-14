import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import SatelliteView from './pages/SatelliteView';
import IoTSensors from './pages/IoTSensors';
import HealthReports from './pages/HealthReports';

function App() {
  return (
    <Router>
      <div className="flex bg-slate-950 min-h-screen text-slate-100 font-sans">
        <Sidebar />
        <main className="flex-1 ml-64 p-8 overflow-y-auto">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/satellite" element={<SatelliteView />} />
            <Route path="/sensors" element={<IoTSensors />} />
            <Route path="/health" element={<HealthReports />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
