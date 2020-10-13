import PySimpleGUI as sg
import urllib3
from bs4 import BeautifulSoup
import os
import requests

def schGetter (id):
    html = "https://www.vyatsu.ru/studentu-1/spravochnaya-informatsiya/raspisanie-zanyatiy-dlya-studentov.html"
    # group = "143851"

    http = urllib3.PoolManager()

    response = http.request('GET',html)
    soup = BeautifulSoup(response.data, 'html.parser')

    div = soup.find('div', id=idGroup)
    # print (div)

    url = str(div)
    clean_url = ''

    for i in range(0, len(url)): 
        if i > 79:
            if i < 133:  
                clean_url = clean_url + url[i]

    if os.path.exists(r'E:\download.txt'):
        result = open(r'E:\download.txt', "r")
        prev_url = result.read()
        if prev_url == clean_url:
            f = open(r'E:\schedule_temp.pdf',"wb")
            file_get = requests.get("https://www.vyatsu.ru" + clean_url)
            f.write(file_get.content)
            if os.path.exists(r'E:\schedule.pdf'):
                if os.path.getsize(r'E:\schedule_temp.pdf') == os.path.getsize(r'E:\schedule.pdf'):
                    print("У Вас последняя версия расписания!")
                    f.close()
                    result.close()
                    os.remove('E:\schedule_temp.pdf')
                    print("Открываю расписание...")
                    os.startfile("E:\schedule.pdf")
            else:
                print("Обновляю расписание...")
                f.close()
                result.close()
                os.remove('E:\schedule.pdf')
                os.rename('E:\schedule_temp.pdf', 'E:\schedule.pdf')
                print("Открываю расписание...")
                os.startfile("E:\schedule.pdf")
            
        else:
            print("Обновляю расписание...")
            # sg.Print("Обновляю расписание...")
            result.close()
            f = open(r'E:\schedule.pdf',"wb")
            file_get = requests.get("https://www.vyatsu.ru" + clean_url)
            f.write(file_get.content)
            print("Открываю расписание...")
            # sg.Print("Открываю расписание...")
            os.startfile("E:\schedule.pdf")
            result = open(r'E:\download.txt', "w")
            result.write(clean_url)
            result.close
            f.close()

    else:
        result = open(r"E:\download.txt", "w")
        result.write(clean_url)
        print("Обновляю расписание...")
        # sg.Print("Обновляю расписание...")
        result.close()
        f = open(r'E:\schedule.pdf',"wb")
        file_get = requests.get("https://www.vyatsu.ru" + clean_url)
        f.write(file_get.content)
        print("Открываю расписание...")
        # sg.Print("Открываю расписание...")
        os.startfile("E:\schedule.pdf")
        result.close()
        f.close()

sg.theme('DefaultNoMoreNagging') 

layout = [
    [sg.Text('Самое свежее расписание ВятГУ!'),  sg.Combo(values=['ЛВб-3201','ЛВб-4201','ЛВб-4202','ПОДб-4203'], enable_events=True, key='-COMBO-', size=(30,6))],
    [sg.Output()],
    [sg.Button("Get the schedule!"), sg.Cancel()]
]
window = sg.Window('vyatsu schedule parser v0.1', layout)

idGroup = ''

while True:                             # The Event Loop
    event, values = window.read()
    print(event, values) #debug

    if event == '-COMBO-':
        if values['-COMBO-'] == "ЛВб-4202":
            idGroup = 'listPeriod_143851'
            print("id = 'listPeriod_143851'")
        if values['-COMBO-'] == "ЛВб-4201":
            idGroup = 'listPeriod_143841'
            print("id = 'listPeriod_143841'")
        if values['-COMBO-'] == "ПОДб-4203":
            idGroup = 'listPeriod_143831'
            print("id = 'listPeriod_143831'")
        if values['-COMBO-'] == "ЛВб-3201":
            idGroup = "listPeriod_144781"
            print("id = 'listPeriod_144781'")


    if event == 'Get the schedule!':
        if idGroup == '':
            sg.Popup("Choose group!")
        else:
            schGetter (idGroup)

    
    if event in ('', 'Exit', 'Cancel'):
        break
