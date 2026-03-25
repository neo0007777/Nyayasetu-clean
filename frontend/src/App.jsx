import { Routes, Route } from 'react-router-dom';
import Navigation from './components/Navigation';
import ProtectedRoute from './components/ProtectedRoute'; // JWT Sentinel
import Home from './pages/Home';
import CaseFinder from './pages/CaseFinder';
import DraftAssistant from './pages/DraftAssistant';
import ClauseConflict from './pages/ClauseConflict';
import LegalAid from './pages/LegalAid';
import Login from './pages/Login'; // Public Authenticator
import './App.css';

// The main Application shell requiring Auth
const AppShell = () => (
  <div className="nyayasetu-app">
    <Navigation />
    <main className="main-content">
      <Routes>
        <Route path="/" element={<ProtectedRoute><Home /></ProtectedRoute>} />
        <Route path="/case-finder" element={<ProtectedRoute><CaseFinder /></ProtectedRoute>} />
        <Route path="/draft-assistant" element={<ProtectedRoute><DraftAssistant /></ProtectedRoute>} />
        <Route path="/clause-conflict" element={<ProtectedRoute><ClauseConflict /></ProtectedRoute>} />
        <Route path="/legal-aid" element={<ProtectedRoute><LegalAid /></ProtectedRoute>} />
      </Routes>
    </main>
  </div>
);

// The core Router decoupling Auth state
const App = () => {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="*" element={<AppShell />} />
    </Routes>
  );
};

export default App;
