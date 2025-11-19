import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

export default function Signup() {
  const [form, setForm] = useState({ name: '', email: '', password: '' });
  const [msg, setMsg] = useState('');
  const navigate = useNavigate();

  const handleChange = e => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async e => {
    e.preventDefault();
    setMsg('');
    try {
      const res = await axios.post('http://127.0.0.1:8000/api/users', form);
      setMsg('Signup successful: ' + JSON.stringify(res.data));
      navigate('/login');
    } catch (err) {
      setMsg(err.response?.data?.detail || 'Signup error');
    }
  };

  return (
    <div className="d-flex justify-content-center">
      <div className="card container-card p-4">
        <h4 className="mb-3">Sign Up</h4>
        <form onSubmit={handleSubmit}>
          <div className="mb-2">
            <label className="form-label">Full name</label>
            <input name="name" className="form-control" onChange={handleChange} required/>
          </div>
          <div className="mb-2">
            <label className="form-label">Email</label>
            <input name="email" type="email" className="form-control" onChange={handleChange} required/>
          </div>
          <div className="mb-2">
            <label className="form-label">Password</label>
            <input name="password" type="password" className="form-control" onChange={handleChange} required/>
          </div>
          <button className="btn btn-success mt-2" type="submit">Sign Up</button>
        </form>
        <pre className="mt-3">{msg}</pre>
      </div>
    </div>
  );
}
