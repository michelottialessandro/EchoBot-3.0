import json
import numpy as np
cache_json=np.empty(1000000,dtype=dict)
counter=0
result=" come stai oggi?"
try:
    with open("cache.text", "r") as file:
        for line in file:
            cache_json[counter]=(json.loads(line))
            counter=counter+1
        file.close()
        print(cache_json)
except:
    print("cache vuota")


for i in range(len(cache_json)):
    if(i<counter):
        if(cache_json[i]["input"]==result):
            print("input in cache ")
            