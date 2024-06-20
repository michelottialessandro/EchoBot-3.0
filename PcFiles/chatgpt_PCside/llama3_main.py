
from typing import List, Optional
import time
from llama import Dialog, Llama
import torch
import multiprocessing as mp
import soundfile as sf
import fire



   
    #modificare i parametri se serve !!!!!
def set_up_generator():
        print("setting up llama generator")
        generator = Llama.build(
        ckpt_dir= "Meta-Llama-3-8B-Instruct",
        tokenizer_path="Meta-Llama-3-8B-Instruct/tokenizer.model",
        max_seq_len=512,
        max_batch_size=4,   
    )
        print("setted up")
        return generator


def get_response(input,generator,max_gen_len=1536,temperature=0.6,top_p=0.9):
        print("sto processando l input")
        dialogs: List[Dialog] = [
        [{"role": "user", "content": input}],]
       
        ts = time.time()
        results = generator.chat_completion(
            dialogs,
            max_gen_len=max_gen_len,
            temperature=temperature,
            top_p=top_p,                    )
       
        for dialog, result in zip(dialogs, results):
            for msg in dialog:
                print(f"{msg['role'].capitalize()}: {msg['content']}\n")
            print(
                f"> {result['generation']['role'].capitalize()}: {result['generation']['content']}"
            )            
        ts2=time.time()
        print(ts2-ts)

        return result['generation']['content']



#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
 

# processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
    # model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts")
    # vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")

    # # Move the models and processor to CPU
    # device = torch.device("cpu")
    # model.to(device)
    # vocoder.to(device)

    # # Load embeddings dataset
    # embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
    # speaker_embeddings = torch.tensor(embeddings_dataset[7306]["xvector"]).unsqueeze(0).to(device)
  #per farlo parlare ma e' lento gira su cpu
        # song = AudioSegment.from_wav("speech.wav")
        # print('playing sound using  pydub')
        # play(song)
# p = mp.Process(target=text_speech, args=(result['generation']['content'],processor,device,speaker_embeddings,vocoder,model))
            # p.start()
            # p.join()
            # print("\n==================================\n")


#from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
#from transformers import VitsModel, AutoTokenizer

""" from pydub import AudioSegment
from pydub.playback import play
  """


# def text_speech(text,processor,device,speaker_embeddings,vocoder,model):

#     # Generate speech on CPU
#     inputs = processor(text=text, return_tensors="pt")
#     inputs = {key: tensor.to(device) for key, tensor in inputs.items()}

#     with torch.no_grad():
#         speech = model.generate_speech(inputs["input_ids"], speaker_embeddings, vocoder=vocoder)

#     # Save the speech
#     sf.write("speech.wav", speech.cpu().numpy(), samplerate=16000)