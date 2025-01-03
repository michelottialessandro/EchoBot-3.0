import time
import keyboard
import threading
from playsound import playsound
import random
import multiprocessing


def set_timer(duration):
    stop_event = threading.Event()
    
    def play_sound(stop_event):
        try:
            while not stop_event.is_set():
                playsound("prova2.wav")
                #print("playing")
        except Exception as e:
            print(f"Errore durante la riproduzione del suono: {e}")

    print(f"Timer impostato per {duration} secondi.")
    time.sleep(duration)
    print("Timer scaduto!")

    sound_thread = threading.Thread(target=play_sound, args=(stop_event,), daemon=True)
    sound_thread.start()

    print("Premi 'a' per fermare il suono.")
    while not stop_event.is_set():
        if keyboard.is_pressed("a"):
            print("Interrompo il suono...")
            stop_event.set()
            break


if __name__ == '__main__':
    processes = []
    
    for i in range(5):
        duration = random.randint(5, 30)
        proc = multiprocessing.Process(target=set_timer, args=(duration,))
        processes.append(proc)
        proc.start()

    for proc in processes:
        proc.join()
