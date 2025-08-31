import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { login } from '../api/api';
// import { Turnstile } from '@marsidev/react-turnstile'; // Commented out for simplified testing


const Login = ({ onLogin }) => {
  const [formData, setFormData] = useState({ username: '', password: '', role: 'buyer' });
  const [status, setStatus] = useState(null)
  const navigate = useNavigate();
  // const SITE_KEY = process.env.REACT_APP_SITE_KEY || '1x00000000000000000000AA'; // Not needed
  const [showPassword, setShowPassword] = useState(false);
  const [loadStatus, setLoadStatus] = useState(false);
  const [showTestPrompt, setShowTestPrompt] = useState(true);

  useEffect(() => {
    setTimeout(() => setShowTestPrompt(false), 10000); // Auto-hide after 10 sec
  }, []);


  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };


  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      setLoadStatus(true);
      console.log("Logging in with:", formData);
      const response = await login({ ...formData });
      console.log("Login response:", response.data);
      
      // Store the token
      localStorage.setItem('token', response.data.token);

      // Get user role from the response
      const userRole = response.data.user.role;
      onLogin({ username: formData.username, role: userRole, id: response.data.user.id });

      // Redirect based on role
      const dashboardPath = userRole === 'NGO' 
        ? '/NGO-dashboard' 
        : '/buyer-dashboard';
          
      console.log(`Redirecting to ${dashboardPath}`);
      navigate(dashboardPath);
    } catch (error) {
      setLoadStatus(false);
      console.error("Login error:", error);
      
      // Handle different error types
      if (error.response) {
        if (error.response.status === 401) {
          setStatus("Invalid credentials. Please try again.");
        } else if (error.response.status === 400) {
          setStatus(error.response.data.message || "Missing required information");
        } else {
          setStatus(error.response.data.message || "Login failed. Please try again.");
        }
      } else {
        setStatus("Network error. Please check your connection.");
      }
      
      // Clear error message after 3 seconds
      setTimeout(() => setStatus(null), 3000);
    }
  };

  return (
    <>
      <div className="flex justify-center items-center py-12 px-4 w-full min-h-screen bg-gradient-to-br from-emerald-100 to-blue-200">
        {status && (
          <div className="flex fixed top-20 left-1/2 items-center py-2 px-4 text-white bg-red-500 rounded-lg shadow-lg transition-transform duration-300 transform -translate-x-1/2 animate-slideIn">
            <span>{status}</span>
          </div>
        )}

        <div className="w-full max-w-md rounded-xl shadow-xl bg-white/80 backdrop-blur-sm">
          <div className="p-8 rounded-xl shadow-lg bg-emerald-50/90">
            <div className="text-center mb-8">
              <h2 className="text-2xl font-bold text-emerald-800 mb-2">WELCOME BACK</h2>
              <p className="text-emerald-600">Login to your account</p>
            </div>

            {/* Simple Direct Login Buttons */}
            <div className="space-y-4">
              <button
                onClick={async () => {
                  try {
                    setLoadStatus(true);
                    const response = await fetch('http://localhost:5000/api/login', {
                      method: 'POST',
                      headers: { 'Content-Type': 'application/json' },
                      body: JSON.stringify({ username: "test_admin", password: "sepolia", role: "NGO" })
                    });
                    const data = await response.json();
                    if (response.ok) {
                      localStorage.setItem('token', data.access_token);
                      onLogin({ username: "test_admin", role: "NGO", id: "test" });
                      navigate('/ngo-dashboard');
                    } else {
                      setStatus("Login failed: " + (data.message || "Unknown error"));
                    }
                  } catch (error) {
                    setStatus("Network error: " + error.message);
                  } finally {
                    setLoadStatus(false);
                  }
                }}
                disabled={loadStatus}
                className="w-full py-3 px-4 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:ring-offset-2 disabled:opacity-50"
              >
                {loadStatus ? "Logging in..." : "Login as NGO (test_admin)"}
              </button>

              <button
                onClick={async () => {
                  try {
                    setLoadStatus(true);
                    const response = await fetch('http://localhost:5000/api/login', {
                      method: 'POST',
                      headers: { 'Content-Type': 'application/json' },
                      body: JSON.stringify({ username: "test_buyer", password: "sepolia", role: "buyer" })
                    });
                    const data = await response.json();
                    if (response.ok) {
                      localStorage.setItem('token', data.access_token);
                      onLogin({ username: "test_buyer", role: "buyer", id: "test" });
                      navigate('/buyer-dashboard');
                    } else {
                      setStatus("Login failed: " + (data.message || "Unknown error"));
                    }
                  } catch (error) {
                    setStatus("Network error: " + error.message);
                  } finally {
                    setLoadStatus(false);
                  }
                }}
                disabled={loadStatus}
                className="w-full py-3 px-4 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50"
              >
                {loadStatus ? "Logging in..." : "Login as Buyer (test_buyer)"}
              </button>
            </div>

            <div className="mt-6 text-center">
              <p className="text-sm text-emerald-600">
                Test credentials are pre-configured
              </p>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default Login;
