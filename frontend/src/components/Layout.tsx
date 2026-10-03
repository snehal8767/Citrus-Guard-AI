// App shell: sidebar nav + top bar + outlet.
import { Link, NavLink, useNavigate } from "react-router-dom";
import { getToken, setToken } from "../api/client";

const NAV = [
  { to: "/", label: "Dashboard" },
  { to: "/map", label: "GIS Map" },
  { to: "/drone", label: "Drone Mission" },
  { to: "/analyze", label: "AI Analysis" },
  { to: "/sensors", label: "Sensors" },
  { to: "/alerts", label: "Alert Center" },
  { to: "/interventions", label: "Intervention" },
  { to: "/history", label: "History" },
  { to: "/reports", label: "Reports" },
  { to: "/console", label: "Command Console" },
];

export default function Layout({ children }: { children: React.ReactNode }) {
  const navigate = useNavigate();
  const loggedIn = !!getToken();

  const logout = () => {
    setToken(null);
    navigate("/login");
  };

  return (
    <div className="min-h-screen">
      <header className="sticky top-0 z-10 border-b border-leaf-100 bg-leaf-950 text-white">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3">
          <Link to="/" className="flex items-center gap-2">
            <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-citrus-500 text-lg font-bold text-leaf-950">
              C
            </span>
            <span className="text-lg font-bold">
              CitrusGuard<span className="text-citrus-400">AI</span>
            </span>
          </Link>
          <div className="flex items-center gap-3 text-sm">
            <span className="hidden rounded-full bg-leaf-800 px-2.5 py-0.5 text-xs sm:inline">
              Vidarbha Orange Estate · 50 ac · Demo
            </span>
            {loggedIn ? (
              <button onClick={logout} className="rounded-lg bg-leaf-800 px-3 py-1.5 font-semibold hover:bg-leaf-700">
                Logout
              </button>
            ) : (
              <Link to="/login" className="rounded-lg bg-citrus-500 px-3 py-1.5 font-semibold text-leaf-950 hover:bg-citrus-400">
                Login
              </Link>
            )}
          </div>
        </div>
      </header>
      <div className="mx-auto flex max-w-7xl gap-6 px-4 py-6">
        <nav className="hidden w-52 shrink-0 md:block">
          <div className="sticky top-20 space-y-1">
            {NAV.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                end={item.to === "/"}
                className={({ isActive }) =>
                  `block rounded-lg px-3 py-2 text-sm font-medium transition ${
                    isActive ? "bg-leaf-600 text-white" : "text-leaf-800 hover:bg-leaf-100"
                  }`
                }
              >
                {item.label}
              </NavLink>
            ))}
          </div>
        </nav>
        <main className="min-w-0 flex-1">
          {/* Mobile nav */}
          <div className="mb-4 flex flex-wrap gap-2 md:hidden">
            {NAV.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                end={item.to === "/"}
                className={({ isActive }) =>
                  `rounded-lg px-2.5 py-1.5 text-xs font-medium ${
                    isActive ? "bg-leaf-600 text-white" : "bg-white text-leaf-800"
                  }`
                }
              >
                {item.label}
              </NavLink>
            ))}
          </div>
          {children}
        </main>
      </div>
      <footer className="border-t border-leaf-100 bg-white py-4 text-center text-xs text-gray-500">
        CitrusGuardAI · Demo prototype — AI outputs are deterministic demo values, not field-validated.
      </footer>
    </div>
  );
}
