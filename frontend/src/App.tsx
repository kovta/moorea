import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import Home from './pages/Home';
import SavedMoodboards from './pages/SavedMoodboards';

const App: React.FC = () => {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/saved" element={<SavedMoodboards />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
};

export default App;