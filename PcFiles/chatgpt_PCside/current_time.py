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
    giorni=["lunedì", "martedì", "mercoledì","giovedì","venerdì","sabato","domenica"]
    
    days=["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
    
    mesi=["gennaio","febbraio","marzo","aprile","maggio","giugno","luglio","agosto","settembre","ottobre","novembre","dicembre"]
    
    months=["january","february","march","april","may","june", "july","august","september","october","november","december"]
    
    italy_timezone = pytz.timezone('Europe/Rome')

    current_time_italy = datetime.now(italy_timezone)
    

    formatted_time_italy = current_time_italy.strftime("%Y-%m-%d")
    
    week_day=current_time_italy.weekday()  #monday =0 sunday=6
    
    date=formatted_time_italy.split("-")
    
    for x in range(len(date)):
        date[x]=int(date[x])
    
    print(date)
    
    if(lan=="en"):
        year=date[0]
        month=date[1]
        day=date[2]
        week_day_name=days[week_day]
        month_name=months[month-1]
        return (f"Today is {week_day_name}, {day} of {month_name}, {year}")
    else:
        anno=date[0]
        mese=date[1]
        giorno=date[2]
        giorno_nome=giorni[week_day]
        mese_nome=mesi[mese-1]
        return (f"Oggi è {giorno_nome}, {giorno}  {mese_nome}, {anno}")




print(get_day("en"))