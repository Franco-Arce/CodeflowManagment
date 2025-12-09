import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation, Navigate } from 'react-router-dom';
import { LayoutDashboard, AlertTriangle, LogOut } from 'lucide-react';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Incidents from './pages/Incidents';
import { cn } from './lib/utils';

const SidebarItem = ({ icon: Icon, label, to }) => {
  const location = useLocation();
  const isActive = location.pathname === to;

  return (
    <Link
      to={to}
      className={cn(
        "flex items-center gap-3 rounded-lg px-3 py-2 text-slate-500 transition-all hover:text-slate-900",
        isActive && "bg-slate-100 text-slate-900"
      )}
    >
      <Icon className="h-4 w-4" />
      {label}
    </Link>
  );
};

const Layout = ({ children }) => {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  return (
    <div className="grid min-h-screen w-full lg:grid-cols-[280px_1fr]">
      <div className="hidden border-r bg-slate-100/40 lg:block dark:bg-slate-800/40">
        <div className="flex h-full max-h-screen flex-col gap-2">
          <div className="flex h-[60px] items-center border-b px-6">
            <Link className="flex items-center gap-2 font-semibold" to="/">
              <span className="">Codeflow Mgmt</span>
            </Link>
          </div>
          <div className="flex-1 overflow-auto py-2">
            <nav className="grid items-start px-4 text-sm font-medium">
              <SidebarItem icon={LayoutDashboard} label="Dashboard" to="/" />
              <SidebarItem icon={AlertTriangle} label="Incidents" to="/incidents" />
            </nav>
          </div>
          <div className="mt-auto p-4">
            <button onClick={handleLogout} className="flex items-center gap-3 rounded-lg px-3 py-2 text-slate-500 transition-all hover:text-slate-900 w-full">
              <LogOut className="h-4 w-4" />
              Logout
            </button>
          </div>
        </div>
      </div>
      <div className="flex flex-col">
        <header className="flex h-14 lg:h-[60px] items-center gap-4 border-b bg-slate-100/40 px-6 dark:bg-slate-800/40">
          <div className="w-full flex-1">
            {/* Header content like search or user profile */}
          </div>
        </header>
        <main className="flex flex-1 flex-col gap-4 p-4 md:gap-8 md:p-6">
          {children}
        </main>
      </div>
    </div>
  );
};

// Helper to use navigate in Layout which is inside Router
const LayoutWrapper = ({ children }) => {
  // We need to use useNavigate here, but Layout is not yet inside Router in the main App return if we structure it wrong.
  // Actually, we can just put Layout inside Routes or wrap it.
  // Let's make Layout use children and be used in Route element.
  return <Layout>{children}</Layout>;
};

// We need a component that uses useNavigate for logout, so it must be inside Router.
// Let's redefine Layout to be used inside the Router context.
import { useNavigate } from 'react-router-dom';

const ProtectedRoute = ({ children }) => {
  const token = localStorage.getItem('token');
  if (!token) {
    return <Navigate to="/login" replace />;
  }
  return children;
};

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/" element={
          <ProtectedRoute>
            <LayoutWrapper><Dashboard /></LayoutWrapper>
          </ProtectedRoute>
        } />
        <Route path="/incidents" element={
          <ProtectedRoute>
            <LayoutWrapper><Incidents /></LayoutWrapper>
          </ProtectedRoute>
        } />
      </Routes>
    </Router>
  );
}
