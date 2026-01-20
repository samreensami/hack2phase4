'use client';

import React from 'react';

export default function LogoutButton() {
  const handleLogout = () => {
    // Add your logout logic here
    if (typeof window !== 'undefined') {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
  };

  return (
    <button
      onClick={handleLogout}
      className="w-full text-left px-4 py-2 text-sm text-red-400 hover:text-red-300 transition"
    >
      🚪 Logout
    </button>
  );
}