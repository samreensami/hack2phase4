import { Suspense } from 'react';
import MyTasksPageContent from './MyTasksPageContent';

// Force this page to be dynamic (SSR) - no static prerendering
export const dynamic = 'force-dynamic';

export default function MyTasksPage() {
  return (
    <Suspense fallback={<div>Loading tasks...</div>}>
      <MyTasksPageContent />
    </Suspense>
  );
}