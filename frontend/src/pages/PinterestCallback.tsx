import React, { useEffect, useState, useRef } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import axios from 'axios';

const PinterestCallback: React.FC = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const [status, setStatus] = useState<'loading' | 'success' | 'error'>('loading');
  const [message, setMessage] = useState('Processing your Pinterest login...');
  const hasRun = useRef(false);

  useEffect(() => {
    const handleCallback = async () => {
      // Prevent duplicate calls (React StrictMode in dev calls useEffect twice)
      if (hasRun.current) return;
      hasRun.current = true;
      try {
        const code = searchParams.get('code');
        const state = searchParams.get('state');

        if (!code || !state) {
          setStatus('error');
          setMessage('Missing authorization code or state parameter');
          setTimeout(() => navigate('/'), 3000);
          return;
        }

        // Exchange code for token
        const API_BASE = process.env.REACT_APP_API_URL
          ? process.env.REACT_APP_API_URL.replace(/\/$/, '')
          : '';
        
        const callbackUrl = `${API_BASE}/api/v1/auth/pinterest/callback?code=${code}&state=${state}`;

        const response = await axios.get(callbackUrl);

        if (response.status === 200) {
          setStatus('success');
          setMessage('✅ Pinterest login successful! Redirecting...');
          
          // Store auth info if needed
          localStorage.setItem('pinterest_authenticated', 'true');
          localStorage.setItem('pinterest_auth_time', new Date().toISOString());

          // Redirect to home after 2 seconds
          setTimeout(() => navigate('/'), 2000);
        }
      } catch (error) {
        console.error('Pinterest callback error:', error);
        setStatus('error');
        
        if (axios.isAxiosError(error)) {
          setMessage(`Login failed: ${error.response?.data?.detail || error.message}`);
        } else {
          setMessage('An unexpected error occurred during Pinterest login');
        }
        
        setTimeout(() => navigate('/'), 3000);
      }
    };

    handleCallback();
  }, [searchParams, navigate]);

  const statusStyles = {
    loading: 'bg-blue-50 border-blue-200 text-blue-800',
    success: 'bg-green-50 border-green-200 text-green-800',
    error: 'bg-red-50 border-red-200 text-red-800',
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-50">
      <div className={`border-2 rounded-lg p-8 max-w-md text-center ${statusStyles[status]}`}>
        <div className="mb-4">
          {status === 'loading' && <div className="animate-spin text-4xl">⏳</div>}
          {status === 'success' && <div className="text-4xl">✅</div>}
          {status === 'error' && <div className="text-4xl">❌</div>}
        </div>
        
        <h2 className="text-2xl font-bold mb-2">
          {status === 'loading' && 'Processing...'}
          {status === 'success' && 'Success!'}
          {status === 'error' && 'Error'}
        </h2>
        
        <p className="text-lg mb-4">{message}</p>
        
        {status !== 'loading' && (
          <p className="text-sm opacity-75">Redirecting you back...</p>
        )}
      </div>
    </div>
  );
};

export default PinterestCallback;
