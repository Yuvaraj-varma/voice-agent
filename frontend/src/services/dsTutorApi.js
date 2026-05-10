import { BACKEND } from "@/config/api";

export async function uploadPDF(file, sessionId) {
  const form = new FormData();
  form.append("file", file);
  form.append("session_id", sessionId);

  const res = await fetch(`${BACKEND}/upload-invoice`, {
    method: "POST",
    body: form,
  });

  if (!res.ok) throw new Error("Upload failed");
  return res.json();
}

export async function askDSTutor(question, voiceId, includeAudio = false, sessionId = "default") {
  const payload = { question, session_id: sessionId };

  if (includeAudio && voiceId) {
    payload.includeAudio = true;
    payload.voiceId = voiceId;
  }

  const res = await fetch(`${BACKEND}/invoice-query`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
    signal: AbortSignal.timeout(120000),
  });

  if (!res.ok) throw new Error("Request failed");
  return res.json();
}

export async function askDSTutorSpeech(blob, voiceId) {
  const form = new FormData();
  form.append("file", blob, "input.webm");
  form.append("voiceId", voiceId);

  const res = await fetch(`${BACKEND}/ds-rag-speech`, {
    method: "POST",
    body: form,
  });

  if (!res.ok) throw new Error("Speech request failed");
  return res.json();
}
