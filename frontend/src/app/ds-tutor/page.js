"use client";

import { useState, useRef, useEffect } from "react";
import Link from "next/link";
import useVoices from "@/hooks/useVoices";
import { uploadPDF, askDSTutor } from "@/services/dsTutorApi";

const SUGGESTIONS = [
  "What is a Stack ADT?",
  "Explain Binary Tree traversals",
  "Difference between Array and Linked List",
  "What is FIFO and LIFO?",
  "What are Linear vs Non-Linear structures?",
];

const BotIcon = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <rect x="3" y="11" width="18" height="11" rx="2"/>
    <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
    <circle cx="12" cy="16" r="1" fill="currentColor"/>
    <path d="M8 16h.01M16 16h.01"/>
  </svg>
);

const UserIcon = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <circle cx="12" cy="8" r="4"/>
    <path d="M4 20c0-4 3.6-7 8-7s8 3 8 7"/>
  </svg>
);

const SendIcon = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <path d="M22 2L11 13M22 2L15 22l-4-9-9-4 20-7z"/>
  </svg>
);

function parseMarkdown(text) {
  return text
    .replace(/^#### (.+)$/gm, '<h4>$1</h4>')
    .replace(/^### (.+)$/gm, '<h3>$1</h3>')
    .replace(/^## (.+)$/gm, '<h2>$1</h2>')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    .replace(/`(.+?)`/g, '<code>$1</code>')
    .replace(/^---$/gm, '<hr/>')
    .replace(/^\* (.+)$/gm, '<li>$1</li>')
    .replace(/^    \* (.+)$/gm, '<li class="sub">$1</li>')
    .replace(/(<li.*<\/li>\n?)+/g, m => `<ul>${m}</ul>`)
    .replace(/\n\n/g, '</p><p>')
    .replace(/^(?!<[hup]|<li|<hr)(.+)$/gm, '$1')
    .replace(/(<\/h[234]>|<\/ul>|<hr\/>)\s*<\/p><p>/g, '$1')
    .replace(/<p><\/p>/g, '');
}

export default function DSTutorPage() {
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content: "Hello! 👋 I'm your **DS Tutor**. Upload a PDF or ask me anything about Data Structures — definitions, examples, comparisons, or exam prep. I'm here to help you deeply understand the concepts!",
      sources: [],
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [uploadMessage, setUploadMessage] = useState("");
  const [voiceEnabled, setVoiceEnabled] = useState(false);
  const [currentAudio, setCurrentAudio] = useState(null);
  const bottomRef = useRef(null);
  const inputRef = useRef(null);
  const { voices, selectedVoice, setSelectedVoice } = useVoices();

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const handlePDFUpload = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setLoading(true);
    try {
      const data = await uploadPDF(file);
      setUploadMessage(`✅ ${data.message}`);
      setMessages(prev => [...prev, {
        role: "assistant",
        content: `📄 **PDF uploaded successfully!** You can now ask questions about the content.`,
        sources: [],
      }]);
    } catch {
      setUploadMessage("❌ Upload failed");
    } finally {
      setLoading(false);
    }
  };

  async function send(text) {
    const q = (text || input).trim();
    if (!q || loading) return;
    setInput("");
    const userMsg = { role: "user", content: q };
    setMessages(prev => [...prev, userMsg]);
    setLoading(true);
    try {
      const data = await askDSTutor(q, voiceEnabled ? selectedVoice : null, voiceEnabled);
      setMessages(prev => [...prev, { 
        role: "assistant", 
        content: data.answer || data.text,
        sources: data.sources || [],
        audio: data.audio || null,
      }]);
    } catch {
      setMessages(prev => [...prev, { 
        role: "assistant", 
        content: "Something went wrong. Please try again.",
        sources: [],
      }]);
    }
    setLoading(false);
    inputRef.current?.focus();
  }

  return (
    <div className="min-h-screen bg-white flex flex-col font-serif text-gray-800">
      {/* Header */}
      <div className="border-b border-gray-200 px-6 py-4 flex items-center gap-3 bg-white sticky top-0 z-10">
        <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-lg">📚</div>
        <div>
          <div className="font-bold text-[15px] tracking-wide">DS Tutor</div>
          <div className="text-xs text-gray-400 font-mono">Data Structures · Exam Prep</div>
        </div>
        <div className="ml-auto flex items-center gap-2">
          <label className="text-xs text-gray-600 cursor-pointer hover:text-indigo-600 transition flex items-center gap-2 border border-gray-200 px-3 py-1.5 rounded-lg hover:border-indigo-300">
            📄 Upload PDF
            <input type="file" accept=".pdf" onChange={handlePDFUpload} className="hidden" />
          </label>
          
          {/* Voice Toggle */}
          <button
            onClick={() => setVoiceEnabled(!voiceEnabled)}
            className={`text-xs cursor-pointer transition flex items-center gap-2 border px-3 py-1.5 rounded-lg ${
              voiceEnabled 
                ? "text-indigo-600 border-indigo-300 bg-indigo-50" 
                : "text-gray-600 border-gray-200 hover:text-indigo-600 hover:border-indigo-300"
            }`}
          >
            🎙️ Voice {voiceEnabled ? "ON" : "OFF"}
          </button>
          
          <div className="flex items-center gap-1.5 text-xs text-green-500">
            <div className="w-1.5 h-1.5 rounded-full bg-green-500 shadow-[0_0_6px_#10b981]" />
            Online
          </div>
        </div>
      </div>

      {/* Chat */}
      <div className="flex-1 overflow-y-auto py-6 flex flex-col gap-0">
        {messages.map((msg, i) => (
          <div key={i} className={`flex ${msg.role === "user" ? "flex-row-reverse" : "flex-row"} items-start gap-3 px-5 py-2.5 max-w-[860px] mx-auto w-full`}>
            <div className={`w-8 h-8 rounded-xl ${msg.role === "user" ? "bg-gradient-to-br from-blue-600 to-blue-400" : "bg-gradient-to-br from-indigo-500 to-purple-600"} flex items-center justify-center flex-shrink-0 text-white`}>
              {msg.role === "user" ? <UserIcon /> : <BotIcon />}
            </div>
            <div className={`${msg.role === "user" ? "bg-blue-50 border-blue-200" : "bg-gray-50 border-gray-200"} border rounded-2xl ${msg.role === "user" ? "rounded-tr-sm" : "rounded-tl-sm"} px-4 py-3.5 max-w-[calc(100%-52px)] text-sm leading-relaxed text-gray-800`}>
              {msg.role === "assistant" ? (
                <>
                  {msg.sources && msg.sources.length > 0 && (
                    <div className="flex items-center gap-2 mb-3 pb-2 border-b border-gray-200">
                      <div className="flex items-center gap-1.5 text-xs font-medium text-indigo-600 bg-indigo-50 px-2.5 py-1 rounded-full border border-indigo-200">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                          <polyline points="14 2 14 8 20 8"/>
                        </svg>
                        From PDF
                      </div>
                      <span className="text-xs text-gray-500">{msg.sources.join(", ")}</span>
                    </div>
                  )}
                  <div dangerouslySetInnerHTML={{ __html: parseMarkdown(msg.content) }} className="msg-content" />
                  
                  {/* Audio Player */}
                  {msg.audio && (
                    <div className="mt-3 pt-3 border-t border-gray-200">
                      <div className="flex items-center gap-2">
                        <button
                          onClick={() => {
                            if (currentAudio) {
                              currentAudio.pause();
                              setCurrentAudio(null);
                            }
                            const audio = new Audio(msg.audio);
                            audio.play();
                            setCurrentAudio(audio);
                            audio.onended = () => setCurrentAudio(null);
                          }}
                          className="flex items-center gap-2 text-xs text-indigo-600 bg-indigo-50 px-3 py-1.5 rounded-full border border-indigo-200 hover:bg-indigo-100 transition"
                        >
                          <svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor">
                            <polygon points="5,3 19,12 5,21" />
                          </svg>
                          Listen to Answer
                        </button>
                        <span className="text-xs text-gray-500">AI Voice Response</span>
                      </div>
                    </div>
                  )}
                </>
              ) : (
                <span className="text-gray-700">{msg.content}</span>
              )}
            </div>
          </div>
        ))}

        {loading && (
          <div className="flex items-start gap-3 px-5 py-2.5 max-w-[860px] mx-auto w-full">
            <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-white">
              <BotIcon />
            </div>
            <div className="bg-gray-50 border border-gray-200 rounded-2xl rounded-tl-sm px-4 py-3.5 flex gap-1.5 items-center">
              {[0, 1, 2].map(n => (
                <div key={n} className="w-1.5 h-1.5 rounded-full bg-indigo-500 animate-pulse" style={{ animationDelay: `${n * 0.2}s` }} />
              ))}
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Suggestions */}
      {messages.length <= 2 && (
        <div className="px-5 pb-4 max-w-[860px] mx-auto w-full">
          <div className="text-[11px] text-gray-500 mb-2 uppercase tracking-wider">Try asking</div>
          <div className="flex flex-wrap gap-2">
            {SUGGESTIONS.map((s, i) => (
              <button key={i} onClick={() => send(s)} className="bg-white border border-gray-200 rounded-full px-3.5 py-1.5 text-xs text-gray-600 hover:border-indigo-400 hover:text-indigo-600 hover:bg-indigo-50 transition">
                {s}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Input */}
      <div className="px-5 pb-5 pt-3 border-t border-gray-200 bg-white">
        <div className="max-w-[860px] mx-auto flex gap-2.5 items-end">
          <div className="flex-1 bg-white border border-gray-300 rounded-xl px-4 py-2.5 flex items-center focus-within:border-indigo-500 transition">
            <textarea
              ref={inputRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); send(); } }}
              placeholder="Ask about any data structure concept..."
              rows={1}
              className="flex-1 bg-transparent border-none outline-none text-gray-800 text-sm resize-none max-h-[120px] overflow-y-auto"
            />
          </div>
          <button
            onClick={() => send()}
            disabled={!input.trim() || loading}
            className={`w-10 h-10 rounded-xl border-none flex items-center justify-center flex-shrink-0 transition ${input.trim() && !loading ? "bg-gradient-to-br from-indigo-500 to-purple-600 text-white cursor-pointer" : "bg-gray-200 text-gray-400 cursor-default"}`}
          >
            <SendIcon />
          </button>
        </div>
        <div className="text-center text-[11px] text-gray-400 mt-2.5">Press Enter to send · Shift+Enter for new line</div>
      </div>

      <style jsx global>{`
        .msg-content h3 { color: #4f46e5; font-size: 15px; margin: 16px 0 8px; border-bottom: 1px solid #e5e7eb; padding-bottom: 6px; }
        .msg-content h4 { color: #6366f1; font-size: 14px; margin: 14px 0 6px; }
        .msg-content strong { color: #1f2937; font-weight: 600; }
        .msg-content em { color: #6b7280; font-style: italic; }
        .msg-content code { background: #f3f4f6; border: 1px solid #d1d5db; border-radius: 4px; padding: 1px 6px; font-family: monospace; font-size: 13px; color: #4f46e5; }
        .msg-content ul { padding-left: 20px; margin: 8px 0; }
        .msg-content li { margin: 5px 0; color: #374151; }
        .msg-content li.sub { margin-left: 16px; color: #6b7280; }
        .msg-content hr { border: none; border-top: 1px solid #e5e7eb; margin: 14px 0; }
        .msg-content p { margin: 8px 0; }
      `}</style>
    </div>
  );
}
