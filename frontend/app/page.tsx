import Link from "next/link";

export default function HomePage() {
  console.log("🏠 HomePage rendering with Sober Emerald theme");

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-emerald-950 font-sans p-5">
      <div className="bg-emerald-900 border border-emerald-800 rounded-3xl p-10 text-center max-w-2xl">
        <h1 className="text-6xl mb-5 font-bold text-white">
          Task Manager
        </h1>
        <p className="text-2xl mb-10 text-emerald-300/80">
          Organize your tasks efficiently in style
        </p>
        <div className="flex gap-5 justify-center flex-wrap">
          <Link href="/login" className="px-10 py-4 text-lg bg-emerald-500 text-white rounded-2xl font-bold shadow-md hover:scale-105 transition-transform">
            Login
          </Link>
          <Link href="/register" className="px-10 py-4 text-lg bg-transparent text-emerald-100 border border-emerald-500/50 rounded-2xl font-bold hover:bg-emerald-800 transition-all">
            Register
          </Link>
        </div>
      </div>
    </div>
  );
}
