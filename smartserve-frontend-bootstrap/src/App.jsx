import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import ReportPage from "./pages/ReportPage";
import MapPage from "./pages/MapPage";

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/report" element={<ReportPage />} />
        <Route path="/map" element={<MapPage />} />
      </Routes>
    </Router>
  );
}
