import React, { useEffect, useState, useCallback } from "react";
import { GoogleMap, Marker, LoadScript } from "@react-google-maps/api";
import axios from "axios";

const containerStyle = {
  width: "100%",
  height: "500px",
};

const center = {
  lat: -26.2041,
  lng: 28.0473,
};

function MapPage() {
  const [reports, setReports] = useState([]);

  // ✅ Vite uses import.meta.env
  const backendUrl = import.meta.env.VITE_BACKEND_URL;
  const apiKey = import.meta.env.VITE_GOOGLE_MAPS_API;

  const fetchReports = useCallback(async () => {
    try {
      const response = await axios.get(`${backendUrl}/api/reports`);
      setReports(response.data);
    } catch (error) {
      console.error("❌ Error fetching reports:", error);
    }
  }, [backendUrl]);

  useEffect(() => {
    fetchReports();
    const interval = setInterval(fetchReports, 10000);
    return () => clearInterval(interval);
  }, [fetchReports]);

  return (
    <LoadScript googleMapsApiKey={apiKey}>
      <GoogleMap mapContainerStyle={containerStyle} center={center} zoom={10}>
        {reports.map((report) =>
          report.latitude !== 0 && report.longitude !== 0 ? (
            <Marker
              key={report.id}
              position={{
                lat: Number(report.latitude),
                lng: Number(report.longitude),
              }}
              title={`${report.description} (${report.status})`}
            />
          ) : null
        )}
      </GoogleMap>
    </LoadScript>
  );
}

export default MapPage;
