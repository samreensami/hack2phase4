import "./globals.css";
import Link from "next/link";
import LogoutButton from "./logoutbutton/page";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning={true}>
      <body suppressHydrationWarning={true} className="bg-emerald-950 text-white min-h-screen">
        <div className="flex min-h-screen">
          {/* Sidebar */}
          <aside className="w-64 bg-emerald-900/40 backdrop-blur-md border-r border-emerald-800 p-6 flex flex-col fixed h-full shadow-xl">
            <div className="flex items-center gap-2 mb-10 px-2">
              <span className="text-3xl">🚀</span>
              <h1 className="text-xl font-bold tracking-tighter">TaskSphere</h1>
            </div>

            <nav className="flex-1 space-y-3">
              <Link
                href="/dashboard"
                className="flex items-center gap-3 p-3 hover:bg-emerald-800/50 rounded-2xl transition-all"
              >
                <span>📊</span> Dashboard
              </Link>

              <Link
                href="/dashboard/tasks"
                className="flex items-center gap-3 p-3 hover:bg-emerald-800/50 rounded-2xl transition-all"
              >
                <span>📝</span> My Tasks
              </Link>

              <Link
                href="/chat"
                className="flex items-center gap-3 p-3 hover:bg-emerald-800/50 rounded-2xl transition-all"
              >
                <span>🤖</span> AI Chat
              </Link>
            </nav>

            <div className="mt-auto pt-6 border-t border-emerald-800/50 space-y-2">
              <Link
                href="/login"
                className="block px-4 py-2 text-sm text-emerald-400 hover:text-white transition"
              >
                🔑 Login
              </Link>
              <Link
                href="/register"
                className="block px-4 py-2 text-sm text-emerald-400 hover:text-white transition"
              >
                👤 Register
              </Link>
              <LogoutButton />
            </div>
          </aside>

          {/* Main content */}
          <main className="flex-1 ml-64 p-10 bg-emerald-900/30">
            {children}
          </main>
        </div>
      </body>
    </html>
  );
}
