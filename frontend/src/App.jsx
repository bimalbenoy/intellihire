import './App.css'
import Candidate from './pages/candidate'
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';  
import SignUp from './components/auth/SignUp';
import Login from './components/auth/Login';
function App() {
  return (
    <>
      <Router>
      <Routes>
        <Route path="/candidate" element={<Candidate />} />
        <Route path="/signup" element={<SignUp />} />
        <Route path="/login" element={<Login />} />
        <Route path="/" element={<Navigate to="/login" replace />} />
      </Routes>
    </Router>
    </>
  )
}

export default App
