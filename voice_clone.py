from TTS.api import TTS
import soundfile as sf
import numpy as np

tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")

texts = [
    "एक और बात यह है कि जैसे ही आप घर पहुँचते हैं जो घर बुक किया गया है सबसे पहले यह जान लें कि आपको अपना सामान कहाँ रखना है।",
    "एक बार जब आप अपना सामान वहाँ रख देते हैं तो पूछें कि आप अपने हाथ कहाँ धो सकते हैं और तुरंत जाकर हाथ धो लें। आपको साबुन या हैंडवॉश का इस्तेमाल करके ही अपने हाथ धोने चाहिए।"
]

all_audio = []
silence = np.zeros(int(24000 * 0.3))  # 0.3 seconds silence between chunks

for i, text in enumerate(texts):
    print(f"Generating part {i+1}...")
    wav = tts.tts(
        text=text,
        speaker_wav="kannada_reference.wav",
        language="hi"
    )
    all_audio.extend(wav)
    if i < len(texts) - 1:
        all_audio.extend(silence)  # add silence between chunks

sf.write("hindi_cloned.wav", np.array(all_audio), 24000)
print("Done! Saved as hindi_cloned.wav")