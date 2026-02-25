from gtts import gTTS

with open("hindi_text.txt", "r", encoding="utf-8") as f:
    hindi_text = f.read()

print("Generating Hindi audio...")
tts = gTTS(hindi_text, lang="hi", slow=False)
tts.save("hindi_dubbed.mp3")

print("Hindi audio saved as hindi_dubbed.mp3!")