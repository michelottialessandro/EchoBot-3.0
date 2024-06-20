import timeit
import whisper
import torch

model = whisper.load_model("medium")

print(torch.cuda.device_count())
print(torch.cuda.get_device_name(0))

if torch.cuda.is_available():
    print("PyTorch è configurato per utilizzare la GPU")
else:

    print("PyTorch è configurato per utilizzare la CPU")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def transcribe_audio(audio_file):
    ts = timeit.default_timer()
    result = model.transcribe(audio=audio_file)
    ts2 = timeit.default_timer()

    print("Tempo di esecuzione:", ts2 - ts, "secondi")


    print(result["text"])
#print("C:\\Users\\Utente\\Documents\\development\\Chat_gpt\\prova.mp3")
transcribe_audio("speech_audio.wav")

# import timeit 
# import torch
# import whisper
# import os
# model = whisper.load_model("medium")


# print(torch.cuda.device_count())
# print(torch.cuda.get_device_name(0))

# if torch.cuda.is_available():
#     print("PyTorch is configured to use the GPU")
# else:
#     print("PyTorch is configured to use the CPU")

# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# model.to(device)

# def transcribe_audio(audio_file):
#     ts = timeit.default_timer()
#     result = model.transcribe(audio_file)
#     ts2 = timeit.default_timer()

#     print("Execution time:", ts2 - ts, "seconds")

#     print(result["text"])

# file_path="prova.mp3"
# if os.path.exists(file_path):
#     print("File exists.")
# else:
#     print("File does not exist.")

# transcribe_audio(file_path)
