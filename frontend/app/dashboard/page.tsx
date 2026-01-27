import React, { Suspense } from 'react';
import DashboardContent from './DashboardContent';

// Force this page to be dynamic (SSR) - no static prerendering
export const dynamic = 'force-dynamic';

// Server component that handles initial data fetch
async function getInitialStats() {
  // Only run on the server during SSR, skip during build
  if (typeof window !== 'undefined') {
    return null;
  }

  try {
    // FIX: api-service default export hai, is liye .default use karna hoga
    const apiModule = await import('../../lib/api-service');
    const api = apiModule.default;

    // During build, return fallback data
    if (process.env.NODE_ENV === 'production' && !process.env.VERCEL) {
      return { tasksCompleted: 0, pendingTasks: 0, upcomingDeadlines: 0 };
    }

    // FIX: Route ko /api/ ke sath update kiya
    const response = await api.get('/api/dashboard/stats');
    const data = response.data;

    if (
      typeof data?.tasksCompleted === 'number' &&
      typeof data?.pendingTasks === 'number' &&
      typeof data?.upcomingDeadlines === 'number'
    ) {
      return data;
    } else {
      return { tasksCompleted: 24, pendingTasks: 5, upcomingDeadlines: 3 };
    }
  } catch (err) {
    console.error('Failed to fetch initial stats:', err);
    return { tasksCompleted: 24, pendingTasks: 5, upcomingDeadlines: 3 };
  }
}

export default async function DashboardPage() {
  const initialStats = await getInitialStats();

  return (
    <div className="space-y-6">
      {/* FIX: Yahan se Dashboard heading delete kar di taake double na ho */}
      
      <Suspense fallback={
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div className="p-6 bg-emerald-800/50 rounded-2xl shadow-lg">
            <h3 className="text-xl font-semibold">Tasks Completed</h3>
            <p className="text-emerald-200 mt-2">Loading...</p>
          </div>
          <div className="p-6 bg-emerald-800/50 rounded-2xl shadow-lg">
            <h3 className="text-xl font-semibold">Pending Tasks</h3>
            <p className="text-emerald-200 mt-2">Loading...</p>
          </div>
          <div className="p-6 bg-emerald-800/50 rounded-2xl shadow-lg">
            <h3 className="text-xl font-semibold">Upcoming Deadlines</h3>
            <p className="text-emerald-200 mt-2">Loading...</p>
          </div>
        </div>
      }>
        <DashboardContent initialStats={initialStats} />
      </Suspense>
    </div>
  );
}