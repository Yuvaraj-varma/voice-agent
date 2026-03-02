"use client";

import { useEffect, useState } from "react";
import { fetchVoices } from "@/services/voiceApi";

export default function useVoices() {
  const [voices, setVoices] = useState([]);
  const [selectedVoice, setSelectedVoice] = useState("");
  const [loadingVoices, setLoadingVoices] = useState(true);

  useEffect(() => {
    async function loadVoices() {
      try {
        const data = await fetchVoices();
        const list = Array.isArray(data.voices) ? data.voices : [];

        const normalized = list
          .map((v) => ({
            id: v.voice_id || v.id,
            name: v.name,
            gender: v.labels?.gender || v.gender || "",
          }))
          .filter((v) => v.id);

        setVoices(normalized);

        if (normalized.length > 0) {
          setSelectedVoice(normalized[0].id);
        }
      } catch (err) {
        console.error("Voice hook error:", err);
      } finally {
        setLoadingVoices(false);
      }
    }

    loadVoices();
  }, []);

  return {
    voices,
    selectedVoice,
    setSelectedVoice,
    loadingVoices,
  };
}
