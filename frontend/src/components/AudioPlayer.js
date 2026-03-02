"use client";

import { Download } from "lucide-react";

export default function AudioPlayer({ audioUrl, filename = "audio.mp3" }) {
  if (!audioUrl) return null;

  return (
    <div className="mt-6 space-y-3">
      <audio controls className="w-full" src={audioUrl} />
      <a
        href={audioUrl}
        download={filename}
        className="flex items-center justify-center gap-2 bg-red-500 hover:bg-red-600 text-white py-2 rounded-lg"
      >
        <Download className="w-4 h-4" />
        Download
      </a>
    </div>
  );
}
