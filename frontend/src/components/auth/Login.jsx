import React, { useState } from 'react';
import '../../pages/CandidateForm.css';
import {
  Box,
  Button,
  Container,
  TextField,
  Typography,
  Paper,
  Link,
  Alert,
} from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';

const Login = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });

  const [errors, setErrors] = useState({
    email: '',
    password: '',
  });

  const [submitError, setSubmitError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const validateForm = () => {
    let isValid = true;
    const newErrors = { ...errors };

    // Validate email
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(formData.email)) {
      newErrors.email = 'Please enter a valid email address';
      isValid = false;
    } else {
      newErrors.email = '';
    }

    // Validate password
    if (!formData.password) {
      newErrors.password = 'Password is required';
      isValid = false;
    } else {
      newErrors.password = '';
    }

    setErrors(newErrors);
    return isValid;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value,
    }));
    // Clear the error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: '',
      }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitError('');

    if (!validateForm()) {
      return;
    }

    setIsLoading(true);
    try {
      // TODO: Implement actual login logic here
      console.log('Login form submitted:', formData);
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // If successful, you might want to redirect to dashboard
      // navigate('/dashboard');
    } catch (error) {
      setSubmitError(error.message || 'Invalid email or password');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="page">
      <div className="content" style={{ justifyContent: 'center', alignItems: 'center' }}>
        <div className="upload-box" style={{ width: '100%', maxWidth: 420, margin: '4rem auto' }}>
          <div style={{ fontWeight: 700, fontSize: '2rem', color: '#2563eb', textAlign: 'center', marginBottom: '1.5rem' }}>Sign In</div>
          {submitError && (
            <div style={{ background: '#fee2e2', color: '#b91c1c', borderRadius: '0.5rem', padding: '0.75rem 1rem', marginBottom: '1rem', textAlign: 'center' }}>
              {submitError}
            </div>
          )}
          <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
            <input
              className="upload-input"
              type="email"
              name="email"
              placeholder="Email Address"
              value={formData.email}
              onChange={handleChange}
              required
              style={{ fontSize: '1.1rem' }}
            />
            <input
              className="upload-input"
              type="password"
              name="password"
              placeholder="Password"
              value={formData.password}
              onChange={handleChange}
              required
              style={{ fontSize: '1.1rem' }}
            />
            <button
              type="submit"
              style={{
                background: '#2563eb',
                color: 'white',
                border: 'none',
                borderRadius: '0.5rem',
                padding: '0.75rem 0',
                fontWeight: 700,
                fontSize: '1.1rem',
                cursor: 'pointer',
                marginTop: '0.5rem'
              }}
              disabled={isLoading}
            >
              {isLoading ? 'Signing in...' : 'Sign In'}
            </button>
            <div style={{ textAlign: 'center', marginTop: '0.5rem' }}>
              <a href="/signup" style={{ color: '#2563eb', textDecoration: 'underline', fontWeight: 500 }}>
                Don't have an account? Sign Up
              </a>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Login;
