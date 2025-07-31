import './App.css';
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';

import Candidate from './pages/candidate';
import Candidate1 from './pages/candidate1';
import AdminPage from './pages/AdminPage';
import AdminView from './pages/AdminView';
import SignUp from './components/auth/SignUp';
import Login from './components/auth/Login';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/candidate" element={<Candidate />} />
        <Route path="/candidate1" element={<Candidate1 />} />
        <Route path="/admin" element={<AdminPage />} />
        <Route path="/adminview" element={<AdminView />} />
        <Route path="/signup" element={<SignUp />} />
        <Route path="/login" element={<Login />} />
        <Route path="/" element={<Navigate to="/login" replace />} />
      </Routes>
    </Router>
  );
}

export default App;
