// frontend/app/task/page.tsx
'use client';

import React, { useEffect, useState } from 'react';
import { taskAPI } from '../../lib/api-service';

interface Task {
  id: number;
  title: string;
  completed: boolean;
}

export default function MyTasksPageContent() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchTasks = async () => {
      try {
        const response = await taskAPI.getTasks(); // backend /task endpoint
        setTasks(response);
      } catch (err) {
        console.error('Error fetching tasks:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchTasks();
  }, []);

  if (loading) return <p>Loading tasks...</p>;

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Tasks</h1>
      {tasks.length === 0 ? (
        <p>No tasks found.</p>
      ) : (
        <ul className="space-y-2">
          {tasks.map(task => (
            <li key={task.id} className="p-2 border rounded">
              <span className={task.completed ? 'line-through' : ''}>
                {task.title}
              </span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};