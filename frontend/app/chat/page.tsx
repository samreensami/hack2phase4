'use client';

import React, { useState, useEffect, useRef } from 'react';
import { api } from '../../lib/api-service';

interface Message {
  sender: 'user' | 'assistant';
  content: string;
}

interface ChatResponse {
  response: string;
  conversation_id: number;
}

interface LatestConv {
  conversation_id: number | null;
}

interface MsgResp {
  sender: string;
  content: string;
}

interface MessagesResp {
  messages: MsgResp[];
}

interface NewConvResp {
  conversation_id: number;
}

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [conversationId, setConversationId] = useState<number | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [initialLoading, setInitialLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    const checkAuth = async () => {
      try {
        await api.get('/dashboard/tasks/');
        setIsAuthenticated(true);

        // Load latest conversation history
        try {
          const latestResp = await api.get<LatestConv>('/api/conversations/latest');
          const convId = latestResp.data.conversation_id;
          if (convId !== null) {
            setConversationId(convId);
            const msgsResp = await api.get<MessagesResp>(`/api/conversations/${convId}/messages`);
            setMessages(
              msgsResp.data.messages.map((m) => ({
                sender: m.sender as 'user' | 'assistant',
                content: m.content,
              }))
            );
          }
        } catch (histError) {
          console.error('Failed to load chat history:', histError);
        }
      } catch (error) {
        console.error('Auth check failed:', error);
        setIsAuthenticated(false);
      } finally {
        setInitialLoading(false);
      }
    };

    checkAuth();
  }, []);

  const handleNewConversation = async () => {
    if (isLoading) return;
    try {
      setIsLoading(true);
      const resp = await api.post<NewConvResp>('/api/conversations/new');
      setConversationId(resp.data.conversation_id);
      setMessages([]);
    } catch (error) {
      console.error('Failed to create new conversation:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const trimmedInput = input.trim();
    if (!trimmedInput || isLoading || !isAuthenticated) return;

    const userMessage: Message = { sender: 'user', content: trimmedInput };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await api.post<ChatResponse>('/api/chat', {
        message: trimmedInput,
        conversation_id: conversationId,
      });

      const { response: assistantMessageContent, conversation_id } = response.data;

      const assistantMessage: Message = { sender: 'assistant', content: assistantMessageContent };
      setMessages((prev) => [...prev, assistantMessage]);
      setConversationId(conversation_id);

    } catch (error) {
      console.error('Failed to send message:', error);
      const errorMessage: Message = { sender: 'assistant', content: "Connection Error. Please check your connection and try again." };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      {initialLoading ? (
        <div className="flex flex-col h-[calc(100vh-120px)] items-center justify-center bg-emerald-900/50 rounded-2xl shadow-lg p-8">
          <p className="text-emerald-100 text-xl font-medium">Rendering...</p>
        </div>
      ) : !isAuthenticated ? (
        <div className="flex flex-col h-[calc(100vh-120px)] items-center justify-center bg-emerald-900/50 rounded-2xl shadow-lg p-8">
          <p className="text-emerald-100 text-xl font-medium">Please <a href="/login" className="underline hover:text-emerald-300">log in</a> to use chat.</p>
        </div>
      ) : (
        <div className="flex flex-col h-[calc(100vh-120px)] bg-emerald-900/50 rounded-2xl shadow-lg">
      <div className="flex-1 p-6 space-y-4 overflow-y-auto">
        {messages.map((msg, index) => (
          <div key={index} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div
              className={`max-w-lg px-4 py-2 rounded-xl ${
                msg.sender === 'user'
                  ? 'bg-emerald-600 text-white'
                  : 'bg-emerald-800 text-emerald-100'
              }`}
            >
              <p style={{whiteSpace: 'pre-wrap'}}>{msg.content}</p>
            </div>
          </div>
        ))}
         {isLoading && (
          <div className="flex justify-start">
            <div className="max-w-lg px-4 py-2 rounded-xl bg-emerald-800 text-emerald-100">
              <p>Thinking...</p>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="p-4 border-t border-emerald-700 flex flex-col gap-2 sm:flex-row sm:items-center sm:space-x-4">
        <div className="flex-1">
          <form onSubmit={handleSubmit} className="flex items-center space-x-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask your assistant to manage your tasks..."
              className="flex-1 p-3 bg-emerald-800/80 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500"
              disabled={isLoading}
            />
            <button
              type="submit"
              className="px-6 py-3 bg-emerald-600 rounded-lg hover:bg-emerald-500 disabled:bg-emerald-700 disabled:cursor-not-allowed whitespace-nowrap"
              disabled={isLoading || !input.trim()}
            >
              Send
            </button>
          </form>
        </div>
        <button
          onClick={handleNewConversation}
          className="px-6 py-3 bg-emerald-700 rounded-lg hover:bg-emerald-600 text-emerald-100 font-medium whitespace-nowrap disabled:opacity-50"
          disabled={isLoading}
        >
          New Chat
        </button>
      </div>
    </div>
  );
}
