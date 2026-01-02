"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { api, clearAuthToken } from "../../lib/api-service";
import { TaskRead } from "../../lib/generated/task_types";

export default function DashboardPage() {
    const [tasks, setTasks] = useState<TaskRead[]>([]);
    const [newTitle, setNewTitle] = useState("");
    const [isLoading, setIsLoading] = useState(true);
    const router = useRouter();

    useEffect(() => {
        fetchTasks();
    }, []);

    const fetchTasks = async () => {
        try {
            const data = await api.get("/tasks/");
            setTasks(data);
        } catch (err) {
            router.push("/login");
        } finally {
            setIsLoading(false);
        }
    };

    const addTask = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!newTitle) return;
        try {
            const newTask = await api.post("/tasks/", { title: newTitle });
            setTasks([newTask, ...tasks]);
            setNewTitle("");
        } catch (err) {
            alert("Failed to add task");
        }
    };

    const toggleTask = async (task: TaskRead) => {
        try {
            const updated = await api.put(`/tasks/${task.id}`, {
                title: task.title,
                status: !task.status
            });
            setTasks(tasks.map(t => t.id === task.id ? updated : t));
        } catch (err) {
            alert("Failed to update status");
        }
    };

    const deleteTask = async (id: number) => {
        try {
            await api.delete(`/tasks/${id}`);
            setTasks(tasks.filter(t => t.id !== id));
        } catch (err) {
            alert("Failed to delete task");
        }
    };

    const handleLogout = () => {
        clearAuthToken();
        router.push("/login");
    };

    if (isLoading) return <div className="p-24 text-center">Loading tasks...</div>;

    return (
        <div className="min-h-screen bg-gray-50 p-8 md:p-24">
            <div className="max-w-4xl mx-auto">
                <div className="flex justify-between items-center mb-12">
                    <h1 className="text-4xl font-bold text-gray-900 tracking-tight">Your Tasks</h1>
                    <button
                        onClick={handleLogout}
                        className="text-sm font-medium text-red-600 hover:text-red-800 border border-red-200 px-4 py-2 rounded-lg bg-white shadow-sm hover:shadow transition-all"
                    >
                        Logout
                    </button>
                </div>

                <div className="bg-white p-6 rounded-2xl shadow-sm border mb-8">
                    <form onSubmit={addTask} className="flex gap-4">
                        <input
                            type="text"
                            placeholder="What needs to be done?"
                            className="flex-1 px-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                            value={newTitle}
                            onChange={(e) => setNewTitle(e.target.value)}
                        />
                        <button
                            type="submit"
                            className="bg-blue-600 text-white px-8 py-3 rounded-xl font-semibold hover:bg-blue-700 shadow-lg shadow-blue-500/30 transition-all active:scale-95"
                        >
                            Add Task
                        </button>
                    </form>
                </div>

                <div className="space-y-4">
                    {tasks.length === 0 ? (
                        <div className="text-center py-12 text-gray-500 bg-white rounded-2xl border border-dashed">
                            No tasks yet. Add your first task above!
                        </div>
                    ) : (
                        tasks.map(task => (
                            <div key={task.id} className="group flex items-center justify-between bg-white p-5 rounded-xl shadow-sm border border-gray-100 hover:border-blue-200 hover:shadow-md transition-all">
                                <div className="flex items-center gap-4">
                                    <input
                                        type="checkbox"
                                        checked={task.status}
                                        onChange={() => toggleTask(task)}
                                        className="w-5 h-5 rounded-full border-gray-300 text-blue-600 focus:ring-blue-500 cursor-pointer"
                                    />
                                    <span className={`text-lg transition-all ${task.status ? 'line-through text-gray-400' : 'text-gray-700'}`}>
                                        {task.title}
                                    </span>
                                </div>
                                <button
                                    onClick={() => deleteTask(task.id)}
                                    className="opacity-0 group-hover:opacity-100 p-2 text-gray-400 hover:text-red-600 transition-all"
                                    title="Delete Task"
                                >
                                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                                    </svg>
                                </button>
                            </div>
                        ))
                    )}
                </div>
            </div>
        </div>
    );
}
