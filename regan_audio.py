import asyncio
import edge_tts

async def generate():
    text = "एक और बात यह है कि जैसे ही आप घर पहुँचते हैं, जो घर बुक किया गया है, सबसे पहले यह जान लें कि आपको अपना सामान कहाँ रखना है। एक बार जब आप अपना सामान वहाँ रख देते हैं, तो पूछें कि आप अपने हाथ कहाँ धो सकते हैं और तुरंत जाकर हाथ धो लें। आपको साबुन या हैंडवॉश का इस्तेमाल करके ही अपने हाथ धोने चाहिए।"
    communicate = edge_tts.Communicate(text, voice="hi-IN-SwaraNeural")
    await communicate.save("temp/hindi_raw.mp3")
    print("Done!")

asyncio.run(generate())