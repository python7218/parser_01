import requests  #Отвечает за взаимодействие с сервером
from bs4 import BeautifulSoup # Отвечает за обработку html текста и извлекает данные
import csv  #

URL = 'https://yellowpages.akipress.org/cats:316/'#это адрес сайта которую мы хотим извлечь

def get_html(url): #функция обращения к серверу
    response = requests.get(url)#ответ от сервера
    return response #возврашаем ответ от сервера туда где вызывается функция

def get_content(html): # Функция для извлечения данных контента сайта
    soup = BeautifulSoup(html,'html.parser')#получает текст для обработки
    items = soup.find_all('div', class_='main-info')#находит все теги div с названием class main-info 

    blocks = []#пустой список которую мы будем заполнять данными
    for item in items: #извлечение всех объявление по одному каждый раз
        name = (item.find('span',class_='name').get_text())#выводит заголовок объявления 
        phone = (item.find('li', class_='phone').get_text())#выводит информацию о  тел компании 
        full_info = item.find_all('li', class_='phone')#записиваем  тел и email
        if len(full_info) > 1:#создаем условие где оба есть то мы выводим email а номер оставляем 
            email = full_info[-1].get_text().split(':')[-1].strip()#извлекаем только email без мусора
            
        else:
            email = ''#если нет email остается только номер тел
            
        address = item.find('ul',class_='address').get_text(strip=True).split('г. ')[-1]#выводем адрес компании
        
        temp_dict = {'name': name, 'phone': phone, 'email': email, 'address': address}#записываем во врем словарь temp_dict
        
        blocks.append(temp_dict)#наполняет блок содержимым временного словаря temp_dict

    return blocks#возвращает список со всеми данными со страницы

def save_file(blocks):#функция сохранения файла с входным параметром ввиде списка с данными 
    with open('yellowpages.csv', 'w', newline='') as file:#контекстный менеджер для создания файла сsv
        writer = csv.writer(file, delimiter=';')#вызов для записи данных в сsv файл
        writer.writerow(['Название','Телефон','E-mail','Адрес'])#записываем первую страку-название столбцов

        for block in blocks:#перебираем в цикле все данные
            writer.writerow([block['name'], block['phone'], block['email'], block['address']])#записываем построчно даные

def main(): #главная функция которая запускает остальные функции
    html = get_html(URL)#вызываем get_html 
    #print(html.text)
    if html.status_code == 200:#Проверка статуса http:
        #print('ok')
        blocks = get_content(html.text)#возвращает список blocks 
        save_file(blocks)#сохраняет файлы в blocks
    else:
        print('Проблемы с ответом от сервера!')#пичатает ответ сервера если не удовлетворительный
        
main() # вызов главной функции

