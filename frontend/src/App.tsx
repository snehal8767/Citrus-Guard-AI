// Router + auth guard.
import { Navigate, Route, Routes } from "react-router-dom";
import Layout from "./components/Layout";
import { getToken } from "./api/client";
import AIAnalysis from "./pages/AIAnalysis";
import Alerts from "./pages/Alerts";
import ConsolePage from "./pages/ConsolePage";
import Dashboard from "./pages/Dashboard";
import DroneMission from "./pages/DroneMission";
import History from "./pages/History";
import Interventions from "./pages/Interventions";
import Login from "./pages/Login";
import MapPage from "./pages/MapPage";
import Reports from "./pages/Reports";
import Sensors from "./pages/Sensors";

function RequireAuth({ children }: { children: JSX.Element }) {
  if (!getToken()) return <Navigate to="/login" replace />;
  return children;
}

export default function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/" element={<RequireAuth><Dashboard /></RequireAuth>} />
        <Route path="/map" element={<RequireAuth><MapPage /></RequireAuth>} />
        <Route path="/drone" element={<RequireAuth><DroneMission /></RequireAuth>} />
        <Route path="/analyze" element={<RequireAuth><AIAnalysis /></RequireAuth>} />
        <Route path="/sensors" element={<RequireAuth><Sensors /></RequireAuth>} />
        <Route path="/alerts" element={<RequireAuth><Alerts /></RequireAuth>} />
        <Route path="/interventions" element={<RequireAuth><Interventions /></RequireAuth>} />
        <Route path="/history" element={<RequireAuth><History /></RequireAuth>} />
        <Route path="/reports" element={<RequireAuth><Reports /></RequireAuth>} />
        <Route path="/console" element={<RequireAuth><ConsolePage /></RequireAuth>} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Layout>
  );
}
