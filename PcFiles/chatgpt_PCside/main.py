import asyncio
import websockets
import json
import multiprocessing as mp
from llama3_main import set_up_generator, get_response
import current_time
import transcribe
import time
import multiprocessing
from functools import partial
import json
import numpy as np
import base64
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
        string = string.replace("'", '')
        string = string.replace("*", '')
        string=string.lower()

    else:
        string = string.replace("*", '')

    return string

def check_prompt(prompt):
    prompt=prompt.lower()
    if("what" in prompt and "time" in prompt and "is" in prompt):
        return current_time.get_time("en")
    elif("what day" in prompt and "today" in prompt):
        return current_time.get_day("en")
    elif("che" in prompt and "giorno" in prompt):
        return current_time.get_day("it")
    elif("che" in prompt and "ore sono" in prompt):
        return current_time.get_time("it")
    elif("che" in prompt and "ora è" in prompt):
        return current_time.get_time()

    else:
        return ""

async def handle_audio(websocket,trascript_queue,brain_queue, whisper_model):
    
    try:
        data=await websocket.recv()
        data=json.loads(data)
        is_echo=data["is_echo"]
        encoded_audio = data["data"]
        print(type(encoded_audio))

        decoded_audio = base64.b64decode(encoded_audio.encode('utf-8'))

        with open("karpus.wav","wb") as f:
            f.write(decoded_audio)
            print("saved")
            f.close()
        
        result_dict= transcribe.transcribe_audio("karpus.wav",whisper_model)
        result=result_dict["text"]

        result=remove_quotes(result,False) # remove from transcription quotes and duble quotes
        if(is_echo):
            response=check_prompt(result) # check if time is asked
            #### aggiungere la parte dello zero shot classification

        else: # se is_echo e' nulla significa che non e' stata fatta una richiesta specifica e la domanda va passata a llama
            print("questo e' il risultato "+result)
            cache_json=np.empty(1000000,dtype=dict)
            counter=0
            try:
                with open("cache.text", "r") as file:
                    for line in file:
                        cache_json[counter]=(json.loads(line))
                        counter=counter+1
                    file.close()
            except:
                print("cache vuota")
            for i in range(len(cache_json)):
                if(i<counter):
                    if(cache_json[i]["input"]==result):
                            print("input in cache ")
                            response=cache_json[i]["output"]
                            language=cache_json[i]["lan"]
                            await websocket.send(json.dumps({"text":response, "lan":language}))
                            return
            print("input nuovo elaboro con modello")

            trascript_queue.put(result)
            response=brain_queue.get()
            response=remove_quotes(response,True)
            with open("cache.text", "a") as file:
                file.write(json.dumps({"input":result,"output":response,"lan":result_dict["language"]}) + '\n')
                file.close()
            await websocket.send(json.dumps({"text":response, "lan":result_dict["language"]}))
        # else:
        #     print("processato")
        #     await websocket.send(json.dumps({"text":response, "lan":result_dict["language"]}))


    except websockets.exceptions.ConnectionClosedError:
        print("Connection closed unexpectedly")


def main_server_transcribe(trascript_queue,brain_queue):
    whisper_model=transcribe.setup_whisper()
    server_address = "0.0.0.0"
    server_port = 8700

    handle_audio_with_params = partial(handle_audio,trascript_queue=trascript_queue,brain_queue=brain_queue, whisper_model=whisper_model)

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
    # Create processes
    gpu_proc = multiprocessing.Process(target=gpu_process, args=(trascript_queue,brain_queue))
    cpu_proc = multiprocessing.Process(target=main_server_transcribe, args=(trascript_queue,brain_queue))
    
    # Start processes
    gpu_proc.start()
    time.sleep(120)
    cpu_proc.start()

    # Wait for both processes to finish
    # gpu_proc.join()
    # cpu_proc.join()
    
