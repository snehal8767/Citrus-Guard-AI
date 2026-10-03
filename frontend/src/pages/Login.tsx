// Login page: JWT auth against POST /auth/login.
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { api, setToken } from "../api/client";

export default function Login() {
  const navigate = useNavigate();
  const [username, setUsername] = useState("farmer");
  const [password, setPassword] = useState("farmer123");
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setBusy(true);
    setError(null);
    try {
      const res = await api.login(username, password);
      setToken(res.access_token);
      navigate("/");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Login failed");
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="mx-auto mt-10 max-w-md">
      <div className="card">
        <h1 className="text-2xl font-bold text-leaf-900">
          CitrusGuard<span className="text-citrus-500">AI</span>
        </h1>
        <p className="mt-1 text-sm text-gray-600">Smart orange orchard monitoring · Vidarbha, Maharashtra</p>
        <form onSubmit={submit} className="mt-6 space-y-4">
          <div>
            <label className="text-sm font-medium">Username</label>
            <input className="input mt-1" value={username} onChange={(e) => setUsername(e.target.value)} autoComplete="username" />
          </div>
          <div>
            <label className="text-sm font-medium">Password</label>
            <input
              className="input mt-1"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              autoComplete="current-password"
            />
          </div>
          {error && <div className="rounded-lg bg-red-50 p-2 text-sm text-red-700">{error}</div>}
          <button className="btn-primary w-full" disabled={busy}>
            {busy ? "Signing in…" : "Sign in"}
          </button>
        </form>
        <div className="mt-4 rounded-lg bg-leaf-50 p-3 text-xs text-gray-600">
          <div className="font-semibold text-leaf-800">Demo accounts</div>
          <div>farmer / farmer123 (farmer role)</div>
          <div>operator / operator123 (operator role)</div>
        </div>
      </div>
    </div>
  );
}
