import React, { useState } from 'react';
import { initiatePinterestAuth } from '../utils/api';

interface PinterestLoginButtonProps {
  onSuccess?: () => void;
  onError?: (error: string) => void;
  className?: string;
}

export const PinterestLoginButton: React.FC<PinterestLoginButtonProps> = ({
  onSuccess,
  onError,
  className = ''
}) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handlePinterestLogin = () => {
    setLoading(true);
    setError(null);
    try {
      // Direct redirect to backend authorization endpoint
      // The backend will handle the OAuth flow and redirect appropriately
      initiatePinterestAuth();
      // Note: Once redirect happens, component will unmount, so onSuccess is not called
      // Success will be determined by the callback page after OAuth completes
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to initiate Pinterest login';
      setError(message);
      setLoading(false);
      onError?.(message);
    }
  };

  return (
    <div className={`pinterest-login ${className}`}>
      <button
        onClick={handlePinterestLogin}
        disabled={loading}
        className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:opacity-50 flex items-center gap-2 font-medium transition"
      >
        {loading ? (
          <>
            <span className="animate-spin">⏳</span>
            Connecting...
          </>
        ) : (
          <>
            <span>📌</span>
            Sign in with Pinterest
          </>
        )}
      </button>
      {error && (
        <p className="text-red-600 text-sm mt-2">{error}</p>
      )}
    </div>
  );
};

export default PinterestLoginButton;
