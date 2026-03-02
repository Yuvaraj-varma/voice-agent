"use client";

import { useState } from "react";
import Link from "next/link";
import { transformVoice } from "@/services/voiceApi";
import AudioPlayer from "@/components/AudioPlayer";
import VoiceSelector from "@/components/VoiceSelector";
import useVoices from "@/hooks/useVoices";

export default function SpeechToSpeech() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [audioUrl, setAudioUrl] = useState(null);
  const [loading, setLoading] = useState(false);

  // Voices handled by hook
  const { voices, selectedVoice, setSelectedVoice } = useVoices();

  // ------------------------------------
  // Voice transform using service layer
  // ------------------------------------
  const handleConversion = async () => {
    if (!selectedFile) return alert("Upload a voice file!");
    if (!selectedVoice) return alert("Select a voice!");

    setLoading(true);
    setAudioUrl(null);

    try {
      const blob = await transformVoice(selectedFile, selectedVoice);
      const url = URL.createObjectURL(blob);
      setAudioUrl(url);
    } catch (err) {
      console.error(err);
      alert("Conversion failed!");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen flex flex-col items-center justify-center bg-gray-50 p-6">
      <div className="bg-white shadow-lg rounded-2xl p-8 w-full max-w-md border text-center">
        <h1 className="text-xl font-bold mb-4">
          💬 Speech → Speech Conversion
        </h1>

        {/* Voice selector */}
        <VoiceSelector
          voices={voices}
          selectedVoice={selectedVoice}
          onChange={setSelectedVoice}
        />

        {/* File upload */}
        <input
          type="file"
          accept="audio/*"
          onChange={(e) => setSelectedFile(e.target.files?.[0] ?? null)}
          className="w-full border p-3 rounded-lg mb-4"
        />

        {/* Convert button */}
        <button
          onClick={handleConversion}
          disabled={loading}
          className={`w-full py-3 rounded-lg text-white font-semibold ${
            loading ? "bg-gray-400" : "bg-purple-600 hover:bg-purple-700"
          }`}
        >
          {loading ? "Processing..." : "Convert Speech"}
        </button>

        {/* Audio player */}
        <AudioPlayer audioUrl={audioUrl} filename="converted_voice.mp3" />

        <Link href="/" className="mt-6 inline-block text-gray-700 underline">
          ← Back to Home
        </Link>
      </div>
    </main>
  );
}
