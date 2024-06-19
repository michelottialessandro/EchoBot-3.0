import speech_recognition as sr
import timeit
import whisper
import torch
import time
import numpy as np


model = whisper.load_model("medium")

print(torch.cuda.device_count())
print(torch.cuda.get_device_name(0))

if torch.cuda.is_available():
    print("PyTorch è configurato per utilizzare la GPU")
else:

    print("PyTorch è configurato per utilizzare la CPU")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

recognizer_instance = sr.Recognizer() # Crea una istanza del recognizer

keyWord = 'compute' # not computer cause can confuse with compute that
with sr.Microphone() as source:
    while True:
        print("sto ascoltando")
        recognizer_instance.adjust_for_ambient_noise(source)
        audio_data = recognizer_instance.listen(source)
        with open("speech_audio.wav", "wb") as file:
                file.write(audio_data.get_wav_data())  
        ts = timeit.default_timer()
        result = model.transcribe("speech_audio.wav")
        ts2 = timeit.default_timer()
        print("Tempo di esecuzione:", ts2 - ts, "secondi")
        print(result)
        time.sleep(4)
        # if(keyWord in result.lower()):
        #     print("im listening please go on")
        #     result = recognizer_instance.listen()
        #     if(result!=""):
        #         print(result)
        #         print('\n')
        #         print('\n')
        # else:
        #     print("non ho capito")
        #     #command = ["say", "i am sorry, i did not understand"]
        #     #subprocess.run(command,user="alessandromichelotti")