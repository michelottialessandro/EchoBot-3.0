import websocket
import json
websocket_url = "ws://192.168.178.43/ws"
ws_esp=websocket.create_connection(websocket_url)


def lights_manager(is_on,text):
    if(is_on):
        if("blu" in text or "blue" in text):
            json_data=json.dumps({"command":"BLUE","value":[0,0,255]})
            ws_esp.send(json_data)
            print("turing on blue")
        elif("red"in text or "ross" in text): #potrebbe essere sia rosse sia rosso 
            json_data=json.dumps({"command":"RED","value":[0,0,255]})
            ws_esp.send(json_data)
            print("turning on red")
        elif("green" in text or "verd" in text): 
            json_data=json.dumps({"command":"GREEN","value":[0,0,255]})
            ws_esp.send(json_data)
            print("turining on green")
        elif("purple" in text or "viol" in text): 
            json_data=json.dumps({"command":"SET","value":[172,0,150]})
            ws_esp.send(json_data)
            print("turining on pruple")
        elif("yellow" in text or "giall" in text): 
            json_data=json.dumps({"command":"SET","value":[255,56,0]})
            ws_esp.send(json_data)
            print("turining on yellow")
        else:
            json_data=json.dumps({"command":"BLUE","value":[0,0,255]})
            ws_esp.send(json_data)
            print("turning on blue beacause non of preavius")
    else:
        json_data=json.dumps({"command":"OFF","value":[0,0,0]})
        ws_esp.send(json_data)
        print("turning off")


