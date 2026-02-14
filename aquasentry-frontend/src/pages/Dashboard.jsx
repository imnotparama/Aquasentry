import React from 'react';
import { ShieldCheck, AlertOctagon, Activity, Users } from 'lucide-react';
import { Link } from 'react-router-dom';

const Dashboard = () => {
    // In a real app, these would be fetched from the 'Risk Engine' API
    const systemStatus = {
        overallRisk: 'LOW',
        satelliteAlerts: 0,
        sensorAnomalies: 2,
        healthReports: 5
    };

    return (
        <div className="space-y-8">
            <header className="mb-8">
                <h1 className="text-4xl font-bold text-white mb-2">System Overview</h1>
                <p className="text-slate-400">Executive Summary of Water Quality Risks</p>
            </header>

            {/* Hero Card */}
            <div className="bg-gradient-to-r from-blue-900/40 to-indigo-900/40 border border-blue-800/50 rounded-2xl p-8 relative overflow-hidden">
                <div className="absolute top-0 right-0 p-8 opacity-10">
                    <ShieldCheck size={200} />
                </div>
                <div className="relative z-10">
                    <h2 className="text-xl font-semibold text-blue-200 uppercase tracking-widest mb-1">Current Threat Level</h2>
                    <div className="flex items-end gap-4">
                        <span className="text-6xl font-black text-white">{systemStatus.overallRisk}</span>
                        <span className="text-green-400 font-bold mb-2 flex items-center gap-1">
                            <ShieldCheck size={20} /> Systems Nominal
                        </span>
                    </div>
                    <p className="mt-4 text-slate-300 max-w-xl">
                        The Predictive Risk Engine has analyzed data from Satellite Imagery (Layer 1), IoT Sensors (Layer 2), and Health Reports (Layer 3). No critical threats detected in the last hour.
                    </p>
                </div>
            </div>

            {/* 3-Layer Grid */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <Link to="/satellite" className="bg-slate-900 border border-slate-800 p-6 rounded-xl hover:bg-slate-800 transition-colors group">
                    <div className="flex justify-between items-start mb-4">
                        <div className="p-3 bg-green-900/30 text-green-400 rounded-lg">
                            <Activity size={24} />
                        </div>
                        <span className="text-xs font-mono text-slate-500">LAYER 1</span>
                    </div>
                    <h3 className="text-xl font-bold text-white mb-1 group-hover:text-blue-400 transition-colors">Satellite Intelligence</h3>
                    <p className="text-sm text-slate-400 mb-4">Optical analysis of turbidity & algae.</p>
                    <div className="text-2xl font-bold text-white">0 <span className="text-sm font-normal text-slate-500">Active Alerts</span></div>
                </Link>

                <Link to="/sensors" className="bg-slate-900 border border-slate-800 p-6 rounded-xl hover:bg-slate-800 transition-colors group">
                    <div className="flex justify-between items-start mb-4">
                        <div className="p-3 bg-orange-900/30 text-orange-400 rounded-lg">
                            <Activity size={24} />
                        </div>
                        <span className="text-xs font-mono text-slate-500">LAYER 2</span>
                    </div>
                    <h3 className="text-xl font-bold text-white mb-1 group-hover:text-blue-400 transition-colors">IoT Sensor Grid</h3>
                    <p className="text-sm text-slate-400 mb-4">Real-time chemical monitoring.</p>
                    <div className="text-2xl font-bold text-white">{systemStatus.sensorAnomalies} <span className="text-sm font-normal text-slate-500">Anomalies Detected</span></div>
                </Link>

                <Link to="/health" className="bg-slate-900 border border-slate-800 p-6 rounded-xl hover:bg-slate-800 transition-colors group">
                    <div className="flex justify-between items-start mb-4">
                        <div className="p-3 bg-pink-900/30 text-pink-400 rounded-lg">
                            <Users size={24} />
                        </div>
                        <span className="text-xs font-mono text-slate-500">LAYER 3</span>
                    </div>
                    <h3 className="text-xl font-bold text-white mb-1 group-hover:text-blue-400 transition-colors">Population Health</h3>
                    <p className="text-sm text-slate-400 mb-4">Symptom reporting & analysis.</p>
                    <div className="text-2xl font-bold text-white">{systemStatus.healthReports} <span className="text-sm font-normal text-slate-500">Reports Today</span></div>
                </Link>
            </div>
        </div>
    );
};

export default Dashboard;
