import speech_recognition as sr
import websocket
ws=websocket.create_connection("ws://alemac:8765")

r = sr.Recognizer() # Crea una istanza del recognizer

with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source)
with open("audio.wav", "wb") as f:
    f.write(audio.get_wav_data())