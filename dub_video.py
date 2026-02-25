import os
import sys
import json
import asyncio
import subprocess
import numpy as np
import soundfile as sf

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
INPUT_VIDEO     = "training_video.mp4"
OUTPUT_VIDEO    = "output_dubbed.mp4"
START_TIME      = "00:02:36"
CLIP_DURATION   = "20"
TEMP_DIR        = "temp"

# ─────────────────────────────────────────────
# UTILS
# ─────────────────────────────────────────────
def run(cmd):
    print(f"\n▶ {' '.join(cmd)}")
    subprocess.run(cmd, check=True)

def get_duration(path):
    result = subprocess.run([
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "json", path
    ], capture_output=True, text=True)
    return float(json.loads(result.stdout)["format"]["duration"])

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

# ─────────────────────────────────────────────
# STEP 1: EXTRACT CLIP
# ─────────────────────────────────────────────
def extract_clip():
    print("\n[1/6] Extracting clip...")
    ensure_dir(TEMP_DIR)
    run([
        "ffmpeg", "-y",
        "-i", INPUT_VIDEO,
        "-ss", START_TIME,
        "-t", CLIP_DURATION,
        "-c", "copy",
        f"{TEMP_DIR}/clip.mp4"
    ])

# ─────────────────────────────────────────────
# STEP 2: EXTRACT AUDIO
# ─────────────────────────────────────────────
def extract_audio():
    print("\n[2/6] Extracting audio...")
    run([
        "ffmpeg", "-y",
        "-i", f"{TEMP_DIR}/clip.mp4",
        "-q:a", "0",
        "-map", "a",
        f"{TEMP_DIR}/kannada_audio.wav"
    ])

# ─────────────────────────────────────────────
# STEP 3: TRANSCRIBE (WHISPER)
# ─────────────────────────────────────────────
def transcribe():
    print("\n[3/6] Transcribing Kannada audio with Whisper...")
    import whisper
    model = whisper.load_model("large")
    result = model.transcribe(
        f"{TEMP_DIR}/kannada_audio.wav",
        language="kn",
        task="transcribe",
        fp16=False,
        condition_on_previous_text=False,
        temperature=0,
        best_of=5,
        beam_size=5
    )
    text = result["text"]
    print(f"\nKannada: {text}")
    with open(f"{TEMP_DIR}/kannada_text.txt", "w", encoding="utf-8") as f:
        f.write(text)
    return text

# ─────────────────────────────────────────────
# STEP 4: TRANSLATE (deep-translator)
# ─────────────────────────────────────────────
def translate(kannada_text):
    print("\n[4/6] Translating to Hindi...")
    from deep_translator import GoogleTranslator
    hindi_text = GoogleTranslator(source="kn", target="hi").translate(kannada_text)
    print(f"\nHindi: {hindi_text}")
    with open(f"{TEMP_DIR}/hindi_text.txt", "w", encoding="utf-8") as f:
        f.write(hindi_text)
    return hindi_text

# ─────────────────────────────────────────────
# STEP 5: GENERATE HINDI AUDIO (edge-tts)
# ─────────────────────────────────────────────
def generate_audio(hindi_text):
    print("\n[5/6] Generating Hindi audio with edge-tts...")
    import edge_tts

    async def _generate():
        communicate = edge_tts.Communicate(hindi_text, voice="hi-IN-SwaraNeural")
        await communicate.save(f"{TEMP_DIR}/hindi_raw.mp3")

    asyncio.run(_generate())

    # Speed match to video duration
    video_dur = get_duration(f"{TEMP_DIR}/clip.mp4")
    audio_dur = get_duration(f"{TEMP_DIR}/hindi_raw.mp3")
    atempo = audio_dur / video_dur
    print(f"\nVideo: {video_dur:.2f}s | Audio: {audio_dur:.2f}s | Atempo: {atempo:.3f}")

    # Handle atempo out of range (chain filters if needed)
    if atempo > 2.0:
        filter_str = "atempo=2.0,atempo={}".format(round(atempo/2, 3))
    elif atempo < 0.5:
        filter_str = "atempo=0.5,atempo={}".format(round(atempo/0.5, 3))
    else:
        filter_str = f"atempo={atempo:.3f}"

    run([
        "ffmpeg", "-y",
        "-i", f"{TEMP_DIR}/hindi_raw.mp3",
        "-filter:a", filter_str,
        f"{TEMP_DIR}/hindi_synced.wav"
    ])

# ─────────────────────────────────────────────
# STEP 6: LIP SYNC (Wav2Lip) — runs on Kaggle/Colab
# ─────────────────────────────────────────────
def lipsync():
    print("\n[6/6] Lip sync with Wav2Lip...")
    print("NOTE: Run this step on Kaggle/Colab with GPU.")
    print("Files needed:")
    print(f"  Video : {TEMP_DIR}/clip.mp4")
    print(f"  Audio : {TEMP_DIR}/hindi_synced.wav")
    print("\nWav2Lip command:")
    print("""
  ffmpeg -y -i clip.mp4 -r 25 clip_25fps.mp4
  ffmpeg -y -i clip_25fps.mp4 -vf "crop=960:1080:960:0" clip_lady.mp4

  python inference.py \\
    --checkpoint_path checkpoints/wav2lip_gan.pth \\
    --face clip_lady.mp4 \\
    --audio hindi_synced.wav \\
    --outfile result_lipsync.mp4 \\
    --pads 0 10 0 0 \\
    --nosmooth

  ffmpeg -y -i original_25fps.mp4 -i result_lipsync.mp4 \\
    -filter_complex "[0:v][1:v]overlay=960:0" \\
    -map 1:a \\
    -vf "unsharp=5:5:1.0:5:5:0.0" \\
    final_output.mp4
    """)

# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 50)
    print("  Supernan Dubbing Pipeline")
    print("=" * 50)

    extract_clip()
    extract_audio()
    kannada_text = transcribe()
    hindi_text = translate(kannada_text)
    generate_audio(hindi_text)
    lipsync()

    print("\n✅ Pipeline complete!")
    print(f"Upload {TEMP_DIR}/clip.mp4 and {TEMP_DIR}/hindi_synced.wav to Kaggle for lip sync.")