import React, { useState, useEffect } from 'react';
import api from '../api';
import { Upload, AlertTriangle, CheckCircle } from 'lucide-react';

const SatelliteView = () => {
    const [images, setImages] = useState([]);
    const [uploading, setUploading] = useState(false);

    const fetchImages = async () => {
        try {
            const res = await api.get('satellite/');
            setImages(res.data);
        } catch (err) {
            console.error("Error fetching images", err);
        }
    };

    useEffect(() => {
        fetchImages();
    }, []);

    const handleUpload = async (e) => {
        const file = e.target.files[0];
        if (!file) return;

        const formData = new FormData();
        formData.append('image', file);
        formData.append('location_name', 'Simulated Region ' + Math.floor(Math.random() * 100));

        setUploading(true);
        try {
            await api.post('satellite/', formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });
            fetchImages();
        } catch (err) {
            console.error("Upload failed", err);
            alert("Upload failed");
        } finally {
            setUploading(false);
        }
    };

    return (
        <div className="space-y-6">
            <header>
                <h2 className="text-3xl font-bold bg-gradient-to-r from-green-400 to-emerald-500 bg-clip-text text-transparent">
                    Satellite Imagery Analysis
                </h2>
                <p className="text-slate-400">Layer 1: Optical Detection of Turbidity & Chlorophyll</p>
            </header>

            {/* Fetch Live Data Section (Sentinel Hub) */}
            <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-6">
                <h3 className="text-lg font-semibold text-white mb-2 flex items-center gap-2">
                    <span className="p-1 bg-purple-500/20 rounded text-purple-400"><Upload size={16} /></span>
                    Fetch Live Sentinel-2 Data
                </h3>
                <div className="flex gap-4 items-end">
                    <div>
                        <label className="block text-xs text-slate-400 mb-1">Region Name</label>
                        <input type="text" placeholder="e.g. Ganges Delta" className="bg-slate-950 border border-slate-700 rounded p-2 text-sm text-white w-48" id="fetch-name" />
                    </div>
                    <div>
                        <label className="block text-xs text-slate-400 mb-1">Latitude</label>
                        <input type="number" placeholder="22.57" className="bg-slate-950 border border-slate-700 rounded p-2 text-sm text-white w-24" id="fetch-lat" />
                    </div>
                    <div>
                        <label className="block text-xs text-slate-400 mb-1">Longitude</label>
                        <input type="number" placeholder="88.36" className="bg-slate-950 border border-slate-700 rounded p-2 text-sm text-white w-24" id="fetch-lon" />
                    </div>
                    <button 
                        onClick={async () => {
                            const name = document.getElementById('fetch-name').value;
                            const lat = document.getElementById('fetch-lat').value;
                            const lon = document.getElementById('fetch-lon').value;
                            if(!lat || !lon) return alert("Please enter coordinates");
                            
                            setUploading(true);
                            try {
                                await api.post('satellite/fetch_live/', { location_name: name, lat, lon });
                                fetchImages();
                            } catch (err) {
                                alert("Fetch failed. Ensure Sentinel API Keys are set in backend.");
                            } finally {
                                setUploading(false);
                            }
                        }}
                        className="bg-purple-600 hover:bg-purple-500 text-white px-4 py-2 rounded-lg text-sm font-semibold transition-colors h-10"
                    >
                        Fetch Satellite Feed
                    </button>
                </div>
            </div>

            {/* Upload Section */}
            <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-8 text-center hover:border-blue-500/50 transition-colors border-dashed">
                <input 
                    type="file" 
                    id="sat-upload" 
                    className="hidden" 
                    accept="image/*"
                    onChange={handleUpload}
                />
                <label htmlFor="sat-upload" className="cursor-pointer flex flex-col items-center gap-4">
                    <div className="p-4 bg-blue-600/20 rounded-full text-blue-400">
                        <Upload size={32} />
                    </div>
                    <div className="space-y-1">
                        <h3 className="text-lg font-semibold text-white">Upload Satellite Feed</h3>
                        <p className="text-sm text-slate-400">Supports JPEG, PNG (Simulated Input)</p>
                    </div>
                    {uploading && <p className="text-blue-400 animate-pulse">Processing Image (OpenCV)...</p>}
                </label>
            </div>

            {/* Results Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {images.map((img) => (
                    <div key={img.id} className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-lg hover:shadow-blue-900/20 transition-all">
                        <div className="h-48 overflow-hidden relative group">
                            <img 
                                src={`http://127.0.0.1:8000${img.image}`} 
                                alt="Satellite Scan" 
                                className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                            />
                            <div className="absolute top-2 right-2 bg-black/70 backdrop-blur-md px-2 py-1 rounded text-xs text-white">
                                {new Date(img.captured_at).toLocaleDateString()}
                            </div>
                        </div>
                        <div className="p-4 space-y-4">
                            <div className="flex justify-between items-start">
                                <h3 className="font-semibold text-white">{img.location_name}</h3>
                                {img.risk_score > 50 ? (
                                    <span className="text-red-400 flex items-center text-xs gap-1 font-bold">
                                        <AlertTriangle size={12} /> HIGH RISK
                                    </span>
                                ) : (
                                    <span className="text-green-400 flex items-center text-xs gap-1 font-bold">
                                        <CheckCircle size={12} /> SAFE
                                    </span>
                                )}
                            </div>
                            
                            <div className="grid grid-cols-2 gap-2 text-sm">
                                <div className="bg-slate-800 p-2 rounded">
                                    <span className="block text-slate-500 text-xs">Chlorophyll</span>
                                    <span className={`font-mono font-bold ${img.chlorophyll_index > 30 ? 'text-yellow-400' : 'text-white'}`}>
                                        {img.chlorophyll_index}%
                                    </span>
                                </div>
                                <div className="bg-slate-800 p-2 rounded">
                                    <span className="block text-slate-500 text-xs">Turbidity</span>
                                    <span className={`font-mono font-bold ${img.turbidity_index > 30 ? 'text-orange-400' : 'text-white'}`}>
                                        {img.turbidity_index}%
                                    </span>
                                </div>
                            </div>

                            <div className="border-t border-slate-800 pt-3">
                                <div className="flex justify-between items-center">
                                    <span className="text-xs text-slate-400">Risk Score</span>
                                    <div className="flex-1 mx-3 h-2 bg-slate-700 rounded-full overflow-hidden">
                                        <div 
                                            className={`h-full rounded-full ${img.risk_score > 50 ? 'bg-red-500' : 'bg-green-500'}`} 
                                            style={{ width: `${img.risk_score}%` }}
                                        />
                                    </div>
                                    <span className="text-xs font-bold text-white">{img.risk_score}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                ))}
                
                {images.length === 0 && (
                    <div className="col-span-full py-12 text-center text-slate-500">
                        No scans available. Upload an image to start analysis.
                    </div>
                )}
            </div>
        </div>
    );
};

export default SatelliteView;
