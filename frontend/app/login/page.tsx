import { Suspense } from "react";
import LoginPageContent from "./LoginPageContent";

// Force this page to be dynamic (SSR) - no static prerendering
export const dynamic = 'force-dynamic';

export default function LoginPage() {
  return (
    <Suspense fallback={<div className="flex min-h-screen items-center justify-center bg-emerald-950">Loading...</div>}>
      <LoginPageContent />
    </Suspense>
  );
}