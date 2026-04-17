import { BACKEND } from "../config/api";

export async function fetchVoices() {
  const res = await fetch(`${BACKEND}/voices`, { signal: AbortSignal.timeout(60000) });
  if (!res.ok) throw new Error("Failed to fetch voices");
  return res.json();
}

export async function transformVoice(file, voiceId) {
  const form = new FormData();
  form.append("file", file);
  form.append("voiceId", voiceId);

  const res = await fetch(`${BACKEND}/voice-transform`, {
    method: "POST",
    body: form,
    signal: AbortSignal.timeout(60000),
  });

  if (!res.ok) throw new Error("Voice transform failed");
  return res.blob();
}
