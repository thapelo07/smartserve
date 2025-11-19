import React, { useState } from 'react';
import axios from 'axios';

export default function ReportForm() {
  const [form, setForm] = useState({ description: '', location: '', user_id: '' });
  const [file, setFile] = useState(null);
  const [msg, setMsg] = useState('');

  const handleChange = e => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async e => {
    e.preventDefault();
    setMsg('');
    try {
      const res = await axios.post('http://127.0.0.1:8000/api/reports', {
        description: form.description,
        location: form.location,
        user_id: form.user_id ? Number(form.user_id) : 0,
        latitude: 0,
        longitude: 0
      });
      const reportId = res.data.id;
      if (file) {
        const data = new FormData();
        data.append('report_id', reportId);
        data.append('file', file);
        await axios.post('http://127.0.0.1:8000/api/reports/upload-image', data, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });
      }
      setMsg('Report submitted (id: ' + reportId + ')');
      setForm({ description: '', location: '', user_id: '' });
      setFile(null);
    } catch (err) {
      setMsg(err.response?.data?.detail || 'Error submitting report');
    }
  };

  return (
    <div className="d-flex justify-content-center">
      <div className="card container-card p-4">
        <h4 className="mb-3">Submit Report</h4>
        <form onSubmit={handleSubmit}>
          <div className="mb-2">
            <label className="form-label">Description</label>
            <input name="description" className="form-control" onChange={handleChange} value={form.description} required/>
          </div>
          <div className="mb-2">
            <label className="form-label">Location (e.g., Tembisa)</label>
            <input name="location" className="form-control" onChange={handleChange} value={form.location} required/>
          </div>
          <div className="mb-2">
            <label className="form-label">User ID (optional)</label>
            <input name="user_id" className="form-control" onChange={handleChange} value={form.user_id}/>
          </div>
          <div className="mb-2">
            <label className="form-label">Image (optional)</label>
            <input type="file" className="form-control" onChange={e => setFile(e.target.files[0])} accept="image/*"/>
          </div>
          <button className="btn btn-primary mt-2" type="submit">Submit</button>
        </form>
        <pre className="mt-3">{msg}</pre>
      </div>
    </div>
  );
}
