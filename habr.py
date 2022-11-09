import datetime
import requests
from bs4 import BeautifulSoup
import csv
import time
from memory_profiler import memory_usage




CSV = 'fl_result.csv'
HOST = 'https://freelance.habr.com'
URL = 'https://freelance.habr.com/tasks?categories='
HEADERS = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9' ,
    'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Mobile Safari/537.36'
}

# Запрос на сайт и вход на сайт (без регистрации)
def get_html(url, params=''):
    r = requests.get(url, headers= HEADERS, params=params)
    return r 


# Получение контента с сайта 
def get_fl(html):
    soup = BeautifulSoup( html.text , 'html.parser') 
    fl_res = soup.find_all('li', class_= 'content-list__item')
    orders = []
    for ord in fl_res[:5]:
            orders.append(
                {
                    'order_name': ord.find ('div', class_= 'task__title').get_text(),
                    'order_price': ord.find ('div', class_= "task__price").get_text(),
                    # может быть "договорная цена"
                    'task_response': ord.find (class_='task__params params').get_text(),
                    # может не быть откликов
                    'link':HOST + ord.find ('div', class_= 'task__title').find('a').get('href'),
                    #'description': ' '
                }
            )
            # Можно раскоментировать если нужно, но для ускорения работы оставим так 
            # html_2 =  get_html( url= orders[len(orders)-1]["link"])
            # soup_2 = BeautifulSoup( html_2.text , 'html.parser') 
            # orders[len(orders)-1]['description']  = soup_2.find('div', class_= 'task__description' ).get_text().replace('\n\n', '\n')
    return orders

def save_doc(orders, path):
    with open (path,"w",newline="", encoding="utf-8" ) as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(['Название заказа', "Цена", "Сколько откликов", "Ссылка", "Описание"])
        for item in orders:
            writer.writerow([item['order_name'] ,item['order_price'] , item['task_response'] , item["link"] , item["description"]])


# выбор категории
def categorize (categories):
    urli= URL + categories
    html = get_html(url=urli)
    if html.status_code == 200:
        try: 
            result= []
            result.extend(get_fl(html))
            #save_doc(orders=result, path= CSV)
            return result 
            
        except Exception as e: 
            print ('Есть проблемы!', e)
    else:
        print ("Не могу найти такую категорию") 


def page_scrolling ():
    pagenation = input(' Сколько страниц? ').strip()
    pagenation = int (pagenation)
    html=  get_html (url=URL, params=f'{pagenation}')

    if html.status_code == 200:
        try:
            result= []
            for page in range (1, pagenation+1):
                print (f"Парсим странцу {page}")
                result.extend (get_fl( html ))
            save_doc(orders=result ,path=CSV )
        except Exception as ex :
            print ("Есть проблемы с поиском!")
            print (ex)

    else: 
        print (" Не получилось зайти на сайт!) ")



# start_time = time.time()
#print(categorize('development_bots'), len(categorize('development_bots')))
# print(memory_usage())
# print("--- %s seconds ---" % (time.time() - start_time))


