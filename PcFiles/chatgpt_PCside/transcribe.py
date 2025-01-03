import time
import whisper
import torch

# print(whisper.available_models())

# #modello scaricato in ./mnt/c/Users/Utente/.cache/whisper/medium.pt

# print(torch.cuda.device_count())
# print(torch.cuda.get_device_name(0))

# if torch.cuda.is_available():
#     print("PyTorch è configurato per utilizzare la GPU")
# else:

#     print("PyTorch è configurato per utilizzare la CPU")

def setup_whisper():
    device = torch.device("cuda")
    model = whisper.load_model("large-v3")
    model.to(device)
    print("model loaded")
    return model

def transcribe_audio(audio_file,model):
    ts = time.time()
    result = model.transcribe(audio_file,verbose=True) 
    ts2=time.time()
    print(ts2-ts)
    print(result["text"])
    return ({"text":result["text"],"no_speech_prob":result["segments"][0]["no_speech_prob"],"language":result["language"]})

