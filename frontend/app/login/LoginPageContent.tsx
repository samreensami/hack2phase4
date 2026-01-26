"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import api from "../../lib/api-service";

export default function LoginPageContent() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const router = useRouter();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    try {
      // ✅ FastAPI login (NO CSRF)
      const formData = new URLSearchParams();
      formData.append("username", email);
      formData.append("password", password);

      const res = await api.post(
        "/auth/login",
        formData,
        {
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
        }
      );

      const token = res.data?.access_token;

      if (!token) {
        throw new Error("Token not returned from backend");
      }

      // ✅ save token
      localStorage.setItem("token", token);

      router.push("/dashboard");

    } catch (err: any) {
      console.error(err);

      if (err.response?.data?.detail) {
        setError(err.response.data.detail);
      } else {
        setError("Invalid email or password");
      }
    }
  };

  return (
    <div className="flex min-h-screen flex-col items-center justify-center p-24 bg-emerald-950">
      <div className="w-full max-w-md space-y-8 bg-emerald-900 p-8 rounded-3xl shadow-lg border border-emerald-800">

        <h2 className="text-center text-4xl font-bold text-white">
          TaskSphere Login
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
              className="block w-full px-4 py-3 border border-emerald-700/50 bg-emerald-800/50 text-emerald-100 rounded-t-md"
              placeholder="Email address"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />

            <input
              type="password"
              required
              className="block w-full px-4 py-3 border border-emerald-700/50 bg-emerald-800/50 text-emerald-100 rounded-b-md"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>

          <button
            type="submit"
            className="w-full py-3 font-bold rounded-2xl text-white bg-emerald-500 hover:bg-emerald-600"
          >
            Login
          </button>
        </form>

        <div className="text-center text-sm text-emerald-300/80">
          Don’t have an account?{" "}
          <Link
            href="/register"
            className="font-bold hover:underline text-emerald-200"
          >
            Register here
          </Link>
        </div>

      </div>
    </div>
  );
}
