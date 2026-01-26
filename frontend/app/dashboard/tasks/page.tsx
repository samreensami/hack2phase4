import { Suspense } from "react";
import { TaskRead } from "../../../lib/generated/task_types";
import TasksContent from "./TasksContent";

// Force this page to be dynamic (SSR) - no static prerendering
export const dynamic = 'force-dynamic';

// Server component that handles initial data fetch
async function getInitialTasks() {
  // Only run on the server during SSR, skip during build
  if (typeof window !== 'undefined') {
    return [];
  }

  try {
    // Import here to avoid bundling issues during build
    const { taskAPI } = await import("../../../lib/api-service");

    // During build, return empty array
    if (process.env.NODE_ENV === 'production' && !process.env.VERCEL) {
      return [];
    }

    const data = await taskAPI.getTasks();
    return data || [];
  } catch (err) {
    console.error("Failed to fetch initial tasks:", err);
    return [];
  }
}

export default async function TasksPage() {
  const initialTasks = await getInitialTasks();

  return (
    <Suspense fallback={<p className="text-emerald-200">Loading tasks...</p>}>
      <TasksContent initialTasks={initialTasks} />
    </Suspense>
  );
}