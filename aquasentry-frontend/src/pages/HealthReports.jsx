import React, { useState } from 'react';
import api from '../api';
import { Send, MapPin, Stethoscope } from 'lucide-react';

const HealthReports = () => {
    const [formData, setFormData] = useState({
        symptom_type: 'GI',
        severity: 5,
        latitude: 0,
        longitude: 0,
        notes: ''
    });
    const [status, setStatus] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        setStatus('submitting');
        try {
            await api.post('health-reports/', formData);
            setStatus('success');
            setTimeout(() => setStatus(''), 3000);
        } catch (err) {
            console.error(err);
            setStatus('error');
        }
    };

    return (
        <div className="max-w-2xl mx-auto space-y-6">
            <header className="text-center">
                <h2 className="text-3xl font-bold bg-gradient-to-r from-pink-400 to-rose-500 bg-clip-text text-transparent">
                    Public Health Reporting
                </h2>
                <p className="text-slate-400">Layer 3: Community Health Symptoms Tracking</p>
            </header>

            <form onSubmit={handleSubmit} className="bg-slate-900 border border-slate-800 rounded-xl p-8 shadow-lg space-y-6">
                <div>
                    <label className="block text-sm font-medium text-slate-300 mb-2">Symptom Category</label>
                    <div className="grid grid-cols-2 gap-4">
                        {['GI', 'NEURO', 'DERM', 'OTHER'].map((type) => (
                            <button
                                key={type}
                                type="button"
                                onClick={() => setFormData({ ...formData, symptom_type: type })}
                                className={`p-4 rounded-lg border text-sm font-bold transition-all ${
                                    formData.symptom_type === type
                                        ? 'bg-blue-600 border-blue-500 text-white shadow-lg shadow-blue-900/50'
                                        : 'bg-slate-950 border-slate-800 text-slate-500 hover:border-slate-600'
                                }`}
                            >
                                {type === 'GI' && 'Gastrointestinal'}
                                {type === 'NEURO' && 'Neurological'}
                                {type === 'DERM' && 'Dermatological'}
                                {type === 'OTHER' && 'Other Symptoms'}
                            </button>
                        ))}
                    </div>
                </div>

                <div>
                    <label className="block text-sm font-medium text-slate-300 mb-2">Severity (1-10)</label>
                    <input
                        type="range"
                        min="1"
                        max="10"
                        value={formData.severity}
                        onChange={(e) => setFormData({ ...formData, severity: parseInt(e.target.value) })}
                        className="w-full h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-blue-500"
                    />
                    <div className="flex justify-between text-xs text-slate-500 mt-1">
                        <span>Mild</span>
                        <span className="text-white font-bold">{formData.severity}</span>
                        <span>Critical</span>
                    </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                    <div>
                        <label className="block text-sm font-medium text-slate-300 mb-2 flex items-center gap-1">
                            <MapPin size={14} /> Latitude
                        </label>
                        <input
                            type="number"
                            step="0.0001"
                            value={formData.latitude}
                            onChange={(e) => setFormData({ ...formData, latitude: parseFloat(e.target.value) })}
                            className="w-full bg-slate-950 border border-slate-800 rounded-lg p-3 text-white focus:ring-2 focus:ring-blue-500 focus:outline-none"
                        />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-slate-300 mb-2 flex items-center gap-1">
                            <MapPin size={14} /> Longitude
                        </label>
                        <input
                            type="number"
                            step="0.0001"
                            value={formData.longitude}
                            onChange={(e) => setFormData({ ...formData, longitude: parseFloat(e.target.value) })}
                            className="w-full bg-slate-950 border border-slate-800 rounded-lg p-3 text-white focus:ring-2 focus:ring-blue-500 focus:outline-none"
                        />
                    </div>
                </div>

                <div>
                    <label className="block text-sm font-medium text-slate-300 mb-2">Clinical Notes</label>
                    <textarea
                        rows="3"
                        value={formData.notes}
                        onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
                        className="w-full bg-slate-950 border border-slate-800 rounded-lg p-3 text-white focus:ring-2 focus:ring-blue-500 focus:outline-none"
                        placeholder="Describe specific symptoms..."
                    ></textarea>
                </div>

                <button
                    type="submit"
                    disabled={status === 'submitting'}
                    className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 hovered:from-blue-500 hovered:to-indigo-500 text-white font-bold py-4 rounded-xl shadow-lg shadow-blue-900/20 transition-all transform active:scale-95 flex justify-center items-center gap-2"
                >
                    {status === 'submitting' ? 'Submitting Report...' : <><Send size={18} /> Submit Health Report</>}
                </button>

                {status === 'success' && (
                    <div className="p-4 bg-green-900/20 border border-green-800 rounded-lg text-green-400 text-center animate-fade-in">
                        Report submitted successfully to the central database.
                    </div>
                )}
            </form>
        </div>
    );
};

export default HealthReports;
