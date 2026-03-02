"use client";
import { useRef, useState } from "react";

export default function AudioRecorder({ onStop }) {
  const [recording, setRecording] = useState(false);
  const mediaRecorderRef = useRef(null);
  const chunksRef = useRef([]);

  const start = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorderRef.current = new MediaRecorder(stream);
    chunksRef.current = [];

    mediaRecorderRef.current.ondataavailable = (e) =>
      chunksRef.current.push(e.data);

    mediaRecorderRef.current.onstop = () => {
      const blob = new Blob(chunksRef.current, { type: "audio/webm" });
      onStop(blob);
    };

    mediaRecorderRef.current.start();
    setRecording(true);
  };

  const stop = () => {
    mediaRecorderRef.current?.stop();
    setRecording(false);
  };

  return (
    <button
      onClick={recording ? stop : start}
      className={`px-4 py-2 rounded text-white ${
        recording ? "bg-red-500" : "bg-indigo-600"
      }`}
    >
      {recording ? "Stop Recording" : "Record Voice"}
    </button>
  );
}
