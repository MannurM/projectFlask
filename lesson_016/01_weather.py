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
import requests
from html.parser import HTMLParser
from bs4 import BeautifulSoup

class WeatherMaker:
    """
     Создать модуль-движок с классом WeatherMaker, необходимым для получения и формирования предсказаний.
     В нём должен быть метод, получающий прогноз с выбранного вами сайта (парсинг + re) за некоторый диапазон дат,
     а затем, получив данные, сформировать их в словарь {погода: Облачная, температура: 10, дата:datetime...}
    """
    def __init__(self):
        pass

    def parsing_data(self):
        response = requests.get('https://www.gismeteo.ru/weather-chelno-vershiny-4580/')
        if response.status_code == 200:
            html_doc = BeautifulSoup(response.text, features='html.parser')
            list_of_values = html_doc.find_all('span', {'class': 'inline-stocks__value_inner'})
            list_of_names = html_doc.find_all('a', {'class': 'home-link home-link_black_yes inline-stocks__link'})

            for names, values in zip(list_of_names, list_of_values):
                print(names.text, values.text)

        # ! response = requests.get()

        # !!with open(filename, 'wb') as fd:
        #         for chunk in r.iter_content(chunk_size=128):
        #             fd.write(chunk)

        #

    def create_dict(self):
        pass

    class MyHTMLParser(HTMLParser):
        def handle_starttag(self, tag, attrs):
            print(f'Encountered a start tag: <{tag}>')

        def handle_endtag(self, tag):
            print(f'Encountered an end tag : </{tag}>')

        def handle_data(self, data):
            print(f'Encountered some data  : "{data}"')




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


if __name__ == '__main__':
    pass
