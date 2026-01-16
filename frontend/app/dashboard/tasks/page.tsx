"use client";

import { useEffect, useState, useRef } from "react";
import { useSearchParams } from "next/navigation";
import type { TaskRead } from "../../../lib/generated/task_types";
import { taskAPI } from "../../../lib/api-service";

export default function TasksPage() {
  const [tasks, setTasks] = useState<TaskRead[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const searchParams = useSearchParams();

  const intervalRef = useRef<NodeJS.Timeout>();

  useEffect(() => {
    const loadTasks = async () => {
      try {
        const data = await taskAPI.getTasks();
        setTasks(data || []);
        setError(null);
      } catch (err: any) {
        console.error("Failed to load tasks:", err);
        if (err.response?.status === 401) {
          setError("You must be logged in to view your tasks.");
        } else {
          setError("Failed to load tasks. Please try again.");
        }
      } finally {
        setLoading(false);
      }
    };

    loadTasks();

    // Poll every 10 seconds for live updates from chat/tools
    intervalRef.current = setInterval(loadTasks, 10000);

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, []);

  if (loading) return <p className="text-emerald-200">Loading tasks...</p>;

  const handleRefresh = () => {
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
    }
    setLoading(true);
    setError(null);
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center mb-4">
  <h2 className="text-3xl font-bold">My Tasks</h2>
  <button
    onClick={handleRefresh}
    className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 rounded-lg text-white font-medium flex items-center gap-2"
    disabled={loading}
  >
    {loading ? (
      <>
        <span className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></span>
        Refreshing...
      </>
    ) : (
      'Refresh'
    )}
  </button>
</div>

      {/* Quick Add Task */}
      <AddTaskForm onCreated={(t) => setTasks((prev) => [t, ...prev])} />

      {error ? (
        <div className="text-red-400 text-sm bg-red-900/30 p-3 rounded border border-red-700/50">{error}</div>
      ) : (
        (() => {
          const filter = searchParams?.get('filter');
          let filtered = tasks;

          if (filter === 'completed') filtered = tasks.filter((t) => t.status === true);
          if (filter === 'pending') filtered = tasks.filter((t) => t.status === false);

          if (filtered.length === 0) {
            return (
              <p className="text-emerald-300">No tasks found for this filter. Try creating a new task using the form above.</p>
            );
          }

          return (
            <ul className="space-y-3">
              {filtered.map((task) => (
                <TaskItem
                  key={task.id}
                  task={task}
                  onUpdated={(u) => setTasks((prev) => prev.map((t) => (t.id === u.id ? u : t)))}
                />
              ))}
            </ul>
          );
        })()
      )}
    </div>
  );
}

function AddTaskForm({ onCreated }: { onCreated?: (task: TaskRead) => void }) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSubmitting(true);
    try {
      const newTask = await taskAPI.createTask({ title, description, status: false });
      setTitle('');
      setDescription('');
      onCreated?.(newTask);
      // notify other parts of the app that tasks changed (dashboard stats)
      if (typeof window !== 'undefined') window.dispatchEvent(new CustomEvent('tasks:changed'));
    } catch (err: any) {
      console.error('Failed to create task', err);
      if (err.response?.status === 401) setError('You must be logged in to create tasks.');
      else setError('Failed to create task.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleCreate} className="space-y-2">
      {error && <div className="text-red-400 text-sm bg-red-900/30 p-2 rounded">{error}</div>}
      <div className="flex gap-2">
        <input value={title} onChange={(e) => setTitle(e.target.value)} placeholder="Task title" required className="flex-1 px-3 py-2 rounded bg-emerald-800/30 placeholder-emerald-400" />
        <input value={description} onChange={(e) => setDescription(e.target.value)} placeholder="Short description" className="flex-1 px-3 py-2 rounded bg-emerald-800/30 placeholder-emerald-400" />
        <button disabled={submitting} type="submit" className="px-4 py-2 bg-emerald-500 rounded text-white font-bold">{submitting ? 'Adding...' : 'Add'}</button>
      </div>
    </form>
  );
}

function TaskItem({ task, onUpdated }: { task: TaskRead; onUpdated?: (task: TaskRead) => void }) {
  const [isEditing, setIsEditing] = useState(false);
  const [title, setTitle] = useState(task.title);
  const [description, setDescription] = useState(task.description ?? '');
  const [status, setStatus] = useState<boolean>(task.status);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // keep local fields in sync if parent updates
  useEffect(() => {
    setTitle(task.title);
    setDescription(task.description ?? '');
    setStatus(task.status);
  }, [task.id, task.title, task.description, task.status]);

  const handleSave = async () => {
    setLoading(true);
    setError(null);
    try {
      const updated = await taskAPI.updateTask(task.id, { title, description, status });
      onUpdated?.(updated);
      // notify dashboard to refresh stats
      if (typeof window !== 'undefined') window.dispatchEvent(new CustomEvent('tasks:changed'));
      setIsEditing(false);
    } catch (err: any) {
      console.error('Failed to update task', err);
      setError(err.response?.data?.detail || 'Failed to update task');
    } finally {
      setLoading(false);
    }
  };

  return (
    <li className="p-4 bg-emerald-800/40 rounded-xl border border-emerald-700">
      {isEditing ? (
        <div className="space-y-2">
          {error && <div className="text-red-400 text-sm">{error}</div>}
          <input value={title} onChange={(e) => setTitle(e.target.value)} className="w-full px-3 py-2 rounded bg-emerald-900/20" />
          <input value={description} onChange={(e) => setDescription(e.target.value)} className="w-full px-3 py-2 rounded bg-emerald-900/20" />
          <label className="flex items-center gap-2 text-sm">
            <input type="checkbox" checked={status} onChange={(e) => setStatus(e.target.checked)} />
            Completed
          </label>

          <div className="flex gap-2">
            <button onClick={handleSave} disabled={loading} className="px-3 py-1 bg-emerald-500 rounded text-white">{loading ? 'Saving...' : 'Save'}</button>
            <button onClick={() => { setIsEditing(false); setError(null); }} className="px-3 py-1 bg-emerald-700 rounded text-white">Cancel</button>
          </div>
        </div>
      ) : (
        <div>
          <div className="flex justify-between items-start">
            <div>
              <h3 className="font-semibold">{task.title}</h3>
              <p className="text-emerald-300 text-sm">{task.description}</p>
            </div>
            <div className="flex gap-2">
              <button onClick={() => setIsEditing(true)} className="px-2 py-1 bg-emerald-600 rounded text-sm">Edit</button>
            </div>
          </div>
          <div className="mt-2 text-sm text-emerald-300">{task.status ? 'Completed' : 'Pending'}</div>
        </div>
      )}
    </li>
  );
}

