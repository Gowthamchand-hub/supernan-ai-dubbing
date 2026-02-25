# Supernan AI Dubbing Pipeline

Automated Kannada → Hindi dubbing pipeline with lip sync.

## Pipeline Overview
1. **Extract clip** from source video (ffmpeg)
2. **Transcribe** Kannada audio (Whisper large)
3. **Translate** to Hindi (Google Translate via deep-translator)
4. **Generate Hindi audio** (Microsoft edge-tts - hi-IN-SwaraNeural)
5. **Lip sync** video to Hindi audio (Wav2Lip GAN)
6. **Enhance** video quality (ffmpeg unsharp filter)

## Setup

### Local (Mac/Linux)
```bash
git clone https://github.com/Gowthamchand-hub/supernan-ai-dubbing.git
cd supernan-ai-dubbing
python3.10 -m venv env
source env/bin/activate
pip install openai-whisper deep-translator edge-tts soundfile ffmpeg-python
brew install ffmpeg
```

### GPU (Kaggle/Colab)
```bash
git clone https://github.com/Rudrabha/Wav2Lip.git
pip install librosa==0.9.2
```

## Usage
```bash
python3 dub_video.py
```
Then upload `temp/clip.mp4` and `temp/hindi_synced.wav` to Kaggle and run the Wav2Lip inference step.

## Dependencies
- Python 3.10
- ffmpeg
- openai-whisper
- deep-translator
- edge-tts
- Wav2Lip (GPU required)

## Cost Estimate (per minute of video)
| Step | Tool | Cost |
|---|---|---|
| Transcription | Whisper (local) | ₹0 |
| Translation | deep-translator | ₹0 |
| TTS | edge-tts | ₹0 |
| Lip sync | Wav2Lip on Kaggle | ₹0 |
| **Total** | | **₹0** |

## Known Limitations
- Whisper sometimes misses words in noisy Kannada audio
- XTTS voice cloning degrades with cross-language reference audio
- Wav2Lip lips don't perfectly match during pauses in dubbed audio
- 60fps video needs conversion to 25fps for Wav2Lip

## What I'd Improve With More Time
- Use IndicTrans2 for better Kannada→Hindi translation
- Fine-tune XTTS with Hindi reference audio of same speaker
- Use VideoReTalking for better lip sync quality
- Add GFPGAN face restoration for sharper output
- Build batching system for long videos using silence detection

## Scaling to 500 Hours of Video
- Use AWS Spot instances with A100 GPUs
- Split videos into 30 second chunks using silence detection
- Process chunks in parallel across multiple GPUs
- Estimated cost: ~₹2-3 per minute at scale
