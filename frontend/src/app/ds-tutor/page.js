"use client";

import { useState } from "react";
import Link from "next/link";
import useVoices from "@/hooks/useVoices";
import VoiceSelector from "@/components/VoiceSelector";
import AudioRecorder from "@/components/AudioRecorder";
import {
  uploadPDF,
  askDSTutor,
  askDSTutorSpeech,
} from "@/services/dsTutorApi";

export default function DSTutorPage() {
  const [text, setText] = useState("");
  const [input, setInput] = useState("");
  const [audioURL, setAudioURL] = useState(null);
  const [loading, setLoading] = useState(false);
  const [uploadMessage, setUploadMessage] = useState("");

  const { voices, selectedVoice, setSelectedVoice } = useVoices();

  const handlePDFUpload = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setLoading(true);

    try {
      const data = await uploadPDF(file);
      setUploadMessage(`✅ ${data.message}`);
    } catch {
      setUploadMessage("❌ Upload failed");
    } finally {
      setLoading(false);
    }
  };

  const handleTextSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    setLoading(true);

    try {
      const data = await askDSTutor(input, selectedVoice);
      setText(data.answer || data.text);
      setAudioURL(data.audio);
      setInput("");
    } catch {
      setText("❌ Request failed");
    } finally {
      setLoading(false);
    }
  };

  const handleVoiceStop = async (blob) => {
    setLoading(true);

    try {
      const data = await askDSTutorSpeech(blob, selectedVoice);
      setText(data.answer || data.text);
      setAudioURL(data.audio);
    } catch {
      setText("❌ Voice request failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-indigo-50 p-6">
      <div className="max-w-3xl mx-auto bg-white p-6 rounded-2xl shadow-lg">
        <h1 className="text-2xl font-bold mb-4">📚 DS Tutor</h1>

        <input type="file" accept=".pdf" onChange={handlePDFUpload} />

        {uploadMessage && (
          <p className="text-sm mt-2">{uploadMessage}</p>
        )}

        <VoiceSelector
          voices={voices}
          selectedVoice={selectedVoice}
          onChange={setSelectedVoice}
        />

        <div className="mt-4">
          <AudioRecorder onStop={handleVoiceStop} />
        </div>

        <form onSubmit={handleTextSubmit} className="mt-4 flex gap-2">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            className="flex-1 border p-2 rounded"
          />
          <button className="bg-indigo-600 text-white px-4 rounded">
            Send
          </button>
        </form>

        {loading && <p className="mt-4">Processing...</p>}

        {text && (
          <pre className="mt-4 bg-gray-100 p-3 rounded">{text}</pre>
        )}

        {audioURL && (
          <audio controls src={audioURL} className="mt-4 w-full" />
        )}

        <Link href="/" className="block mt-6 underline">
          ← Back to Home
        </Link>
      </div>
    </div>
  );
}
