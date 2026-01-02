"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { api } from "../../lib/api-service";
import Link from "next/link";

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
            await api.post("/auth/register", { email, password });
            setSuccess(true);
            setTimeout(() => router.push("/login"), 2000);
        } catch (err: any) {
            setError(err.message || "Registration failed");
        }
    };

    return (
        <div className="flex min-h-screen flex-col items-center justify-center p-24">
            <div className="w-full max-w-md space-y-8 bg-white p-8 rounded-xl shadow-md border">
                <h2 className="text-center text-3xl font-bold tracking-tight text-gray-900">Task App - Register</h2>
                <form className="mt-8 space-y-6" onSubmit={handleRegister}>
                    {error && <div className="text-red-500 text-sm text-center bg-red-50 p-2 rounded">{error}</div>}
                    {success && <div className="text-green-500 text-sm text-center bg-green-50 p-2 rounded">Registration successful! Redirecting...</div>}
                    <div className="rounded-md shadow-sm -space-y-px">
                        <input
                            type="email"
                            required
                            className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                            placeholder="Email address"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                        />
                        <input
                            type="password"
                            required
                            className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                            placeholder="Password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                        />
                    </div>
                    <div>
                        <button type="submit" className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500">
                            Create Account
                        </button>
                    </div>
                </form>
                <div className="text-center text-sm">
                    Already have an account? <Link href="/login" className="text-blue-600 hover:underline">Log in here</Link>
                </div>
            </div>
        </div>
    );
}
