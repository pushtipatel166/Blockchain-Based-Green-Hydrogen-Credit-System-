import React, { useState, useEffect } from 'react';
import { Route, Routes, Navigate, Link, useNavigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import NGOSignup from './components/NGOSignup';
import BuyerSignup from './components/BuyerSignup';

import SimpleLogin from './components/SimpleLogin';
import NGODashboard from './components/NGODashboard/NGODashboard';
import BuyerDashboard from './components/BuyerDashboard';

import TestPage from './components/testPage';
import CreditDetails from './components/CreditDetails'
import Profile from './components/Profile'

import Home from './components/Home';
import { SpeedInsights } from '@vercel/speed-insights/react';
import { CCProvider } from './context/SmartContractConnector';

import { SiRender } from "react-icons/si";




const App = () => {
  const [user, setUser] = useState(null);
  const [backendReady, setBackendReady] = useState(false);
  const navigate = useNavigate();

  // Keep localStorage for user data
  useEffect(() => {
    console.log("App mounted - ready for direct access");
  }, []);



  const handleLogout = () => {
    localStorage.removeItem('token');
    setUser(null);
  };

  // Backend check bypassed - always ready
  useEffect(() => {
    setBackendReady(true);
  }, []);

  useEffect(() => {
    document.title = "Green Hydrogen Credit Ecosystem";
    // Check if user data exists in localStorage
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      const userData = JSON.parse(storedUser);
      setUser(userData);
    }
  }, []);

  useEffect(() => {
    // Skip backend check - go directly to home
    if (window.location.pathname === '/loading') {
      navigate('/home')
    }
  }, [navigate])

  //inline component
  const LoadingScreen = () => (
    <div style={{
      height: '100vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      fontSize: '24px',
      fontWeight: 'bold',
      backgroundColor: '#f0fdf4',
      color: '#166534'
    }}>
      <div style={{ marginRight: '12px', color: '#16a34a' }}>
        <SiRender />
      </div>
      <span style={{ color: '#166534' }}>Render is restarting the service...</span>
    </div>
  );

  return (
    <CCProvider>
      {/* <Router> */}
      <div >
        <Navbar user={user} onLogout={handleLogout} />
        <div >
          <Routes>
            <Route path='/loading' element={<LoadingScreen />} />
            <Route path="/home" element={<Home />} />
            <Route path="/NGO-signup" element={<NGOSignup />} />
            <Route path="/buyer-signup" element={<BuyerSignup />} />
            <Route path="/login" element={<SimpleLogin />} />
            <Route path="/test" element={<TestPage />} />
            <Route path="/credits/:creditId" element={<CreditDetails />} />
            <Route path="/profile" element={<Profile />} />
            <Route
              path="/NGO-dashboard"
              element={<NGODashboard onLogout={handleLogout} />}
            />
            <Route
              path="/buyer-dashboard"
              element={<BuyerDashboard onLogout={handleLogout} />}
            />

            <Route path="/" element={<Navigate to="/home" replace />} />
          </Routes>;
        </div>
        <SpeedInsights />
      </div>
      {/* </Router> */}
    </CCProvider>
  );
};

export default App;
