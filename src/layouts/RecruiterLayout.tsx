import React, { useEffect, useState } from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { Navbar } from '../components/Navbar';
import { Sidebar } from '../components/Sidebar';
import { useApp } from '../context/AppContext';

export const RecruiterLayout: React.FC = () => {
  const [mobileSidebarOpen, setMobileSidebarOpen] = useState(false);
  const { setRole, recruiterAuthenticated } = useApp();

  useEffect(() => {
    setRole('recruiter');
  }, [setRole]);

  if (!recruiterAuthenticated) {
    return <Navigate to="/recruiter/signin" replace />;
  }

  return (
    <div className="min-h-screen bg-slate-50/70 flex flex-col font-sans text-slate-900">
      <Navbar
        showSidebarToggle={true}
        onToggleMobileSidebar={() => setMobileSidebarOpen(!mobileSidebarOpen)}
      />

      <div className="flex-1 flex max-w-7xl w-full mx-auto">
        <Sidebar
          isOpenMobile={mobileSidebarOpen}
          onCloseMobile={() => setMobileSidebarOpen(false)}
        />

        <main className="flex-1 p-4 sm:p-6 lg:p-8 max-w-full overflow-hidden">
          <Outlet />
        </main>
      </div>
    </div>
  );
};


