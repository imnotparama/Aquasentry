import React from 'react';
import { NavLink } from 'react-router-dom';
import { Satellite, Activity, Stethoscope, LayoutDashboard } from 'lucide-react';

const Sidebar = () => {
  const navItems = [
    { name: 'Dashboard', path: '/', icon: <LayoutDashboard size={20} /> },
    { name: 'Satellite Monitor', path: '/satellite', icon: <Satellite size={20} /> },
    { name: 'IoT Sensor Network', path: '/sensors', icon: <Activity size={20} /> },
    { name: 'Health Reporting', path: '/health', icon: <Stethoscope size={20} /> },
  ];

  return (
    <div className="h-screen w-64 bg-slate-900 text-white flex flex-col fixed left-0 top-0 overflow-y-auto">
      <div className="p-6 border-b border-slate-800">
        <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-cyan-300 bg-clip-text text-transparent">
          AquaSentry
        </h1>
        <p className="text-xs text-slate-400 mt-1">Smart Water Monitoring</p>
      </div>
      
      <nav className="flex-1 p-4 space-y-2">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `flex items-center space-x-3 px-4 py-3 rounded-lg transition-all duration-200 ${
                isActive
                  ? 'bg-blue-600 shadow-lg shadow-blue-900/50 text-white'
                  : 'text-slate-400 hover:bg-slate-800 hover:text-white'
              }`
            }
          >
            {item.icon}
            <span className="font-medium">{item.name}</span>
          </NavLink>
        ))}
      </nav>

      <div className="p-4 border-t border-slate-800">
        <div className="bg-slate-800/50 rounded-lg p-3 text-xs text-slate-500">
          <p>System Status: <span className="text-green-400 font-bold">Online</span></p>
          <p className="mt-1">v2.0 Patent-Ready</p>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
