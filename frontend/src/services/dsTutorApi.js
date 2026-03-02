import { BACKEND } from "@/config/api";

export async function uploadPDF(file) {
  const form = new FormData();
  form.append("file", file);

  const res = await fetch(`${BACKEND}/upload-pdf`, {
    method: "POST",
    body: form,
  });

  if (!res.ok) throw new Error("Upload failed");
  return res.json();
}

export async function askDSTutor(question, voiceId) {
  const res = await fetch(`${BACKEND}/ds-rag-voice`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question, voiceId }),
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
