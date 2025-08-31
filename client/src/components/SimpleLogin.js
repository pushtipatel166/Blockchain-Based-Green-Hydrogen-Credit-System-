import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const SimpleLogin = () => {
  const [selectedRole, setSelectedRole] = useState('buyer');
  const navigate = useNavigate();

  const handleDirectAccess = (role) => {
    const mockUser = {
      id: 1,
      username: 'demo_user',
      role: role,
      email: 'demo@example.com'
    };
    
    localStorage.setItem('user', JSON.stringify(mockUser));
    localStorage.setItem('token', 'bypass_token_12345');
    
    if (role === 'buyer') {
      navigate('/buyer-dashboard');
    } else if (role === 'NGO') {
      navigate('/ngo-dashboard');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100 flex items-center justify-center p-4">
      <div className="max-w-4xl w-full grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">
        
        {/* Left Side - Branding & Info */}
        <div className="text-center lg:text-left">
          <div className="mb-8">
            <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-emerald-500 to-teal-600 rounded-2xl shadow-2xl mb-6">
              <span className="text-white text-4xl">🌱</span>
            </div>
            <h1 className="text-5xl font-bold bg-gradient-to-r from-emerald-600 to-teal-700 bg-clip-text text-transparent mb-4">
              H₂Credits
            </h1>
            <p className="text-xl text-slate-600 leading-relaxed">
              The future of sustainable hydrogen credit trading
            </p>
          </div>
          
          <div className="space-y-4 text-slate-600">
            <div className="flex items-center space-x-3">
              <div className="w-2 h-2 bg-emerald-500 rounded-full"></div>
              <span>AI-powered verification system</span>
            </div>
            <div className="flex items-center space-x-3">
              <div className="w-2 h-2 bg-emerald-500 rounded-full"></div>
              <span>Blockchain-secured transactions</span>
            </div>
            <div className="flex items-center space-x-3">
              <div className="w-2 h-2 bg-emerald-500 rounded-full"></div>
              <span>Real-time market analytics</span>
            </div>
          </div>
        </div>

        {/* Right Side - Login Form */}
        <div className="bg-white/80 backdrop-blur-sm rounded-3xl shadow-2xl border border-white/20 p-8">
          <div className="text-center mb-8">
            <h2 className="text-3xl font-bold text-slate-800 mb-2">Welcome Back</h2>
            <p className="text-slate-600">Select your role to access the platform</p>
          </div>

          {/* Role Selection */}
          <div className="mb-8">
            <label className="block text-sm font-semibold text-slate-700 mb-4 text-left">
              Choose Your Role
            </label>
            <div className="grid grid-cols-2 gap-4">
              <button
                onClick={() => setSelectedRole('buyer')}
                className={`group relative p-6 rounded-2xl border-2 transition-all duration-300 ${
                  selectedRole === 'buyer'
                    ? 'border-emerald-500 bg-emerald-50 shadow-lg shadow-emerald-100'
                    : 'border-slate-200 hover:border-emerald-300 hover:shadow-md'
                }`}
              >
                <div className="text-center">
                  <div className={`text-3xl mb-3 transition-transform duration-300 ${
                    selectedRole === 'buyer' ? 'scale-110' : 'group-hover:scale-105'
                  }`}>
                    🛒
                  </div>
                  <div className="font-bold text-slate-800 mb-1">Buyer</div>
                  <div className="text-sm text-slate-500">Purchase & Trade Credits</div>
                </div>
                {selectedRole === 'buyer' && (
                  <div className="absolute -top-2 -right-2 w-6 h-6 bg-emerald-500 rounded-full flex items-center justify-center">
                    <svg className="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                  </div>
                )}
              </button>
              
              <button
                onClick={() => setSelectedRole('NGO')}
                className={`group relative p-6 rounded-2xl border-2 transition-all duration-300 ${
                  selectedRole === 'NGO'
                    ? 'border-blue-500 bg-blue-50 shadow-lg shadow-blue-100'
                    : 'border-slate-200 hover:border-blue-300 hover:shadow-md'
                }`}
              >
                <div className="text-center">
                  <div className={`text-3xl mb-3 transition-transform duration-300 ${
                    selectedRole === 'NGO' ? 'scale-110' : 'group-hover:scale-105'
                  }`}>
                    🏢
                  </div>
                  <div className="font-bold text-slate-800 mb-1">NGO</div>
                  <div className="text-sm text-slate-500">Create & Manage Credits</div>
                </div>
                {selectedRole === 'NGO' && (
                  <div className="absolute -top-2 -right-2 w-6 h-6 bg-blue-500 rounded-full flex items-center justify-center">
                    <svg className="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                  </div>
                )}
              </button>
            </div>
          </div>

          {/* Access Button */}
          <button
            onClick={() => handleDirectAccess(selectedRole)}
            className="w-full bg-gradient-to-r from-emerald-500 to-teal-600 text-white font-bold py-4 px-6 rounded-2xl hover:from-emerald-600 hover:to-teal-700 transition-all duration-300 transform hover:scale-[1.02] shadow-lg hover:shadow-xl mb-6 group"
          >
            <div className="flex items-center justify-center space-x-2">
              <span className="text-lg">Access Dashboard</span>
              <svg className="w-5 h-5 transition-transform duration-300 group-hover:translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </div>
          </button>

          {/* Quick Access Links */}
          <div className="grid grid-cols-2 gap-3">
            <button
              onClick={() => handleDirectAccess('buyer')}
              className="text-sm text-emerald-600 hover:text-emerald-700 font-medium hover:bg-emerald-50 py-2 px-3 rounded-lg transition-colors duration-200"
            >
              🛒 Quick Buyer Access
            </button>
            <button
              onClick={() => handleDirectAccess('NGO')}
              className="text-sm text-blue-600 hover:text-blue-700 font-medium hover:bg-blue-50 py-2 px-3 rounded-lg transition-colors duration-200"
            >
              🏢 Quick NGO Access
            </button>
          </div>

          {/* Status Info */}
          <div className="mt-6 p-4 bg-slate-50 rounded-xl border border-slate-200">
            <div className="flex items-center space-x-2 text-slate-600 text-sm">
              <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse"></div>
              <span>System Status: Ready</span>
            </div>
            <div className="text-xs text-slate-500 mt-1">
              No authentication required • Direct access enabled
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SimpleLogin;
