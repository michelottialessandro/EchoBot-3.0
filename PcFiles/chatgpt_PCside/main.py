import asyncio
import websockets
from llama3_main import set_up_generator, get_response
import current_time
import transcribe
import time
import multiprocessing
from functools import partial
import json
import numpy as np
import base64
from transformers import pipeline
from wordTonumber import create_expression
import os
from lights import lights_manager
import joblib
from set_timer import extract_info
import threading
spegnimento=["buonanotte","buona notte","good night", "goodnight","spegni","spegniti","shutdown","shut down"]

svm_classifier=joblib.load("svm_model.pkl")
vectorizer=joblib.load("vectorizer.pkl")



def classify(text):
    new_phrase=[]
    new_phrase.append(text)
    
    new_phrase_tfidf = vectorizer.transform(new_phrase)
    prediction=svm_classifier.predict(new_phrase_tfidf)
    
    return prediction[0]


def tronca_all_ultimo_punto(testo):
    ultimo_punto = testo.rfind('.')
    if ultimo_punto == -1:
        return testo
    troncato = testo[:ultimo_punto + 1]
    troncato = troncato.replace('"', '')
    troncato = troncato.replace("'", '')
    return troncato

def remove_quotes(string,is_response):
    if(is_response==False):
        string = string.replace('"', '')
        string = string.replace("'", "")
        string = string.replace("*", "")
        string=string.lower()

    else:
        string = string.replace("*", '')

    return string


async def handle_audio(websocket,trascript_queue_classifier,trascript_queue,brain_queue, whisper_model):
   
    try:
        data=await websocket.recv()
        data=json.loads(data)
        is_echo=data["is_echo"]
        encoded_audio = data["data"]
        print(type(encoded_audio))
        print(f"Received audio data of type: {type(encoded_audio)}")
        decoded_audio = base64.b64decode(encoded_audio.encode('utf-8'))

        with open("karpus.wav","wb") as f:
            f.write(decoded_audio)
            print("saved")
        
        result_dict= transcribe.transcribe_audio("karpus.wav",whisper_model)
        result=result_dict["text"]
        result=remove_quotes(result,False) # remove from transcription quotes and duble quotes
        
        if(is_echo):
            #understand class of result transcription 
            # classification=classifier(result, candidate_labels)
            # class_=classification["labels"][0]
            print("sto usando il classifier")
            prov=result.lower()
            prov=prov.replace(".","")
            print(prov)
            if(prov in spegnimento):
                await websocket.send(json.dumps({"text":"shutdown"}))
                os.system('sudo shutdown now')

            #trascript_queue_classifier.put(result)
            #class_=brain_queue.get()
            class_=classify(result)
            print(class_)
            if(class_=="time"):
                response=current_time.get_time("en")
                await websocket.send(json.dumps({"text":response, "lan":"en"}))
            elif(class_=="orario"):
                response=current_time.get_time("it")
                await websocket.send(json.dumps({"text":response, "lan":"it"}))
                
            elif(class_=="date"):
                response=current_time.get_day("en")
                await websocket.send(json.dumps({"text":response, "lan":"en"}))
                
            elif(class_=="data"):
                response=current_time.get_day("it")
                await websocket.send(json.dumps({"text":response, "lan":"it"}))
            
            elif(class_=="calculation"):
                print("performing calculation")
                try:
                    result=create_expression(result)
                    await websocket.send(json.dumps({"text":str(result), "lan":result_dict["language"]}))
                except Exception as e:
                    print(f"There has been a server internal error during calculation: {e}")
                    await websocket.send(json.dumps({"text":"There has been a server internal error during calculation", "lan":"en"}))

            elif(class_=="lights_on"):
                print("turn on")
                lights_manager(True,result)
                await websocket.send(json.dumps({"text":"turn on", "lan":result_dict["language"]}))
            
            elif(class_=="luci_accese"):
                print("turn on")
                lights_manager(True,result)
                await websocket.send(json.dumps({"text":"Luci accese", "lan":"it"}))
            
            elif(class_=="lights_off"):
                print("turn off")
                lights_manager(is_on=False,text="")
                await websocket.send(json.dumps({"text":"turn off", "lan":result_dict["language"]}))
            
            elif(class_=="luci_spente"):
                print("turn off")
                lights_manager(is_on=False,text="")
                await websocket.send(json.dumps({"text":"luci spente", "lan":"it"}))
            
            elif(class_=="timer_en"):
                time=extract_info(text=result)
                await websocket.send(json.dumps({"text":"timer is set", "lan":"en","time":time}))

            elif(class_=="alarm"):
                print("Setting an allert")
                
            elif(class_=="low confidence"):
                print(class_)
                await websocket.send(json.dumps({"text":"I did not understand, please repeat.", "lan":result_dict["language"]}))

               
        else: # se is_echo e' nulla significa che non e' stata fatta una richiesta specifica e la domanda va passata a llama
            print("questo e' il risultato "+result)
            cache_json=np.empty(1000000,dtype=dict)
            counter=0
            try:
                with open("cache.text", "r") as file:
                    for line in file:
                        cache_json[counter]=(json.loads(line))
                        counter=counter+1
            except Exception as e:
                print(f"Error reading cache: {e}")
            for i in range(len(cache_json)):
                if(i<counter):
                    if(cache_json[i]["input"]==result):
                            print("input in cache ")
                            response=cache_json[i]["output"]
                            language=cache_json[i]["lan"]
                            await websocket.send(json.dumps({"text":response, "lan":language}))
                            return
            
            
            print("input nuovo elaboro con modello")

            trascript_queue.put(result)   # inserisce la trascrizione in questa coda cosi che il processo gpu_process potra' leggerla e iniziare l elaborazione
            response=brain_queue.get()
            response=remove_quotes(response,True)
            with open("cache.text", "a") as file:
                file.write(json.dumps({"input":result,"output":response,"lan":result_dict["language"]}) + '\n')
                file.close()
            await websocket.send(json.dumps({"text":response, "lan":result_dict["language"]}))
       


    except websockets.exceptions.ConnectionClosedError:
        print("Connection closed unexpectedly")


def main_server_transcribe(trascript_queue_classifier,trascript_queue,brain_queue):
    whisper_model=transcribe.setup_whisper()
    server_address = "0.0.0.0"
    server_port = 8700

    handle_audio_with_params = partial(handle_audio,trascript_queue_classifier=trascript_queue_classifier,trascript_queue=trascript_queue,brain_queue=brain_queue, whisper_model=whisper_model)

    start_server = websockets.serve(handle_audio_with_params, server_address, server_port,)

    print(f"WebSocket server started at ws://{server_address}:{server_port}")

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

def gpu_process(trascript_queue,brain_queue):
    generator=set_up_generator()
    while True:
        message = trascript_queue.get()
        print('sto processando '+message)
        result=get_response(message,generator)
        brain_queue.put(result)


if __name__ == '__main__':
    # Create a multiprocessing Queue
    trascript_queue = multiprocessing.Queue()
    brain_queue=  multiprocessing.Queue()
    trascript_queue_classifier= multiprocessing.Queue()
    # Create processes
    gpu_proc = multiprocessing.Process(target=gpu_process, args=(trascript_queue,brain_queue))
    cpu_proc = multiprocessing.Process(target=main_server_transcribe, args=(trascript_queue_classifier,trascript_queue,brain_queue))
   
    gpu_proc.start()
    time.sleep(120)
  
    cpu_proc.start()

    
