import { Suspense } from "react";
import LogoutButtonContent from "./LogoutButtonContent";

// Force this page to be dynamic (SSR) - no static prerendering
export const dynamic = 'force-dynamic';

export default function LogoutButton() {
  return (
    <Suspense fallback={<div>Logging out...</div>}>
      <LogoutButtonContent />
    </Suspense>
  );
}