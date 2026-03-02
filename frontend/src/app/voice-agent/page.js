"use client";

import { useState, useRef, useEffect } from "react";
import Link from "next/link";
import { BACKEND } from "@/config/api";
import useVoices from "@/hooks/useVoices";
import VoiceSelector from "@/components/VoiceSelector";
import AudioRecorder from "@/components/AudioRecorder";

export default function VoiceAgentPage() {
  const [audioURL, setAudioURL] = useState(null);
  const [text, setText] = useState("");
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const { voices, selectedVoice, setSelectedVoice } = useVoices();
  const currentAudioRef = useRef(null);

  // --------------------------------
  // Send request helper
  // --------------------------------
  const sendRequest = async (url, body, isJSON = false) => {
    setLoading(true);

    try {
      const res = await fetch(url, {
        method: "POST",
        body,
        ...(isJSON && { headers: { "Content-Type": "application/json" } }),
      });

      if (!res.ok) {
        throw new Error("Backend request failed");
      }

      const data = await res.json();

      setText(`🗣 You: ${data.userText}\n\n🤖 AI: ${data.text}`);
      setAudioURL(data.audio);
      setInput("");
    } catch (err) {
      console.error(err);
      setText("❌ Request failed");
    } finally {
      setLoading(false);
    }
  };

  // --------------------------------
  // Text submit
  // --------------------------------
  const handleTextSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const body = JSON.stringify({
      text: input,
      voiceId: selectedVoice,
    });

    await sendRequest(`${BACKEND}/text-agent`, body, true);
  };

  // --------------------------------
  // Voice submit
  // --------------------------------
  const handleVoiceStop = async (blob) => {
    const form = new FormData();
    form.append("file", blob, "input.webm");
    form.append("voiceId", selectedVoice);

    await sendRequest(`${BACKEND}/agent`, form);
  };

  // --------------------------------
  // Auto-play audio
  // --------------------------------
  useEffect(() => {
    if (!audioURL) return;

    if (currentAudioRef.current) {
      currentAudioRef.current.pause();
    }

    const audio = new Audio(audioURL);
    currentAudioRef.current = audio;

    audio.play().catch(() => {});
  }, [audioURL]);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-b from-green-50 to-white p-6">
      <div className="w-full max-w-md bg-white shadow-xl rounded-3xl p-6 border text-center">
        <h1 className="text-2xl font-bold mb-2 text-green-700">
          🎙️ Agentic Voice Assistant
        </h1>

        <p className="text-gray-600 mb-4 text-sm">
          Speak or type your question — AI responds with text and voice.
        </p>

        {/* Voice selector */}
        <VoiceSelector
          voices={voices}
          selectedVoice={selectedVoice}
          onChange={setSelectedVoice}
        />

        {/* Recorder */}
        <div className="mt-4">
          <AudioRecorder onStop={handleVoiceStop} />
        </div>

        {/* Text input */}
        <form onSubmit={handleTextSubmit} className="mt-5 flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask your question..."
            className="flex-1 border rounded-lg p-2"
          />
          <button className="bg-green-600 text-white px-4 py-2 rounded-lg">
            Send
          </button>
        </form>

        {loading && (
          <p className="text-blue-500 mt-4 animate-pulse">
            Processing...
          </p>
        )}

        {text && (
          <pre className="mt-4 p-3 bg-gray-100 rounded-lg text-left whitespace-pre-wrap text-sm">
            {text}
          </pre>
        )}

        {audioURL && (
          <audio controls src={audioURL} className="w-full mt-4" />
        )}

        <Link
          href="/"
          className="text-green-700 hover:underline mt-5 inline-block text-sm"
        >
          ← Back to Home
        </Link>
      </div>
    </div>
  );
}
