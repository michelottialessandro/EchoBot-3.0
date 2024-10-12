import asyncio
import time
import websockets
import websocket
import json
import os
#trasmette i dati ricevuti ad un altro server che gira su wsl 
#trasmette i file a il server su main.py

server_address = "0.0.0.0"
server_port = 8765

async def handle_audio(web_socket, path):
    
    encoded_audio = await web_socket.recv()
    print("connesso")
    uri = "ws://172.18.92.64:8700" #wsl ip
    ws=websocket.create_connection(uri)
    ws.send(encoded_audio)
    data=  ws.recv()
    print(type(data))
    print(data)
    response=json.loads(data)
    if(response["text"]=="shutdown"):
        print(response)
        await web_socket.send(data)
        os.system("shutdown /s /t 1") 
    else:
        print(response)
        await web_socket.send(data)



start_server = websockets.serve(handle_audio, server_address, server_port)

print(f"WebSocket server started at ws://{server_address}:{server_port}")

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
