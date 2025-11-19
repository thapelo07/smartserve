import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

export default function Login() {
  const [form, setForm] = useState({ email: '', password: '' });
  const [msg, setMsg] = useState('');
  const navigate = useNavigate();

  const handleChange = e => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async e => {
    e.preventDefault();
    setMsg('');
    try {
      const res = await axios.post('http://127.0.0.1:8000/api/login', form);
      setMsg('Login successful: ' + JSON.stringify(res.data));
      if (res.data.user_id) localStorage.setItem('smartserve_user_id', res.data.user_id);
      navigate('/report');
    } catch (err) {
      setMsg(err.response?.data?.detail || 'Login error');
    }
  };

  return (
    <div className="d-flex justify-content-center">
      <div className="card container-card p-4">
        <h4 className="mb-3">Login</h4>
        <form onSubmit={handleSubmit}>
          <div className="mb-2">
            <label className="form-label">Email</label>
            <input name="email" type="email" className="form-control" onChange={handleChange} required/>
          </div>
          <div className="mb-2">
            <label className="form-label">Password</label>
            <input name="password" type="password" className="form-control" onChange={handleChange} required/>
          </div>
          <button className="btn btn-primary mt-2" type="submit">Login</button>
        </form>
        <div className="mt-3">
          <small>Don't have an account? <a href="/signup">Sign up</a></small>
        </div>
        <pre className="mt-3">{msg}</pre>
      </div>
    </div>
  );
}
