from deep_translator import GoogleTranslator

with open("kannada_text.txt", "r", encoding="utf-8") as f:
    kannada_text = f.read()

print("Kannada text:")
print(kannada_text)

hindi_text = GoogleTranslator(source="kn", target="hi").translate(kannada_text)

print("\nHindi translation:")
print(hindi_text)

with open("hindi_text.txt", "w", encoding="utf-8") as f:
    f.write(hindi_text)

print("\nSaved to hindi_text.txt")