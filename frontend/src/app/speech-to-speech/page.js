"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { Download } from "lucide-react";

// ---------- BACKEND URL ----------
const RAW = process.env.NEXT_PUBLIC_BACKEND_URL || "http://127.0.0.1:8000";
const BACKEND = RAW.replace(/\/$/, "") + "/api";

console.log("Speech-to-Speech (via Gemini+ElevenLabs) BACKEND =", BACKEND);

export default function SpeechToSpeech() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [audioUrl, setAudioUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [voices, setVoices] = useState([]);
  const [selectedVoice, setSelectedVoice] = useState("");

  // ------------------------------------
  // 🔊 Load ElevenLabs voices
  // ------------------------------------
  useEffect(() => {
    async function loadVoices() {
      try {
        const res = await fetch(`${BACKEND}/voices`);
        if (!res.ok) {
          console.error("Voices fetch failed:", res.status, res.statusText);
          return;
        }

        const data = await res.json();
        const list = Array.isArray(data.voices) ? data.voices : [];

        const normalized = list
          .map((v) => ({
            id: v.voice_id || v.id,
            name: v.name,
            gender: v.labels?.gender || v.gender || "",
          }))
          .filter((v) => v.id);

        setVoices(normalized);
        if (normalized.length > 0) setSelectedVoice(normalized[0].id);

      } catch (err) {
        console.error("Voice load error:", err);
      }
    }

    loadVoices();
  }, []);

  // ------------------------------------
  // 🔁 Voice Transform (Speech → Text → AI Speech)
  // ------------------------------------
  const handleConversion = async () => {
    if (!selectedFile) return alert("Upload a voice file!");
    if (!selectedVoice) return alert("Select a voice!");

    setLoading(true);
    setAudioUrl(null);

    try {
      const form = new FormData();
      form.append("file", selectedFile);
      form.append("voiceId", selectedVoice);

      // NEW working backend route:
      const res = await fetch(`${BACKEND}/voice-transform`, {
        method: "POST",
        body: form,
      });

      if (!res.ok) {
        console.error("Voice Transform failed:", await res.text());
        throw new Error("Conversion failed");
      }

      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      setAudioUrl(url);

    } catch (err) {
      console.error(err);
      alert("Something went wrong!");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen flex flex-col items-center justify-center bg-gray-50 p-6">
      <div className="bg-white shadow-lg rounded-2xl p-8 w-full max-w-md border text-center">
        <h1 className="text-xl font-bold mb-4">💬 Speech → Speech Conversion</h1>
        {/* description removed as requested */}

        {/* Voice selector */}
        <select
          className="w-full border p-3 rounded-lg mb-3"
          value={selectedVoice}
          onChange={(e) => setSelectedVoice(e.target.value)}
        >
          {voices.length > 0 ? (
            voices.map((v) => (
              <option key={v.id} value={v.id}>
                {v.name} {v.gender ? `— ${v.gender}` : ""}
              </option>
            ))
          ) : (
            <option>Loading voices...</option>
          )}
        </select>

        {/* File upload */}
        <input
          type="file"
          accept="audio/*"
          onChange={(e) => setSelectedFile(e.target.files?.[0] ?? null)}
          className="w-full border p-3 rounded-lg mb-4"
        />

        <button
          onClick={handleConversion}
          disabled={loading}
          className={`w-full py-3 rounded-lg text-white font-semibold ${
            loading ? "bg-gray-400" : "bg-purple-600 hover:bg-purple-700"
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
