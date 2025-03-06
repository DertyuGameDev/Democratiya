import os
import random
import sys

import requests
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton

SCREEN_SIZE = [600, 600]


def check_responce(response):
    if not response:
        print("Ошибка выполнения запроса:")
        print("Http статус:", response.status_code, "(", response.reason, ")")
        os.remove('image.png')
        quit()


def get_coords(city):
    params_search = {
        "geocode": city,
        "format": "json",
        "apikey": '7baececd-be0e-4475-a6ae-f15bef0b9622'
    }
    link = 'http://geocode-maps.yandex.ru/1.x/'
    reponse = requests.get(link, params=params_search)
    check_responce(reponse)
    data = reponse.json()
    return ','.join(data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'].split())


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.map_file = "image.png"
        self.cities = ['Санкт-Петербург', 'Ярославль', 'Сочи', 'Калининград', 'Москва']
        self.first = True
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Угадай город или заплати 100 рублей')

        ## Изображение
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)

        self.label_info = QLabel(f'Города для загадывания: {", ".join(self.cities)}', self)
        self.label_info.move(85, 470)
        self.label_info.resize(600, 20)

        self.btn = QPushButton('загадать', self)
        self.btn.move(270, 530)
        self.btn.clicked.connect(self.click)

        self.lineedit = QLineEdit(self)
        self.lineedit.move(270, 500)

        self.label_error = QLabel(self)
        self.label_error.move(50, 560)
        self.label_error.resize(600, 20)

        self.current_loc = random.choice(self.cities)
        self.get_image(get_coords(self.current_loc))
        self.image.setPixmap(QPixmap(self.map_file))

    def click(self):
        self.label_error.setText("")
        if self.lineedit.text() not in self.cities:
            self.label_error.setText(f'"{self.lineedit.text()}" не найдено в списке город: {", ".join(self.cities)}')
        else:
            if self.lineedit.text() == self.current_loc:
                self.statusBar().showMessage('Угадал')
            else:
                self.statusBar().showMessage('Не угадал')
            self.current_loc = random.choice([i for i in self.cities if i != self.current_loc])
            self.get_image(get_coords(self.current_loc))
            self.lineedit.setText("")
            self.image.setPixmap(QPixmap(self.map_file))

    def get_image(self, coords):
        if self.first:
            val_l = 'sat'
            self.first = False
        else:
            val_l = random.choice(('map', 'sat'))
        print(1)
        link = 'http://static-maps.yandex.ru/v1'
        apikey = "ef67d706-4387-4517-8b08-50f4c0929dd7"
        search_params = {
            'apikey': apikey,
            'll': coords,
            'spn': '0.02,0.002',
        }
        response = requests.get(link, params=search_params)
        check_responce(response)
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
