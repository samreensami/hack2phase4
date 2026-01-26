import { Suspense } from 'react';
import ChatPageContent from './ChatPageContent';

// Force this page to be dynamic (SSR) - no static prerendering
export const dynamic = 'force-dynamic';

export default function ChatPage() {
  return (
    <Suspense fallback={<div className="flex h-screen items-center justify-center bg-emerald-900/50">Loading chat...</div>}>
      <ChatPageContent />
    </Suspense>
  );
}