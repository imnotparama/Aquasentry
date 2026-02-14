import React, { useState, useEffect } from 'react';
import api from '../api';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { Activity, Clock } from 'lucide-react';

const IoTSensors = () => {
    const [sensors, setSensors] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const res = await api.get('sensors/');
                setSensors(res.data);
            } catch (err) {
                console.error("Error fetching sensor data", err);
            }
        };

        fetchData();
        const interval = setInterval(fetchData, 5000); // Poll every 5 seconds
        return () => clearInterval(interval);
    }, []);

    const recentData = sensors.slice(0, 20).reverse(); // Show last 20 readings

    return (
        <div className="space-y-6">
            <header className="flex justify-between items-end">
                <div>
                    <h2 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-cyan-500 bg-clip-text text-transparent">
                        IoT Sensor Network
                    </h2>
                    <p className="text-slate-400">Layer 2: Real-time Water Quality Monitoring</p>
                </div>
                <div className="flex items-center text-xs text-green-400 gap-2 bg-green-900/20 px-3 py-1 rounded-full border border-green-800">
                    <span className="relative flex h-2 w-2">
                      <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                      <span className="relative inline-flex rounded-full h-2 w-2 bg-green-500"></span>
                    </span>
                    Live Stream Active
                </div>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* pH Chart */}
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-lg">
                    <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                        <Activity size={18} className="text-blue-400" /> pH Level Stream
                    </h3>
                    <div className="h-64">
                        <ResponsiveContainer width="100%" height="100%">
                            <LineChart data={recentData}>
                                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                                <XAxis dataKey="timestamp" tick={false} />
                                <YAxis domain={[0, 14]} stroke="#9ca3af" />
                                <Tooltip contentStyle={{ backgroundColor: '#1f2937', border: 'none' }} />
                                <Line type="monotone" dataKey="ph" stroke="#3b82f6" strokeWidth={2} dot={false} />
                            </LineChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                {/* Turbidity Chart */}
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-lg">
                    <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                        <Activity size={18} className="text-orange-400" /> Turbidity Stream (NTU)
                    </h3>
                    <div className="h-64">
                         <ResponsiveContainer width="100%" height="100%">
                            <LineChart data={recentData}>
                                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                                <XAxis dataKey="timestamp" tick={false} />
                                <YAxis domain={[0, 10]} stroke="#9ca3af" />
                                <Tooltip contentStyle={{ backgroundColor: '#1f2937', border: 'none' }} />
                                <Line type="monotone" dataKey="turbidity" stroke="#f97316" strokeWidth={2} dot={false} />
                            </LineChart>
                        </ResponsiveContainer>
                    </div>
                </div>
            </div>

            {/* Recent Readings Table */}
            <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
                <div className="p-4 border-b border-slate-800 flex items-center gap-2">
                    <Clock size={16} className="text-slate-400" />
                    <h3 className="font-semibold text-white">Recent Data Packets</h3>
                </div>
                <div className="overflow-x-auto">
                    <table className="w-full text-sm text-left text-slate-400">
                        <thead className="text-xs text-slate-500 uppercase bg-slate-950">
                            <tr>
                                <th className="px-6 py-3">Timestamp</th>
                                <th className="px-6 py-3">Sensor ID</th>
                                <th className="px-6 py-3">pH</th>
                                <th className="px-6 py-3">Turbidity</th>
                                <th className="px-6 py-3">DO (mg/L)</th>
                                <th className="px-6 py-3">TDS (ppm)</th>
                            </tr>
                        </thead>
                        <tbody>
                            {recentData.map((reading) => (
                                <tr key={reading.id} className="border-b border-slate-800 hover:bg-slate-800/50">
                                    <td className="px-6 py-4">{new Date(reading.timestamp).toLocaleTimeString()}</td>
                                    <td className="px-6 py-4 font-mono text-blue-400">{reading.sensor_id}</td>
                                    <td className="px-6 py-4">{reading.ph.toFixed(2)}</td>
                                    <td className="px-6 py-4">{reading.turbidity.toFixed(2)}</td>
                                    <td className="px-6 py-4">{reading.dissolved_oxygen.toFixed(2)}</td>
                                    <td className="px-6 py-4">{reading.conductivity.toFixed(0)}</td>
                                </tr>
                            ))}
                            {recentData.length === 0 && (
                                <tr>
                                    <td colSpan="6" className="px-6 py-4 text-center">No sensor data available.</td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
};

export default IoTSensors;
