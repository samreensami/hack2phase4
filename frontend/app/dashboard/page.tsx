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

    if (isLoading) return <div className="p-24 text-center bg-emerald-950 min-h-screen text-emerald-200 font-bold">Loading tasks...</div>;

    return (
        <div className="min-h-screen bg-emerald-950 flex flex-col md:flex-row">
            {/* Sidebar-style Header for Mobile or Desktop Sidebar */}
            <div className="w-full md:w-64 bg-emerald-800 text-emerald-100 p-8 flex flex-col justify-between shadow-xl">
                <div>
                    <h2 className="text-2xl font-bold mb-8">Task App</h2>
                    <nav className="space-y-4">
                        <div className="bg-emerald-700/30 p-3 rounded-lg font-bold">Dashboard</div>
                    </nav>
                </div>
                <button
                    onClick={handleLogout}
                    className="mt-8 bg-emerald-500 text-white py-3 px-4 rounded-2xl font-bold shadow-lg hover:bg-emerald-600 transition-all text-center"
                >
                    Logout
                </button>
            </div>

            {/* Main Content */}
            <div className="flex-1 p-8 md:p-16 overflow-y-auto">
                <div className="max-w-4xl mx-auto">
                    <header className="mb-12">
                        <h1 className="text-4xl font-bold text-white tracking-tight">Your Daily Focus</h1>
                        <p className="text-emerald-300/80 mt-2">Manage your tasks in the Sober Emerald workspace</p>
                    </header>

                    <div className="bg-emerald-900 p-6 rounded-3xl shadow-lg border border-emerald-800 mb-8">
                        <form onSubmit={addTask} className="flex flex-col sm:flex-row gap-4">
                            <input
                                type="text"
                                placeholder="What's the next big thing?"
                                className="flex-1 px-4 py-3 rounded-2xl border border-emerald-700/50 bg-emerald-800/50 text-emerald-100 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-all"
                                value={newTitle}
                                onChange={(e) => setNewTitle(e.target.value)}
                            />
                            <button
                                type="submit"
                                className="bg-emerald-500 text-white px-8 py-3 rounded-2xl font-bold hover:bg-emerald-600 shadow-lg shadow-emerald-500/30 transition-all active:scale-95"
                            >
                                Add Task
                            </button>
                        </form>
                    </div>

                    <div className="space-y-4">
                        {tasks.length === 0 ? (
                            <div className="text-center py-12 text-emerald-400/50 bg-emerald-900/50 rounded-3xl border-2 border-dashed border-emerald-700/30">
                                Peaceful space. No tasks yet.
                            </div>
                        ) : (
                            tasks.map(task => (
                                <div key={task.id} className="group flex items-center justify-between bg-emerald-900 p-5 rounded-2xl shadow-md border border-emerald-800/50 hover:border-emerald-600/30 hover:shadow-lg transition-all">
                                    <div className="flex items-center gap-4">
                                        <input
                                            type="checkbox"
                                            checked={task.status}
                                            onChange={() => toggleTask(task)}
                                            className="w-6 h-6 rounded-full border-emerald-600 text-emerald-500 focus:ring-emerald-500 cursor-pointer"
                                        />
                                        <span className={`text-lg font-medium transition-all ${task.status ? 'line-through text-emerald-400/50' : 'text-emerald-100'}`}>
                                            {task.title}
                                        </span>
                                    </div>
                                    <button
                                        onClick={() => deleteTask(task.id)}
                                        className="p-2 text-emerald-400/50 hover:text-red-400 transition-all"
                                        title="Delete Task"
                                    >
                                        <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                                        </svg>
                                    </button>
                                </div>
                            ))
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}
