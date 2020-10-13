import urllib3
from bs4 import BeautifulSoup
import os
import requests

html = "https://www.vyatsu.ru/studentu-1/spravochnaya-informatsiya/raspisanie-zanyatiy-dlya-studentov.html"
group = "143851"

http = urllib3.PoolManager()

response = http.request('GET',html)
soup = BeautifulSoup(response.data, 'html.parser')

div = soup.find('div', id='listPeriod_143851')
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
        print("У Вас последняя версия расписания!")
        print("Открываю расписание...")
        os.startfile("E:\new_schedule.pdf")
        result.close()
    else:
        print("Обновляю расписание...")
        result.close()
        f = open(r'E:\new_schedule.pdf',"wb")
        file_get = requests.get("https://www.vyatsu.ru" + clean_url)
        f.write(file_get.content)
        print("Открываю расписание...")
        os.startfile("E:\new_schedule.pdf")
        result = open(r'E:\download.txt', "w")
        result.write('clean_url')
        result.close
        f.close()

else:
    result = open(r"E:\download.txt", "w")
    result.write(clean_url)
    print("Обновляю расписание...")
    result.close()
    f = open(r'E:\new_schedule.pdf',"wb")
    file_get = requests.get("https://www.vyatsu.ru" + clean_url)
    f.write(file_get.content)
    print("Открываю расписание...")
    os.startfile("E:\new_schedule.pdf")
    result.close()
    f.close()


# print(os.getcwd())