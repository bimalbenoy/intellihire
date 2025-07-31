import React, { useState } from 'react';

const Login = () => {
  const [form, setForm] = useState({ email: '', password: '' });
  const [msg, setMsg] = useState('');

  const handleChange = e => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async e => {
    e.preventDefault();
    try {
      const res = await fetch('http://localhost:8000/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form)
      });

      if (!res.ok) throw new Error('Login failed');
      const data = await res.json();
      localStorage.setItem('token', data.access_token);  // save token
      setMsg('Login successful!');
    } catch (err) {
      console.error(err);
      setMsg('Login error!');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input name="email" onChange={handleChange} placeholder="Email" />
      <input name="password" type="password" onChange={handleChange} placeholder="Password" />
      <button type="submit">Log In</button>
      <p>{msg}</p>
    </form>
  );
};

export default Login;

