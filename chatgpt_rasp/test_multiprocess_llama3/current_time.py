from datetime import datetime
import pytz
def get_time(lan):
    italy_timezone = pytz.timezone('Europe/Rome')

    current_time_italy = datetime.now(italy_timezone)

    formatted_time_italy = current_time_italy.strftime("%H:%M")
    if(lan=="en"):
        return (f"It is {formatted_time_italy}")
    else:
        return (f"Sono le {formatted_time_italy}")

def get_day(lan):
    italy_timezone = pytz.timezone('Europe/Rome')

    current_time_italy = datetime.now(italy_timezone)

    formatted_time_italy = current_time_italy.strftime("%Y-%m-%d")
    
    if(lan=="en"):
        return (f"Today is {formatted_time_italy}")
    else:
        return (f"Oggi è {formatted_time_italy}")

