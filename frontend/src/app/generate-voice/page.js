"use client";

import { useState } from "react";
import Link from "next/link";
import { BACKEND } from "@/config/api";
import AudioPlayer from "@/components/AudioPlayer";
import VoiceSelector from "@/components/VoiceSelector";
import useVoices from "@/hooks/useVoices";

export default function GenerateVoice() {
  const [text, setText] = useState("");
  const [audioUrl, setAudioUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [charCount, setCharCount] = useState(0);
  const [error, setError] = useState("");

  const { voices, selectedVoice, setSelectedVoice } = useVoices();

  // ✍️ Handle text change
  const handleTextChange = (e) => {
    const val = e.target.value.slice(0, 500);
    setText(val);
    setCharCount(val.length);
    setError("");
  };

  // 🎤 Generate speech
  const handleGenerate = async () => {
    if (!text.trim()) {
      setError("Please enter text!");
      return;
    }

    setLoading(true);
    setAudioUrl(null);
    setError("");

    try {
      const res = await fetch(`${BACKEND}/speech`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text, voiceId: selectedVoice }),
        signal: AbortSignal.timeout(30000),
      });

      if (!res.ok) {
        throw new Error("Speech generation failed");
      }

      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      setAudioUrl(url);
    } catch (err) {
      console.error(err);
      setError("Failed to generate voice!");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen flex flex-col items-center justify-center bg-gray-50 p-6">
      <div className="w-full max-w-md bg-white shadow-lg rounded-2xl p-8 border">
        <h1 className="text-xl font-bold mb-4 text-center">
          🎤 Generate Voice
        </h1>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-4">
            {error}
          </div>
        )}

        {/* Text Input */}
        <textarea
          value={text}
          onChange={handleTextChange}
          placeholder="Type something..."
          className="w-full border rounded-lg p-3"
          rows={4}
        />

        <p className="text-sm text-gray-500 text-right">{charCount}/500</p>

        {/* Voice selector */}
        <VoiceSelector
          voices={voices}
          selectedVoice={selectedVoice}
          onChange={setSelectedVoice}
        />

        {/* Generate button */}
        <button
          onClick={handleGenerate}
          disabled={loading || !text.trim()}
          className={`w-full mt-4 py-3 rounded-lg text-white font-semibold ${
            loading ? "bg-gray-400" : "bg-blue-600 hover:bg-blue-700"
          }`}
        >
          {loading ? "Generating..." : "Generate Voice"}
        </button>

        {/* Audio player */}
        <AudioPlayer audioUrl={audioUrl} filename="voice.mp3" />

        <div className="text-center mt-6">
          <Link href="/" className="underline text-gray-700">
            ← Back to Home
          </Link>
        </div>
      </div>
    </main>
  );
}
