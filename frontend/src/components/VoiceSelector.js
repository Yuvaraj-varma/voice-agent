"use client";

export default function VoiceSelector({
  voices,
  selectedVoice,
  onChange,
  disabled = false,
}) {
  return (
    <select
      className="w-full border p-3 rounded-lg mb-3"
      value={selectedVoice}
      onChange={(e) => onChange(e.target.value)}
      disabled={disabled}
    >
      {voices.length > 0 ? (
        voices.map((v) => (
          <option key={v.id || v.voice_id} value={v.id || v.voice_id}>
            {v.name} {v.gender || v.labels?.gender ? `— ${v.gender || v.labels?.gender}` : ""}
          </option>
        ))
      ) : (
        <option>Loading voices...</option>
      )}
    </select>
  );
}
