import React, { useState } from 'react';
import { Outlet } from 'react-router-dom';
import { Navbar } from '../components/Navbar';
import { Sidebar } from '../components/Sidebar';
import { useApp } from '../context/AppContext';

export const CandidateLayout: React.FC = () => {
  const [mobileSidebarOpen, setMobileSidebarOpen] = useState(false);
  const { currentRole, setRole } = useApp();

  // Ensure role is candidate when accessing candidate layout
  if (currentRole !== 'candidate') {
    setRole('candidate');
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
