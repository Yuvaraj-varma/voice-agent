"use client";
import Link from "next/link";

export default function Home() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center bg-white text-gray-900 p-6 relative">
      {/* 🏠 Title */}
      <h1 className="absolute top-6 left-8 text-3xl font-bold text-gray-900 bg-gray-100 px-5 py-2 rounded-full shadow-md hover:shadow-lg hover:scale-105 transition-all cursor-pointer">
        Home
      </h1>

      {/* 👇 Image */}
      <div className="flex flex-col items-center -mt-20 mb-8">
        <img
          src="/talking-face.png"
          alt="Talking Face Icon"
          className="w-72 h-auto mb-10 transition-transform duration-500 hover:scale-105"
        />
      </div>

      {/* 🔘 Main Navigation Buttons */}
      <div className="flex flex-col sm:flex-row gap-8 items-center justify-center mt-[-20px]">
        
        {/* 🗣 Generate Voice */}
        <Link href="/generate-voice">
          <button className="flex items-center gap-2 px-10 py-4 text-lg font-semibold text-white bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full shadow-lg hover:scale-105 transition-transform">
            🗣 Generate Voice
          </button>
        </Link>

        {/* 💬 Speech → Speech */}
        <Link href="/speech-to-speech">
          <button className="flex items-center gap-2 px-10 py-4 text-lg font-semibold text-white bg-gradient-to-r from-pink-500 to-fuchsia-500 rounded-full shadow-lg hover:scale-105 transition-transform">
            💬 Speech → Speech
          </button>
        </Link>

        {/* 🎙 Voice Agent */}
        <Link href="/voice-agent">
          <button className="flex items-center gap-2 px-10 py-4 text-lg font-semibold text-white bg-gradient-to-r from-green-500 to-emerald-500 rounded-full shadow-lg hover:scale-105 transition-transform">
            🎙 Voice Agent
          </button>
        </Link>

      </div>
    </main>
  );
}
