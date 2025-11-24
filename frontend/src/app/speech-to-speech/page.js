"use client";
import { useState, useEffect } from "react";
import Link from "next/link";
import { Download } from "lucide-react";

export default function SpeechToSpeech() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [audioUrl, setAudioUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [voices, setVoices] = useState([]);
  const [selectedVoice, setSelectedVoice] = useState("");

  const BACKEND = process.env.NEXT_PUBLIC_BACKEND_URL || "http://127.0.0.1:8000/api";

  // Load ElevenLabs voices
  useEffect(() => {
    async function loadVoices() {
      try {
        const res = await fetch(`${BACKEND}/voices`);
        const data = await res.json();
        setVoices(data.voices || []);
        if (data.voices && data.voices.length > 0) {
          setSelectedVoice(data.voices[0].voice_id);
        }
      } catch (err) {
        console.error("Voice load error:", err);
      }
    }
    loadVoices();
  }, []);

  const handleConversion = async () => {
    if (!selectedFile) return alert("Upload a voice file!");

    setLoading(true);
    setAudioUrl(null);

    try {
      const form = new FormData();
      form.append("file", selectedFile);
      form.append("voiceId", selectedVoice);

      const res = await fetch(`${BACKEND}/speech-to-speech`, {
        method: "POST",
        body: form,
      });

      if (!res.ok) throw new Error("Speech conversion failed");

      const blob = await res.blob();
      setAudioUrl(URL.createObjectURL(blob));
    } catch (err) {
      console.error(err);
      alert("Something went wrong during speech conversion!");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen flex flex-col items-center justify-center bg-gray-50 p-6">
      <div className="bg-white shadow-lg rounded-2xl p-8 w-full max-w-md border text-center">
        <h1 className="text-xl font-bold mb-4">💬 Speech → Speech Conversion</h1>

        {/* Voice Selector */}
        <select
          className="w-full border p-3 rounded-lg mb-3"
          value={selectedVoice}
          onChange={(e) => setSelectedVoice(e.target.value)}
        >
          {voices.length > 0 ? (
            voices.map((v) => (
              <option key={v.voice_id} value={v.voice_id}>
                {v.name} — {v.labels?.gender || ""}
              </option>
            ))
          ) : (
            <option>Loading voices...</option>
          )}
        </select>

        {/* File Upload */}
        <input
          type="file"
          accept="audio/*"
          onChange={(e) => setSelectedFile(e.target.files[0])}
          className="w-full border p-3 rounded-lg mb-4"
        />

        <button
          onClick={handleConversion}
          disabled={loading}
          className={`w-full py-3 rounded-lg text-white font-semibold ${
            loading
              ? "bg-gray-400"
              : "bg-gradient-to-r from-purple-500 to-pink-500 hover:scale-105"
          }`}
        >
          {loading ? "Processing..." : "Convert Speech"}
        </button>

        {audioUrl && (
          <div className="mt-6 space-y-3">
            <audio controls className="w-full" src={audioUrl} />
            <a
              href={audioUrl}
              download="converted_voice.mp3"
              className="flex items-center justify-center gap-2 bg-red-500 hover:bg-red-600 text-white py-2 rounded-lg"
            >
              <Download className="w-4 h-4" /> Download
            </a>
          </div>
        )}

        <Link href="/" className="mt-6 inline-block text-gray-700 underline">
          ← Back to Home
        </Link>
      </div>
    </main>
  );
}
