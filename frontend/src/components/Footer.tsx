import React from 'react';

const Footer: React.FC = () => {
  return (
    <footer className="mt-12 py-8 border-t border-gray-200">
      <div className="max-w-4xl mx-auto px-4 text-center">
        <div className="text-sm text-gray-500">
          <a href="/PRIVACY_POLICY.md" className="underline mx-2 hover:text-gray-700" target="_blank" rel="noopener noreferrer">Privacy Policy</a>
          <span className="text-gray-300">•</span>
          <a href="/TERMS_OF_SERVICE.md" className="underline mx-2 hover:text-gray-700" target="_blank" rel="noopener noreferrer">Terms of Service</a>
        </div>
        <div className="mt-2 text-xs text-gray-400">
          Made with ✨ for fashion lovers
        </div>
      </div>
    </footer>
  );
};

export default Footer;