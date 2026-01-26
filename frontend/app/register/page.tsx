import { Suspense } from "react";
import RegisterPageContent from "./RegisterPageContent";

// Force this page to be dynamic (SSR) - no static prerendering
export const dynamic = 'force-dynamic';

export default function RegisterPage() {
    return (
        <Suspense fallback={<div className="flex min-h-screen items-center justify-center bg-emerald-950">Loading...</div>}>
            <RegisterPageContent />
        </Suspense>
    );
}