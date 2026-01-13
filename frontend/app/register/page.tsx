"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { api } from "../../lib/api-service";

export default function RegisterPage() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [success, setSuccess] = useState(false);
    const router = useRouter();

    const handleRegister = async (e: React.FormEvent) => {
        e.preventDefault();
        setError("");

        try {
            // CSRF token fetch karna zaruri hai agar backend require karta hai
            const csrfRes = await api.get("/api/auth/csrf");
            const csrfToken = csrfRes.data.csrfToken;

            await api.post(
                "/auth/register",
                { email, password },
                {
                    headers: {
                        "X-CSRF-Token": csrfToken,
                        "Content-Type": "application/json",
                    },
                }
            );

            setSuccess(true);
            setTimeout(() => router.push("/login"), 2000);
        } catch (err: any) {
            console.error(err);
            // Axios error ka message properly show karna
            if (err.response?.data?.detail) {
                setError(err.response.data.detail);
            } else {
                setError(err.message || "Registration failed");
            }
        }
    };

    return (
        <div className="flex min-h-screen flex-col items-center justify-center p-24 bg-emerald-950">
            <div className="w-full max-w-md space-y-8 bg-emerald-900 p-8 rounded-3xl shadow-lg border border-emerald-800">
                <h2 className="text-center text-4xl font-bold tracking-tight text-white">Task App - Register</h2>
                <form className="mt-8 space-y-6" onSubmit={handleRegister}>
                    {error && <div className="text-red-400 text-sm text-center bg-red-900/30 p-2 rounded border border-red-700/50">{error}</div>}
                    {success && <div className="text-emerald-300 text-sm text-center bg-emerald-900/30 p-2 rounded border border-emerald-700/50">Registration successful! Redirecting...</div>}
                    <div className="rounded-md shadow-sm -space-y-px">
                        <input
                            type="email"
                            required
                            className="appearance-none rounded-none relative block w-full px-4 py-3 border border-emerald-700/50 placeholder-emerald-500 text-emerald-100 bg-emerald-800/50 rounded-t-md focus:outline-none focus:ring-emerald-500 focus:border-emerald-500 sm:text-sm"
                            placeholder="Email address"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                        />
                        <input
                            type="password"
                            required
                            className="appearance-none rounded-none relative block w-full px-4 py-3 border border-emerald-700/50 placeholder-emerald-500 text-emerald-100 bg-emerald-800/50 rounded-b-md focus:outline-none focus:ring-emerald-500 focus:border-emerald-500 sm:text-sm"
                            placeholder="Password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                        />
                    </div>
                    <div>
                        <button type="submit" className="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-bold rounded-2xl text-white bg-emerald-500 hover:bg-emerald-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emerald-500 transition-colors">
                            Create Account
                        </button>
                    </div>
                </form>
                <div className="text-center text-sm text-emerald-300/80">
                    Already have an account? <Link href="/login" className="font-bold hover:underline text-emerald-200">Log in here</Link>
                </div>
            </div>
        </div>
    );
}
