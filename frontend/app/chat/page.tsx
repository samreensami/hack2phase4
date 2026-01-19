'use client';

import React, { useEffect, useRef, useState } from 'react';
import { useRouter } from 'next/navigation';
import { api } from '../../lib/api-service';

interface Message {
  sender: 'user' | 'assistant';
  content: string;
}

interface ChatResponse {
  response: string;
  conversation_id: number;
}

interface LatestConversation {
  conversation_id: number | null;
}

interface MessageAPI {
  sender: string;
  content: string;
}

interface MessagesResponse {
  messages: MessageAPI[];
}

interface NewConversationResponse {
  conversation_id: number;
}

export default function ChatPage() {
  const router = useRouter();

  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [conversationId, setConversationId] = useState<number | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [initialLoading, setInitialLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  // auto scroll
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // auth + load latest conversation
  useEffect(() => {
    const controller = new AbortController();
    let mounted = true;

    const init = async () => {
      try {
        const token =
          typeof window !== 'undefined'
            ? localStorage.getItem('token')
            : null;

        if (!token) {
          setIsAuthenticated(false);
          return;
        }

        // ✅ no root "/" call anymore
        setIsAuthenticated(true);

        const latest = await api.get<LatestConversation>(
          '/api/conversations/latest',
          { signal: controller.signal }
        );

        if (!mounted) return;

        if (latest.data.conversation_id) {
          const convId = latest.data.conversation_id;
          setConversationId(convId);

          const msgs = await api.get<MessagesResponse>(
            `/api/conversations/${convId}/messages`,
            { signal: controller.signal }
          );

          if (!mounted) return;

          setMessages(
            msgs.data.messages.map((m) => ({
              sender: m.sender as 'user' | 'assistant',
              content: m.content,
            }))
          );
        }
      } catch (err: any) {
        // Ignore canceled requests (component unmounted)
        if (err?.name === 'CanceledError' || err?.code === 'ERR_CANCELED') {
          return;
        }
        console.error('Chat init failed:', err);
        setIsAuthenticated(false);
      } finally {
        if (mounted) setInitialLoading(false);
      }
    };

    init();

    return () => {
      mounted = false;
      controller.abort();
    };
  }, []);

  // redirect if not logged in
  useEffect(() => {
    if (!initialLoading && !isAuthenticated) {
      router.replace('/login');
    }
  }, [initialLoading, isAuthenticated, router]);

  // new conversation
  const handleNewConversation = async () => {
    if (isLoading) return;

    try {
      setIsLoading(true);
      const res = await api.post<NewConversationResponse>(
        '/api/conversations/new'
      );
      setConversationId(res.data.conversation_id);
      setMessages([]);
    } catch (err) {
      console.error('New chat error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  // send message
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMsg: Message = {
      sender: 'user',
      content: input.trim(),
    };

    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setIsLoading(true);

    try {
      const res = await api.post<ChatResponse>('/api/chat', {
        message: userMsg.content,
        conversation_id: conversationId,
      });

      setConversationId(res.data.conversation_id);

      setMessages((prev) => [
        ...prev,
        { sender: 'assistant', content: res.data.response },
      ]);
    } catch (err: any) {
      let msg = 'Connection error. Please try again.';

      if (err.response?.status === 401) {
        localStorage.removeItem('token');
        router.replace('/login');
        return;
      }

      if (err.response?.data?.detail) {
        msg = err.response.data.detail;
      }

      setMessages((prev) => [
        ...prev,
        { sender: 'assistant', content: `Error: ${msg}` },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  if (initialLoading) {
    return (
      <div className="flex h-[calc(100vh-120px)] items-center justify-center bg-emerald-900/50 rounded-2xl">
        <p className="text-emerald-100 text-lg">Loading session...</p>
      </div>
    );
  }

  if (!isAuthenticated) return null;

  // Quick action buttons
  const quickActions = [
    { label: 'List my tasks', prompt: 'Show me all my tasks' },
    { label: 'Add a task', prompt: 'Add a new task called ' },
    { label: 'Delete a task', prompt: 'Delete task with ID ' },
    { label: 'Complete a task', prompt: 'Mark task ID as complete: ' },
    { label: 'Pending tasks', prompt: 'How many tasks are pending?' },
  ];

  const handleQuickAction = (prompt: string) => {
    setInput(prompt);
  };

  return (
    <div className="flex flex-col h-[calc(100vh-120px)] bg-emerald-900/50 rounded-2xl shadow-lg">
      {/* Quick Actions */}
      <div className="p-3 border-b border-emerald-700 flex flex-wrap gap-2">
        {quickActions.map((action, i) => (
          <button
            key={i}
            onClick={() => handleQuickAction(action.prompt)}
            className="px-3 py-1 text-xs bg-emerald-700/50 hover:bg-emerald-600 rounded-full transition-colors"
          >
            {action.label}
          </button>
        ))}
      </div>

      {/* messages */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`flex ${
              msg.sender === 'user' ? 'justify-end' : 'justify-start'
            }`}
          >
            <div
              className={`max-w-lg px-4 py-2 rounded-xl text-sm ${
                msg.sender === 'user'
                  ? 'bg-emerald-600 text-white'
                  : 'bg-emerald-800 text-emerald-100'
              }`}
            >
              <p className="whitespace-pre-wrap">{msg.content}</p>
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-emerald-800 text-emerald-100 px-4 py-2 rounded-xl">
              Thinking...
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* input */}
      <div className="border-t border-emerald-700 p-4 flex flex-col sm:flex-row gap-3">
        <form onSubmit={handleSubmit} className="flex flex-1 gap-2">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask your assistant..."
            className="flex-1 p-3 rounded-lg bg-emerald-800/80 focus:outline-none focus:ring-2 focus:ring-emerald-500"
            disabled={isLoading}
          />

          <button
            type="submit"
            disabled={isLoading || !input.trim()}
            className="px-6 py-3 bg-emerald-600 rounded-lg hover:bg-emerald-500 disabled:opacity-50"
          >
            Send
          </button>
        </form>

        <button
          onClick={handleNewConversation}
          disabled={isLoading}
          className="px-6 py-3 bg-emerald-700 rounded-lg hover:bg-emerald-600 disabled:opacity-50"
        >
          New Chat
        </button>
      </div>
    </div>
  );
}
