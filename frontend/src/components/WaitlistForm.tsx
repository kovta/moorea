import React, { useState } from 'react';
import { subscribeToWaitlist, WaitlistSubscribeRequest } from '../utils/api';

interface WaitlistFormProps {
  onSuccess?: (email: string) => void;
}

const WaitlistForm: React.FC<WaitlistFormProps> = ({ onSuccess }) => {
  const [email, setEmail] = useState('');
  const [name, setName] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  const validateEmail = (email: string): boolean => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setMessage(null);

    // Validate email
    if (!email.trim()) {
      setMessage({ type: 'error', text: 'Please enter your email address' });
      return;
    }

    if (!validateEmail(email)) {
      setMessage({ type: 'error', text: 'Please enter a valid email address' });
      return;
    }

    setIsSubmitting(true);

    try {
      const request: WaitlistSubscribeRequest = {
        email: email.trim(),
        ...(name.trim() && { name: name.trim() })
      };

      const response = await subscribeToWaitlist(request);
      
      setMessage({ type: 'success', text: response.message });
      setEmail('');
      setName('');
      
      if (onSuccess) {
        onSuccess(response.email);
      }
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || error.message || 'Something went wrong. Please try again.';
      setMessage({ type: 'error', text: errorMessage });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="w-full max-w-md mx-auto">
      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Name field (optional) */}
        <div>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Your name (optional)"
            className="w-full px-4 py-3 rounded-xl border-2 border-gray-200 focus:outline-none focus:ring-2 focus:ring-purple-400 focus:border-purple-400 transition-all text-gray-900 placeholder-gray-400"
            disabled={isSubmitting}
          />
        </div>

        {/* Email field */}
        <div>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Enter your email"
            required
            className="w-full px-4 py-3 rounded-xl border-2 border-gray-200 focus:outline-none focus:ring-2 focus:ring-purple-400 focus:border-purple-400 transition-all text-gray-900 placeholder-gray-400"
            disabled={isSubmitting}
          />
        </div>

        {/* Submit button */}
        <button
          type="submit"
          disabled={isSubmitting}
          className="btn-primary w-full py-3 text-lg font-semibold disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isSubmitting ? (
            <span className="inline-flex items-center gap-2">
              <span className="animate-spin">⏳</span>
              Joining...
            </span>
          ) : (
            'Join the Waitlist ✨'
          )}
        </button>

        {/* Message display */}
        {message && (
          <div
            className={`p-4 rounded-xl ${
              message.type === 'success'
                ? 'bg-green-50 border border-green-200 text-green-800'
                : 'bg-red-50 border border-red-200 text-red-800'
            } animate-fade-in`}
          >
            <p className="text-sm font-medium">{message.text}</p>
          </div>
        )}

        {/* Privacy note */}
        <p className="text-xs text-gray-500 text-center">
          We'll never spam you. Unsubscribe anytime.
        </p>
      </form>
    </div>
  );
};

export default WaitlistForm;

