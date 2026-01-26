"use client";

import { useEffect, useState, useRef } from "react";
import { useSearchParams } from "next/navigation";
import type { TaskRead } from "../../../lib/generated/task_types";
import { taskAPI } from "../../../lib/api-service";

export default function TasksContent({ initialTasks }: { initialTasks: TaskRead[] }) {
  const [tasks, setTasks] = useState<TaskRead[]>(initialTasks);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const searchParams = useSearchParams();

  const intervalRef = useRef<NodeJS.Timeout | null>(null);

  const loadTasks = async () => {
    try {
      setLoading(true);
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

  useEffect(() => {
    // Only run client-side effects in browser
    if (typeof window === 'undefined') return;

    // Use initial tasks from server, then set up polling
    // Poll every 10 seconds for live updates
    intervalRef.current = setInterval(loadTasks, 10000);

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, []);

  const handleRefresh = () => {
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
    }

    loadTasks();

    intervalRef.current = setInterval(loadTasks, 10000);
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-3xl font-bold">My Tasks</h2>

        <button
          onClick={handleRefresh}
          disabled={loading}
          className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 rounded-lg text-white font-medium flex items-center gap-2"
        >
          {loading ? (
            <>
              <span className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></span>
              Refreshing...
            </>
          ) : (
            "Refresh"
          )}
        </button>
      </div>

      {/* Add Task */}
      <AddTaskForm
        onCreated={(task) => setTasks((prev) => [task, ...prev])}
      />

      {error ? (
        <div className="text-red-400 text-sm bg-red-900/30 p-3 rounded border border-red-700/50">
          {error}
        </div>
      ) : (
        (() => {
          const filter = searchParams?.get("filter");
          let filtered = tasks;

          if (filter === "completed")
            filtered = tasks.filter((t) => t.status === true);

          if (filter === "pending")
            filtered = tasks.filter((t) => t.status === false);

          if (filtered.length === 0) {
            return (
              <p className="text-emerald-300">
                No tasks found for this filter.
              </p>
            );
          }

          return (
            <ul className="space-y-3">
              {filtered.map((task) => (
                <TaskItem
                  key={task.id}
                  task={task}
                  onUpdated={(updated) =>
                    setTasks((prev) =>
                      prev.map((t) =>
                        t.id === updated.id ? updated : t
                      )
                    )
                  }
                  onDeleted={(taskId) =>
                    setTasks((prev) => prev.filter((t) => t.id !== taskId))
                  }
                />
              ))}
            </ul>
          );
        })()
      )}
    </div>
  );
}

/* ============================
   Add Task Component
============================ */

function AddTaskForm({
  onCreated,
}: {
  onCreated?: (task: TaskRead) => void;
}) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    setError(null);

    try {
      const newTask = await taskAPI.createTask({
        title,
        description,
        status: false,
      });

      setTitle("");
      setDescription("");
      onCreated?.(newTask);

      window.dispatchEvent(new CustomEvent("tasks:changed"));
    } catch (err: any) {
      console.error(err);

      if (err.response?.status === 401) {
        setError("You must be logged in to create tasks.");
      } else {
        setError("Failed to create task.");
      }
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleCreate} className="space-y-2">
      {error && (
        <div className="text-red-400 text-sm bg-red-900/30 p-2 rounded">
          {error}
        </div>
      )}

      <div className="flex gap-2">
        <input
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Task title"
          required
          className="flex-1 px-3 py-2 rounded bg-emerald-800/30 placeholder-emerald-400"
        />

        <input
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Short description"
          className="flex-1 px-3 py-2 rounded bg-emerald-800/30 placeholder-emerald-400"
        />

        <button
          disabled={submitting}
          type="submit"
          className="px-4 py-2 bg-emerald-500 rounded text-white font-bold"
        >
          {submitting ? "Adding..." : "Add"}
        </button>
      </div>
    </form>
  );
}

/* ============================
   Task Item
============================ */

function TaskItem({
  task,
  onUpdated,
  onDeleted,
}: {
  task: TaskRead;
  onUpdated?: (task: TaskRead) => void;
  onDeleted?: (taskId: number) => void;
}) {
  const [isEditing, setIsEditing] = useState(false);
  const [title, setTitle] = useState(task.title);
  const [description, setDescription] = useState(task.description ?? "");
  const [status, setStatus] = useState(task.status);
  const [loading, setLoading] = useState(false);
  const [deleting, setDeleting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setTitle(task.title);
    setDescription(task.description ?? "");
    setStatus(task.status);
  }, [task]);

  const handleSave = async () => {
    setLoading(true);
    setError(null);

    try {
      const updated = await taskAPI.updateTask(task.id, {
        title,
        description,
        status,
      });

      onUpdated?.(updated);
      window.dispatchEvent(new CustomEvent("tasks:changed"));
      setIsEditing(false);
    } catch (err: any) {
      setError(err.response?.data?.detail || "Update failed");
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!confirm("Are you sure you want to delete this task?")) return;

    setDeleting(true);
    setError(null);

    try {
      await taskAPI.deleteTask(task.id);
      onDeleted?.(task.id);
      window.dispatchEvent(new CustomEvent("tasks:changed"));
    } catch (err: any) {
      setError(err.response?.data?.detail || "Delete failed");
    } finally {
      setDeleting(false);
    }
  };

  return (
    <li className="p-4 bg-emerald-800/40 rounded-xl border border-emerald-700">
      {isEditing ? (
        <div className="space-y-2">
          {error && <div className="text-red-400 text-sm">{error}</div>}

          <input
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="w-full px-3 py-2 rounded bg-emerald-900/20"
          />

          <input
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="w-full px-3 py-2 rounded bg-emerald-900/20"
          />

          <label className="flex items-center gap-2 text-sm">
            <input
              type="checkbox"
              checked={status}
              onChange={(e) => setStatus(e.target.checked)}
            />
            Completed
          </label>

          <div className="flex gap-2">
            <button
              onClick={handleSave}
              disabled={loading}
              className="px-3 py-1 bg-emerald-500 rounded text-white"
            >
              {loading ? "Saving..." : "Save"}
            </button>

            <button
              onClick={() => setIsEditing(false)}
              className="px-3 py-1 bg-emerald-700 rounded text-white"
            >
              Cancel
            </button>
          </div>
        </div>
      ) : (
        <div>
          <h3 className="font-semibold">{task.title}</h3>
          <p className="text-emerald-300 text-sm">{task.description}</p>
          <div className="mt-2 text-sm text-emerald-300">
            {task.status ? "Completed" : "Pending"}
          </div>

          <div className="mt-2 flex gap-2">
            <button
              onClick={() => setIsEditing(true)}
              className="px-2 py-1 bg-emerald-600 rounded text-sm hover:bg-emerald-500"
            >
              Edit
            </button>
            <button
              onClick={handleDelete}
              disabled={deleting}
              className="px-2 py-1 bg-red-600 rounded text-sm hover:bg-red-500 disabled:opacity-50"
            >
              {deleting ? "Deleting..." : "Delete"}
            </button>
          </div>
        </div>
      )}
    </li>
  );
}