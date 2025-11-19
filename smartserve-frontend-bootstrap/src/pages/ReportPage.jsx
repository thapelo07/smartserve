import React, { useState } from "react";
import axios from "axios";

export default function ReportPage() {
  const [form, setForm] = useState({
    description: "",
    location: "",
  });
  const [message, setMessage] = useState("");

  const user_id = localStorage.getItem("smartserve_user_id");

  const handleChange = (e) =>
    setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage("");

    try {
      const res = await axios.post("http://127.0.0.1:8000/api/reports", {
        ...form,
        user_id: Number(user_id),
      });

      setMessage("Report submitted!");

    } catch (err) {
      setMessage(err.response?.data?.detail || "Error sending report");
    }
  };

  return (
    <div className="container mt-5" style={{ maxWidth: "500px" }}>
      <h3>Submit a Report</h3>

      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label>Description</label>
          <input
            className="form-control"
            name="description"
            onChange={handleChange}
            required
          />
        </div>

        <div className="mb-3">
          <label>Location</label>
          <input
            className="form-control"
            name="location"
            onChange={handleChange}
            required
          />
        </div>

        <button className="btn btn-primary">Send Report</button>
      </form>

      <button
        className="btn btn-secondary mt-3"
        onClick={() => (window.location.href = "/map")}
      >
        View Map
      </button>

      <p className="mt-3 text-success">{message}</p>
    </div>
  );
}
