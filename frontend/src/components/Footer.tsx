import React from 'react';
import { Link } from 'react-router-dom';

const Footer: React.FC = () => {
  return (
    <footer className="mt-12 py-8 border-t border-gray-200">
      <div className="max-w-4xl mx-auto px-4 text-center">
        <div className="text-sm text-gray-500">
          <Link to="/privacy" className="underline mx-2 hover:text-gray-700">Privacy Policy</Link>
          <span className="text-gray-300">•</span>
          <Link to="/terms" className="underline mx-2 hover:text-gray-700">Terms of Service</Link>
        </div>
        <div className="mt-2 text-xs text-gray-400">
          Made with ✨ for fashion lovers
        </div>
      </div>
    </footer>
  );
};

export default Footer;