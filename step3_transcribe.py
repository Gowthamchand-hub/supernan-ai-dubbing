import whisper

print("Loading Whisper large model...")
model = whisper.load_model("large")

print("Transcribing...")
result = model.transcribe(
    "kannada_audio.wav",
    language="kn",
    task="transcribe",
    fp16=False,
    verbose=True,
    condition_on_previous_text=False,
    temperature=0,
    best_of=5,
    beam_size=5
)

print("\nKannada Text:")
print(result["text"])

# Also print segments with timestamps
print("\nSegments with timestamps:")
for segment in result["segments"]:
    print(f"[{segment['start']:.1f}s - {segment['end']:.1f}s]: {segment['text']}")

with open("kannada_text.txt", "w", encoding="utf-8") as f:
    f.write(result["text"])

print("\nSaved to kannada_text.txt")