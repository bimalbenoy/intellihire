import './App.css';
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';

import Candidate from './pages/candidate';
import AdminPage from './pages/AdminPage'; // ✅ Add this line
import SignUp from './components/auth/SignUp';
import Login from './components/auth/Login';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/candidate" element={<Candidate />} />
        <Route path="/admin" element={<AdminPage />} /> {/* ✅ Add this route */}
        <Route path="/signup" element={<SignUp />} />
        <Route path="/login" element={<Login />} />
        <Route path="/" element={<Navigate to="/login" replace />} />
      </Routes>
    </Router>
  );
}

export default App;
