"use client";
import { useState, useEffect } from "react";
import { Download } from "lucide-react";

export default function GenerateVoice() {
  const [text, setText] = useState("");
  const [audioUrl, setAudioUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [voices, setVoices] = useState([]);
  const [selectedVoice, setSelectedVoice] = useState("");
  const [charCount, setCharCount] = useState(0);

  // Backend URL
  const BACKEND = process.env.NEXT_PUBLIC_BACKEND_URL || "http://127.0.0.1:8000";

  // 🧠 Fetch voices from backend → /api/voices
  useEffect(() => {
    const fetchVoices = async () => {
      try {
        const res = await fetch(`${BACKEND}/api/voices`);
        const data = await res.json();

        if (data.voices) {
          setVoices(data.voices);
          setSelectedVoice(data.voices[0].voice_id);
        } else {
          console.warn("Voice response error:", data);
        }
      } catch (err) {
        console.error("Error fetching voices:", err);
      }
    };

    fetchVoices();
  }, []);

  // ✍️ Handle text change
  const handleTextChange = (e) => {
    const val = e.target.value.slice(0, 500);
    setText(val);
    setCharCount(val.length);
  };

  // 🎤 Generate speech → /api/speech
  const handleGenerate = async () => {
    if (!text.trim()) {
      alert("Please enter text!");
      return;
    }

    setLoading(true);
    setAudioUrl(null);

    try {
      const res = await fetch(`${BACKEND}/api/speech`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text, voiceId: selectedVoice }),
      });

      if (!res.ok) throw new Error("Speech generation failed!");

      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      setAudioUrl(url);
    } catch (err) {
      console.error(err);
      alert("Failed to generate voice!");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen flex flex-col items-center justify-center bg-gray-50 p-6">
      <div className="w-full max-w-md bg-white shadow-lg rounded-2xl p-8 border border-gray-100">
        <h1 className="text-xl font-bold mb-4 text-center text-gray-900">
          🎤 Generate Realistic Voices Instantly
        </h1>

        {/* Text Input */}
        <textarea
          value={text}
          onChange={handleTextChange}
          placeholder="Type something to convert..."
          className="w-full border border-gray-300 rounded-lg p-3 resize-none focus:ring-2 focus:ring-indigo-400"
          rows={4}
        />
        <p className="text-sm text-gray-500 text-right">
          {charCount}/500
        </p>

        {/* Voice Selector */}
        <select
          value={selectedVoice}
          onChange={(e) => setSelectedVoice(e.target.value)}
          className="w-full border border-gray-300 rounded-lg p-3 mt-3 text-gray-800 bg-white"
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

        {/* Generate Button */}
        <button
          onClick={handleGenerate}
          disabled={loading}
          className={`w-full mt-5 py-3 rounded-lg font-semibold text-white transition-all ${
            loading
              ? "bg-gray-400"
              : "bg-gradient-to-r from-blue-500 to-pink-500 hover:scale-105 shadow-md"
          }`}
        >
          {loading ? "Generating..." : "✨ Generate Voice"}
        </button>

        {/* Audio Output */}
        {audioUrl && (
          <div className="mt-6 space-y-3 text-center">
            <audio controls className="w-full rounded-lg" src={audioUrl} />
            <a
              href={audioUrl}
              download="voice.mp3"
              className="flex items-center justify-center gap-2 bg-red-500 hover:bg-red-600 text-white py-2 rounded-lg font-semibold"
            >
              <Download className="w-4 h-4" />
              Download
            </a>
          </div>
        )}

        {/* Back */}
        <div className="text-center mt-6">
          <a href="/" className="text-gray-600 hover:text-gray-900 font-semibold underline">
            ← Back to Home
          </a>
        </div>
      </div>
    </main>
  );
}
