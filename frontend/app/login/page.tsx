"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { api } from "../../lib/api-service";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const router = useRouter();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    try {
      // 🔐 Get CSRF token
      const csrfRes = await api.get("/api/auth/csrf");
      const csrfToken = csrfRes.data.csrfToken;

      // 🧾 FastAPI expects form data, not JSON
      const formData = new URLSearchParams();
      formData.append("username", email);
      formData.append("password", password);

      const res = await api.post("/auth/login", formData, {
        headers: {
          "X-CSRF-Token": csrfToken,
          "Content-Type": "application/x-www-form-urlencoded",
        },
      });

      // Persist token for authenticated requests
      if (typeof window !== 'undefined' && res?.data?.access_token) {
        localStorage.setItem('token', res.data.access_token);
      }

      router.push("/dashboard");
    } catch (err: any) {
      console.error(err);
      if (err.response?.data?.detail) {
        setError(err.response.data.detail);
      } else {
        setError(err.message || "Login failed");
      }
    }
  };

  return (
    <div className="flex min-h-screen flex-col items-center justify-center p-24 bg-emerald-950">
      <div className="w-full max-w-md space-y-8 bg-emerald-900 p-8 rounded-3xl shadow-lg border border-emerald-800">
        <h2 className="text-center text-4xl font-bold tracking-tight text-white">
          TaskSphere - Login
        </h2>

        <form className="mt-8 space-y-6" onSubmit={handleLogin}>
          {error && (
            <div className="text-red-400 text-sm text-center bg-red-900/30 p-2 rounded border border-red-700/50">
              {error}
            </div>
          )}

          <div className="rounded-md shadow-sm -space-y-px">
            <input
              type="email"
              required
              className="appearance-none block w-full px-4 py-3 border border-emerald-700/50 placeholder-emerald-500 text-emerald-100 bg-emerald-800/50 rounded-t-md focus:outline-none focus:ring-emerald-500 focus:border-emerald-500 sm:text-sm"
              placeholder="Email address"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />

            <input
              type="password"
              required
              className="appearance-none block w-full px-4 py-3 border border-emerald-700/50 placeholder-emerald-500 text-emerald-100 bg-emerald-800/50 rounded-b-md focus:outline-none focus:ring-emerald-500 focus:border-emerald-500 sm:text-sm"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>

          <button
            type="submit"
            className="w-full py-3 px-4 text-sm font-bold rounded-2xl text-white bg-emerald-500 hover:bg-emerald-600 transition-colors"
          >
            Login
          </button>
        </form>

        <div className="text-center text-sm text-emerald-300/80">
          Do not have an account?{" "}
          <Link href="/register" className="font-bold hover:underline text-emerald-200">
            Register here
          </Link>
        </div>
      </div>
    </div>
  );
}
