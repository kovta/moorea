import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import Home from './pages/Home';
import LandingPage from './pages/LandingPage';
import SavedMoodboards from './pages/SavedMoodboards';
import PrivacyPolicy from './pages/PrivacyPolicy';

/**
 * Main App component with React Router configuration
 * Routes:
 * - / -> Home (moodboard generator)
 * - /waitlist -> LandingPage (waitlist signup)
 * - /saved -> SavedMoodboards
 * - /privacy -> PrivacyPolicy
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
        </Routes>
      </Router>
    </AuthProvider>
  );
};

export default App;