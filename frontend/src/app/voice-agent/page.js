"use client";
import { useState, useRef, useEffect } from "react";
import Link from "next/link";

export default function VoiceAgentPage() {
  const [audioURL, setAudioURL] = useState(null);
  const [text, setText] = useState("");
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [recording, setRecording] = useState(false);
  const [voices, setVoices] = useState([]);
  const [selectedVoice, setSelectedVoice] = useState("21m00Tcm4TlvDq8ikWAM"); // ✅ Default to Rachel (real ElevenLabs voice)
  const [isPlaying, setIsPlaying] = useState(false);
  const [isPaused, setIsPaused] = useState(false);

  const mediaRecorderRef = useRef(null);
  const audioChunks = useRef([]);
  const currentAudioRef = useRef(null);

  const BACKEND =
  (process.env.NEXT_PUBLIC_BACKEND_URL || "http://127.0.0.1:8000") + "/api";


  // 🎶 Fetch available ElevenLabs voices on page load
  useEffect(() => {
    async function fetchVoices() {
      try {
        const res = await fetch(`${BACKEND}/voices`);
        const data = await res.json();
        setVoices(data.voices || []);
      } catch (err) {
        console.error("Error fetching voices:", err);
      }
    }
    fetchVoices();
  }, []);

  // 🎙️ Start mic recording
  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorderRef.current = new MediaRecorder(stream);
      audioChunks.current = [];

      mediaRecorderRef.current.ondataavailable = (event) => {
        if (event.data.size > 0) audioChunks.current.push(event.data);
      };

      mediaRecorderRef.current.onstop = handleStop;
      mediaRecorderRef.current.start();
      setRecording(true);
      setText("🎤 Listening...");
    } catch (err) {
      console.error("Mic access error:", err);
      setText("❌ Please allow microphone access.");
    }
  };

  // ⏹ Stop recording
  const stopRecording = () => {
    if (mediaRecorderRef.current?.state !== "inactive") {
      mediaRecorderRef.current.stop();
      setRecording(false);
      setText("⏳ Processing your voice...");
    }
  };

  // 🧠 Send voice to backend
  const handleStop = async () => {
    const audioBlob = new Blob(audioChunks.current, { type: "audio/webm" });
    const formData = new FormData();
    formData.append("file", audioBlob, "input.webm");
    formData.append("voiceId", selectedVoice);
    await sendRequest(`${BACKEND}/agent`, formData);
  };

  // 💬 Handle text query
  const handleTextSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;
    stopAudio(); // stop current voice before next
    const body = JSON.stringify({ text: input, voiceId: selectedVoice });
    await sendRequest(`${BACKEND}/text-agent`, body, true);
  };

  // 🔄 Send voice/text to backend
  const sendRequest = async (url, body, isJSON = false) => {
    setLoading(true);

    try {
      const res = await fetch(url, {
        method: "POST",
        body,
        ...(isJSON && { headers: { "Content-Type": "application/json" } }),
      });

      if (!res.ok) throw new Error("Backend error");
      const data = await res.json();

      setText(`🗣 You: ${data.userText}\n\n🤖 AI: ${data.text}`);
      setAudioURL(data.audio); // ✅ keep audio visible after playback
      setInput("");
    } catch (err) {
      console.error("Error:", err);
      setText("❌ Something went wrong while processing your query.");
    } finally {
      setLoading(false);
    }
  };

  // 🎧 Auto-play ElevenLabs voice reply
  useEffect(() => {
    if (audioURL) {
      stopAudio();
      const audio = new Audio(audioURL);
      currentAudioRef.current = audio;
      setIsPlaying(true);
      setIsPaused(false);
      audio.play().catch((err) =>
        console.error("Audio playback error:", err)
      );

      audio.onended = () => {
        // ✅ Keep audio visible after completion
        setIsPlaying(false);
        setIsPaused(false);
      };
    }
  }, [audioURL]);

  // 🛑 Pause
  const stopAudio = () => {
    if (currentAudioRef.current) {
      currentAudioRef.current.pause();
      setIsPlaying(false);
      setIsPaused(true);
    }
  };

  // ▶ Resume
  const resumeAudio = () => {
    if (currentAudioRef.current && isPaused) {
      currentAudioRef.current.play();
      setIsPlaying(true);
      setIsPaused(false);
    }
  };

  // 🔁 Stop Completely
  const resetAudio = () => {
    if (currentAudioRef.current) {
      currentAudioRef.current.pause();
      currentAudioRef.current.currentTime = 0;
      setIsPlaying(false);
      setIsPaused(false);
    }
  };

  // 🔁 Replay (Manual replay after finish)
  const replayAudio = () => {
    if (audioURL) {
      const replay = new Audio(audioURL);
      replay.play();
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-b from-green-50 to-white p-6">
      <div className="w-full max-w-md bg-white shadow-xl rounded-3xl p-6 border text-center">
        <h1 className="text-2xl font-bold mb-2 text-green-700">
          🎙️ Agentic Voice Assistant
        </h1>
        <p className="text-gray-600 mb-4 text-sm">
          Speak or type your question — I’ll respond with both text and voice.
        </p>

        {/* 🎚 Voice Selector */}
        <div className="flex items-center justify-center mb-4 gap-2">
          <label className="text-sm font-medium text-gray-700">Voice:</label>
          <select
            className="border rounded-lg p-2 text-sm text-gray-700"
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
        </div>

        {/* 🎤 Mic Button */}
        <button
          onClick={recording ? stopRecording : startRecording}
          className={`relative w-16 h-16 flex items-center justify-center rounded-full text-3xl text-white shadow-lg transition-all duration-300 ${
            recording
              ? "bg-red-500 scale-105 animate-pulse"
              : "bg-green-500 hover:bg-green-600 hover:scale-105"
          }`}
        >
          {recording ? "⏹" : "🎤"}
          {recording && (
            <span className="absolute inset-0 rounded-full border-4 border-red-300 animate-ping"></span>
          )}
        </button>

        {/* 💬 Text Input */}
        <form
          onSubmit={handleTextSubmit}
          className="mt-5 flex items-center gap-2 justify-center"
        >
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask your question..."
            className="flex-1 border rounded-lg p-2 w-64 text-gray-800 text-sm shadow-sm focus:ring-2 focus:ring-green-400"
          />
          <button
            type="submit"
            className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg text-sm transition-all"
          >
            Send
          </button>
        </form>

        {/* 🌀 Loading */}
        {loading && (
          <p className="text-blue-500 mt-4 text-sm animate-pulse">
            Processing...
          </p>
        )}

        {/* 💬 Text Output */}
        {text && (
          <pre className="mt-4 p-3 bg-gray-100 rounded-lg text-left whitespace-pre-wrap text-sm text-gray-800 border border-gray-200">
            {text}
          </pre>
        )}

        {/* 🎧 Audio Controls */}
        {audioURL && (
          <div className="flex flex-col items-center mt-3">
            <audio controls src={audioURL} className="w-full rounded-lg" />

            {/* 🛑 / ▶ / 🔁 Buttons */}
            {isPlaying && (
              <button
                onClick={stopAudio}
                className="mt-3 bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg text-sm transition-all"
              >
                🛑 Pause Voice
              </button>
            )}
            {isPaused && (
              <div className="flex justify-center mt-3 gap-3">
                <button
                  onClick={resumeAudio}
                  className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg text-sm transition-all"
                >
                  ▶ Resume
                </button>
                <button
                  onClick={resetAudio}
                  className="bg-gray-500 hover:bg-gray-600 text-white px-4 py-2 rounded-lg text-sm transition-all"
                >
                  🔁 Stop Completely
                </button>
              </div>
            )}

            {/* 🔁 Replay Button */}
            <button
              onClick={replayAudio}
              className="mt-3 bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg text-sm transition-all"
            >
              🔂 Replay Voice
            </button>
          </div>
        )}

        {/* 🏠 Back Link */}
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
