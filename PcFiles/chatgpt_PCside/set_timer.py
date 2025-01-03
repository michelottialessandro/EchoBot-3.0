from word2number_en_ita import w2n
import re
## il trhead che fa partire il tutto viene definito nel main.py per evitare di dover rimportare tutte le libreria 

def extract_info(text):
    numbers = re.findall(r'\d+', text)
    print(numbers)
    numbers = [int(num) for num in numbers]
    numero_secondi=numbers[0]

    if "minutes" in text or "minute" in text:
            #numero_secondi= w2n.word_to_num(text)
            numero_secondi=numero_secondi*60
    elif "hour" in text or "hours" in text:
            #numero_secondi= w2n.word_to_num(text)
            numero_secondi=numero_secondi*60*60
    elif "seconds" in text or "second" in text:
            #numero_secondi= w2n.word_to_num(text)
            numero_secondi=numbers[0]

 
    elif "minuti" in text or "minuto" in text:
            #numero_secondi= w2n.word_to_num(text)
            numero_secondi=numero_secondi*60
    elif "ore" in text or "ora" in text:
            #numero_secondi= w2n.word_to_num(text)
            numero_secondi=numero_secondi*60*60
    elif "secondi" in text or "secondo" in text:
            #numero_secondi= w2n.word_to_num(text)
            numero_secondi=numbers[0]

    return numero_secondi      



