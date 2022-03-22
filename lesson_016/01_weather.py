# -*- coding: utf-8 -*-

# В очередной спешке, проверив приложение с прогнозом погоды, вы выбежали
# навстречу ревью вашего кода, которое ожидало вас в офисе.
# И тут же день стал хуже - вместо обещанной облачности вас встретил ливень.

# Вы промокли, настроение было испорчено, и на ревью вы уже пришли не в духе.
# В итоге такого сокрушительного дня вы решили написать свою программу для прогноза погоды
# из источника, которому вы доверяете.

# Для этого вам нужно:

# Создать модуль-движок с классом WeatherMaker, необходимым для получения и формирования предсказаний.
# В нём должен быть метод, получающий прогноз с выбранного вами сайта (парсинг + re) за некоторый диапазон дат,
# а затем, получив данные, сформировать их в словарь {погода: Облачная, температура: 10, дата:datetime...}

# Добавить класс ImageMaker.
# Снабдить его методом рисования открытки
# (использовать OpenCV, в качестве заготовки брать lesson_016/python_snippets/external_data/probe.jpg):
#   С текстом, состоящим из полученных данных (пригодится cv2.putText)
#   С изображением, соответствующим типу погоды
# (хранятся в lesson_016/python_snippets/external_data/weather_img ,но можно нарисовать/добавить свои)
#   В качестве фона добавить градиент цвета, отражающего тип погоды
# Солнечно - от желтого к белому
# Дождь - от синего к белому
# Снег - от голубого к белому
# Облачно - от серого к белому

# Добавить класс DatabaseUpdater с методами:
#   Получающим данные из базы данных за указанный диапазон дат.
#   Сохраняющим прогнозы в базу данных (использовать peewee)

# Сделать программу с консольным интерфейсом, постаравшись все выполняемые действия вынести в отдельные функции.
# Среди действий, доступных пользователю, должны быть:
#   Добавление прогнозов за диапазон дат в базу данных
#   Получение прогнозов за диапазон дат из базы
#   Создание открыток из полученных прогнозов
#   Выведение полученных прогнозов на консоль
# При старте консольная утилита должна загружать прогнозы за прошедшую неделю.

# Рекомендации:
# Можно создать отдельный модуль для инициализирования базы данных.
# Как далее использовать эту базу данных в движке:
# Передавать DatabaseUpdater url-путь
# https://peewee.readthedocs.io/en/latest/peewee/playhouse.html#db-url
# Приконнектится по полученному url-пути к базе данных
# Инициализировать её через DatabaseProxy()
# https://peewee.readthedocs.io/en/latest/peewee/database.html#dynamically-defining-a-database

import requests, re

from bs4 import BeautifulSoup

class WeatherMaker:
    """
     Создать модуль-движок с классом WeatherMaker, необходимым для получения и формирования предсказаний.
     В нём должен быть метод, получающий прогноз с выбранного вами сайта (парсинг + re) за некоторый диапазон дат,
     а затем, получив данные, сформировать их в словарь {погода: Облачная, температура: 10, дата:datetime...}
    """
    def __init__(self):
        self.response = None
        self.src = None
        self.file_name = None

    def parsing_data(self):
        url = 'https://darksky.net/forecast/54.4123,51.0794/si12/en'
        headers = {
            'Accept' : '*/*',
            'User-Agent': ''
        }
        self.response = requests.get(url, headers=headers)
        self.src = self.response.text
        return self.src


    def save_page(self, src): # Сохранение спарсенной страницы в файл
        self.src = src
        self.file_name = 'index.html'
        with open(self.file_name, 'w', encoding='utf-8') as file:
            file.write(self.src)
        return self.file_name


    def open_page(self, file_name):  # открыть файл html
        self.file_name = file_name
        file_name = 'index.html'
        with open(file_name, encoding='utf-8') as file:
            self.response = file.read()

        html_doc = BeautifulSoup(self.response, "html5lib")
        # Облачность, Осадки, мм
        list_val_precipitation = html_doc.find_all('div', class_="dayDetails")
        list_prec, list_count, list_cloud = [], [], []
        for item in list_val_precipitation:
            val_precipitation = item.find('span', class_="label swip")
            val_count_prec = item.find('span', class_="num swip")
            val_cloud_status = item.find('div', class_='summary')
            list_prec.append(val_precipitation)
            list_count.append(val_count_prec)
            list_cloud.append(val_cloud_status)
        # Дни, диапазон температур
        list_temp = html_doc.find_all('a', class_="day")
        dict_data_temp = {}
        for number, item in enumerate(list_temp):
            dict_day_temp = {}
            val_low = item.find('span', class_='minTemp')
            val_high = item.find('span', class_='maxTemp')
            val_range = (val_low.text, val_high.text)
            # re - использовать для отделения лишних знаков
            val_name_day = item.find('span', class_='name')
            val_name_day = val_name_day.text
            val = re.sub("[^A-Za-z]", "", val_name_day)
            val_name_day = val
            # Создание словаря с данными погоды за 8 дней
            gen_temp_prec, gen_temp_count, gen_temp_cloud = list_prec[number], list_count[number], list_cloud[number]
            dict_day_temp['Облачность'] = gen_temp_cloud.text
            dict_day_temp['Температура'] = val_range
            dict_day_temp['Осадки'] = (gen_temp_prec.text, gen_temp_count.text)
            dict_data_temp[val_name_day] = dict_day_temp  # или лучше список словарей??
        return dict_data_temp


class ImageMaker:
    """
    Добавить класс ImageMaker.
    Снабдить его методом рисования открытки
    (использовать OpenCV, в качестве заготовки брать lesson_016/python_snippets/external_data/probe.jpg):
      С текстом, состоящим из полученных данных (пригодится cv2.putText)
      С изображением, соответствующим типу погоды
    (хранятся в lesson_016/python_snippets/external_data/weather_img ,но можно нарисовать/добавить свои)
      В качестве фона добавить градиент цвета, отражающего тип погоды
    Солнечно - от желтого к белому
    Дождь - от синего к белому
    Снег - от голубого к белому
    Облачно - от серого к белому
    """
    def __init__(self):
        pass

    def create_image(self):
        pass


class DatabaseUpdater:
    """
    Добавить класс DatabaseUpdater с методами:
    Получающим данные из базы данных за указанный диапазон дат.
    Сохраняющим прогнозы в базу данных (использовать peewee)
    """
    def __init__(self):
        pass

    def read_database(self):
        pass

    def add_database(self):
        pass

    def save_database(self):
        pass


class ConsolInterface:
    """
    Сделать программу с консольным интерфейсом, постаравшись все выполняемые действия вынести в отдельные функции.
    Среди действий, доступных пользователю, должны быть:
      Добавление прогнозов за диапазон дат в базу данных
      Получение прогнозов за диапазон дат из базы
      Создание открыток из полученных прогнозов
      Выведение полученных прогнозов на консоль
    При старте консольная утилита должна загружать прогнозы за прошедшую неделю.
    """
    def __init__(self):
        pass

    def range_selection(self):
        pass

    def create_forecasts(self):
        pass

    def create_images(self):
        pass

    def print_console(self):
        pass


dict_weather = {}

def main():
    wm = WeatherMaker()
    src = wm.parsing_data()
    file_name = wm.save_page(src)
    dict_weather = wm.open_page(file_name)
    print(dict_weather)


if __name__ == '__main__':
   main()
