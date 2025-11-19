import React, { useEffect, useState } from 'react';
import axios from 'axios';

export default function ReportsList() {
  const [reports, setReports] = useState([]);
  const [err, setErr] = useState('');

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/api/reports')
      .then(res => setReports(res.data))
      .catch(e => setErr(e.response?.data?.detail || 'Failed to fetch reports'));
  }, []);

  return (
    <div className="py-4">
      <h4>Reports</h4>
      {err && <div className="alert alert-danger">{err}</div>}
      <div className="list-group">
        {reports.map(r => (
          <div key={r.id} className="list-group-item">
            <strong>{r.description}</strong>
            <div><small>{r.location} — {r.status}</small></div>
            <div><small>Lat: {r.latitude} Lng: {r.longitude}</small></div>
            <div><small>id: {r.id} created: {r.created_at}</small></div>
          </div>
        ))}
      </div>
    </div>
  );
}
