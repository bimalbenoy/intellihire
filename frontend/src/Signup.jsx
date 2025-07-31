import React, { useState } from 'react';

const SignUp = () => {
  const [form, setForm] = useState({ email: '', password: '' });
  const [msg, setMsg] = useState('');

  const handleChange = e => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async e => {
    e.preventDefault();
    try {
      const res = await fetch('http://localhost:8000/auth/signup', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form)
      });

      if (!res.ok) throw new Error('Signup failed');
      const data = await res.json();
      setMsg('Signup successful!');
    } catch (err) {
      console.error(err);
      setMsg('Signup error!');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input name="email" onChange={handleChange} placeholder="Email" />
      <input name="password" type="password" onChange={handleChange} placeholder="Password" />
      <button type="submit">Sign Up</button>
      <p>{msg}</p>
    </form>
  );
};

export default SignUp;

