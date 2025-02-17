import sys
from io import BytesIO  # Этот класс поможет нам сделать картинку из потока байт
import requests
from PIL import Image


def spn1(json_response):
    low = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]['boundedBy']['Envelope'][
        'lowerCorner']
    high = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]['boundedBy']['Envelope'][
        'upperCorner']
    ll1 = list(map(float, low.split()))
    ll2 = list(map(float, high.split()))
    spn = ','.join(map(str, (abs(ll1[0] - ll2[0]), abs(ll1[1] - ll2[1]))))
    return spn


# Пусть наше приложение предполагает запуск:
# python search.py Москва, ул. Ак. Королева, 12
# Тогда запрос к геокодеру формируется следующим образом:
toponym_to_find = " ".join(sys.argv[1:])

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

geocoder_params = {
    "apikey": "8013b162-6b42-4997-9691-77b7074026e0",
    "geocode": toponym_to_find,
    "format": "json"}

response = requests.get(geocoder_api_server, params=geocoder_params)

if not response:
    # обработка ошибочной ситуации
    pass

# Преобразуем ответ в json-объект
json_response = response.json()
# Получаем первый топоним из ответа геокодера.
toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
# Координаты центра топонима:
toponym_coodrinates = toponym["Point"]["pos"]
# Долгота и широта:
toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
org_point = ','.join(
    json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]['Point']['pos'].split())
apikey = "ef67d706-4387-4517-8b08-50f4c0929dd7"
# Собираем параметры для запроса к StaticMapsAPI:
map_params = {
    "ll": ",".join([toponym_longitude, toponym_lattitude]),
    "spn": spn1(json_response),
    "apikey": apikey,
    "pt": f"{org_point},pm2dbl"
}

map_api_server = "https://static-maps.yandex.ru/v1"
# ... и выполняем запрос
response = requests.get(map_api_server, params=map_params)
im = BytesIO(response.content)
opened_image = Image.open(im)
opened_image.show()  # Создадим картинку и тут же ее покажем встроенным просмотрщиком операционной системы
