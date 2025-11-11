import React from 'react';
import { Link } from 'react-router-dom';
import WaitlistForm from '../components/WaitlistForm';

const LandingPage: React.FC = () => {
  const handleSuccess = (email: string) => {
    console.log('Successfully subscribed:', email);
    // Could add analytics tracking here
  };

  return (
    <div className="min-h-screen gradient-bg relative overflow-hidden">
      {/* Decorative background elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-20 left-10 w-72 h-72 bg-white/5 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute bottom-20 right-10 w-96 h-96 bg-white/5 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '1s' }}></div>
      </div>

      <div className="max-w-6xl mx-auto px-4 md:px-8 py-12 md:py-20 relative z-10">
        {/* Hero Section */}
        <div className="text-center mb-12 md:mb-16 animate-fade-in">
          <div className="mb-6">
            <span className="text-5xl md:text-6xl mb-4 block animate-bounce-slow">✨</span>
            <h1 className="text-4xl sm:text-5xl md:text-7xl font-display font-bold text-white mb-4 drop-shadow-lg">
              Moorea
            </h1>
            <h2 className="text-2xl sm:text-3xl md:text-4xl font-display font-semibold text-white mb-6 drop-shadow-lg">
              Coming Soon
            </h2>
          </div>
          
          <p className="text-lg md:text-xl lg:text-2xl text-white font-medium max-w-3xl mx-auto leading-relaxed mb-4">
            AI-powered moodboard generation for fashion lovers
          </p>
          <p className="text-base md:text-lg text-white/90 max-w-2xl mx-auto">
            Upload your clothing photos and get instant aesthetic inspiration
          </p>
        </div>

        {/* Signup Form Card */}
        <div className="card max-w-2xl mx-auto mb-16 animate-slide-up shadow-2xl">
          <div className="text-center mb-8">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-purple-100 to-pink-100 rounded-full mb-4">
              <span className="text-2xl">📧</span>
            </div>
            <h3 className="text-2xl md:text-3xl font-display font-semibold text-gray-900 mb-3">
              Be the first to know when we launch
            </h3>
            <p className="text-gray-600 text-base">
              Join our waitlist and get early access to the future of fashion inspiration
            </p>
          </div>
          
          <WaitlistForm onSuccess={handleSuccess} />
        </div>

        {/* Features Preview */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 md:gap-8 max-w-4xl mx-auto mb-16">
          <div className="card text-center animate-fade-in hover:scale-105 transition-transform duration-300" style={{ animationDelay: '0.1s' }}>
            <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-pink-100 to-orange-100 rounded-full mb-4">
              <span className="text-3xl">📸</span>
            </div>
            <h4 className="text-xl font-semibold text-gray-900 mb-2">Upload Photos</h4>
            <p className="text-gray-600 text-sm leading-relaxed">
              Simply drop your clothing images and let our AI work its magic
            </p>
          </div>

          <div className="card text-center animate-fade-in hover:scale-105 transition-transform duration-300" style={{ animationDelay: '0.2s' }}>
            <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-purple-100 to-pink-100 rounded-full mb-4">
              <span className="text-3xl">🎨</span>
            </div>
            <h4 className="text-xl font-semibold text-gray-900 mb-2">AI Detection</h4>
            <p className="text-gray-600 text-sm leading-relaxed">
              Our advanced AI identifies your style aesthetic automatically
            </p>
          </div>

          <div className="card text-center animate-fade-in hover:scale-105 transition-transform duration-300" style={{ animationDelay: '0.3s' }}>
            <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-yellow-100 to-orange-100 rounded-full mb-4">
              <span className="text-3xl">✨</span>
            </div>
            <h4 className="text-xl font-semibold text-gray-900 mb-2">Curated Moodboards</h4>
            <p className="text-gray-600 text-sm leading-relaxed">
              Get personalized moodboards filled with style inspiration
            </p>
          </div>
        </div>

        {/* Footer */}
        <div className="text-center text-white/70 text-sm animate-fade-in border-t border-white/10 pt-8 mt-12">
          <p className="mb-4 text-base">
            Made with ✨ for fashion lovers
          </p>
          <div className="flex flex-wrap justify-center gap-4 text-sm">
            <Link 
              to="/privacy" 
              className="hover:text-white transition-colors underline decoration-white/30 hover:decoration-white"
            >
              Privacy Policy
            </Link>
            <span className="text-white/30">•</span>
            <a 
              href="mailto:annaszilviakennedy@gmail.com" 
              className="hover:text-white transition-colors underline decoration-white/30 hover:decoration-white"
            >
              Contact Us
            </a>
          </div>
          <p className="mt-6 text-xs text-white/50">
            © {new Date().getFullYear()} Moorea. All rights reserved.
          </p>
        </div>
      </div>
    </div>
  );
};

export default LandingPage;

