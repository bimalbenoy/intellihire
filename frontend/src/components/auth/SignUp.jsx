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
  MenuItem,
  Alert,
} from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';

const SignUp = () => {
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    password: '',
    confirmPassword: '',
    role: 'candidate',
  });

  const [errors, setErrors] = useState({
    firstName: '',
    lastName: '',
    email: '',
    password: '',
    confirmPassword: '',
  });

  const [submitError, setSubmitError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const validateForm = () => {
    let isValid = true;
    const newErrors = { ...errors };

    // Validate firstName
    if (formData.firstName.trim().length < 2) {
      newErrors.firstName = 'First name must be at least 2 characters';
      isValid = false;
    } else {
      newErrors.firstName = '';
    }

    // Validate lastName
    if (formData.lastName.trim().length < 2) {
      newErrors.lastName = 'Last name must be at least 2 characters';
      isValid = false;
    } else {
      newErrors.lastName = '';
    }

    // Validate email
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(formData.email)) {
      newErrors.email = 'Please enter a valid email address';
      isValid = false;
    } else {
      newErrors.email = '';
    }

    // Validate password
    if (formData.password.length < 8) {
      newErrors.password = 'Password must be at least 8 characters';
      isValid = false;
    } else {
      newErrors.password = '';
    }

    // Validate confirmPassword
    if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
      isValid = false;
    } else {
      newErrors.confirmPassword = '';
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
      // TODO: Implement actual signup logic here
      console.log('Signup form submitted:', formData);
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // If successful, you might want to redirect to login
      // navigate('/login');
    } catch (error) {
      setSubmitError(error.message || 'An error occurred during signup');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="page">
      <div className="content" style={{ justifyContent: 'center', alignItems: 'center' }}>
        <div className="upload-box" style={{ width: '100%', maxWidth: 480, margin: '3rem auto' }}>
          <div style={{ fontWeight: 700, fontSize: '2rem', color: '#2563eb', textAlign: 'center', marginBottom: '1.5rem' }}>Sign Up</div>
          {submitError && (
            <div style={{ background: '#fee2e2', color: '#b91c1c', borderRadius: '0.5rem', padding: '0.75rem 1rem', marginBottom: '1rem', textAlign: 'center' }}>
              {submitError}
            </div>
          )}
          <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
            <input
              className="upload-input"
              type="text"
              name="firstName"
              placeholder="First Name"
              value={formData.firstName}
              onChange={handleChange}
              required
              style={{ fontSize: '1.1rem' }}
            />
            <input
              className="upload-input"
              type="text"
              name="lastName"
              placeholder="Last Name"
              value={formData.lastName}
              onChange={handleChange}
              required
              style={{ fontSize: '1.1rem' }}
            />
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
            <input
              className="upload-input"
              type="password"
              name="confirmPassword"
              placeholder="Confirm Password"
              value={formData.confirmPassword}
              onChange={handleChange}
              required
              style={{ fontSize: '1.1rem' }}
            />
            <select
              className="upload-input"
              name="role"
              value={formData.role}
              onChange={handleChange}
              required
              style={{ fontSize: '1.1rem' }}
            >
              <option value="candidate">Candidate</option>
              <option value="reviewer">Reviewer</option>
              <option value="admin">Admin</option>
            </select>
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
              {isLoading ? 'Signing up...' : 'Sign Up'}
            </button>
            <div style={{ textAlign: 'center', marginTop: '0.5rem' }}>
              <a href="/login" style={{ color: '#2563eb', textDecoration: 'underline', fontWeight: 500 }}>
                Already have an account? Sign In
              </a>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default SignUp;
