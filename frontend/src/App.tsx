import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import Home from './pages/Home';
import LandingPage from './pages/LandingPage';
import SavedMoodboards from './pages/SavedMoodboards';
import PrivacyPolicy from './pages/PrivacyPolicy';
import Terms from './pages/Terms';
import PinterestCallback from './pages/PinterestCallback';
import Footer from './components/Footer';

/**
 * Main App component with React Router configuration
 * Routes:
 * - / -> Home (moodboard generator)
 * - /waitlist -> LandingPage (waitlist signup)
 * - /saved -> SavedMoodboards
 * - /privacy -> PrivacyPolicy
 * - /auth/pinterest/callback -> Pinterest OAuth callback handler
 */
const App: React.FC = () => {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/waitlist" element={<LandingPage />} />
          <Route path="/saved" element={<SavedMoodboards />} />
          <Route path="/privacy" element={<PrivacyPolicy />} />
          <Route path="/terms" element={<Terms />} />
          <Route path="/auth/pinterest/callback" element={<PinterestCallback />} />
        </Routes>
        <Footer />
      </Router>
    </AuthProvider>
  );
};

export default App;