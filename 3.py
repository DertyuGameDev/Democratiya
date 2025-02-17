import math
import sys
from io import BytesIO  # Этот класс поможет нам сделать картинку из потока байт
import requests
from PIL import Image


def lonlat_distance(a, b):
    degree_to_meters_factor = 111 * 1000  # 111 километров в метрах
    a_lon, a_lat = a
    b_lon, b_lat = b

    # Берем среднюю по широте точку и считаем коэффициент для нее.
    radians_lattitude = math.radians((a_lat + b_lat) / 2.)
    lat_lon_factor = math.cos(radians_lattitude)

    # Вычисляем смещения в метрах по вертикали и горизонтали.
    dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
    dy = abs(a_lat - b_lat) * degree_to_meters_factor

    # Вычисляем расстояние между точками.
    distance = math.sqrt(dx * dx + dy * dy)

    return distance


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

search_api_server1 = "https://search-maps.yandex.ru/v1/"
api_key1 = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"

address_ll = ",".join([toponym_longitude, toponym_lattitude])

search_params = {
    "apikey": api_key1,
    "text": "аптека",
    "lang": "ru_RU",
    "ll": address_ll,
    "type": "biz"
}

response = requests.get(search_api_server1, params=search_params)
if not response:
    # ...
    pass

json_response1 = response.json()
# Получаем первую найденную организацию.
organization = json_response1["features"][0]
# Название организации.
org_name = organization["properties"]["CompanyMetaData"]["name"]
# Адрес организации.
org_address = organization["properties"]["CompanyMetaData"]["address"]

# Получаем координаты ответа.
point = organization["geometry"]["coordinates"]
point1 = list(map(float, org_point.split(',')))
sp = f'{abs(point[0] - point1[0]) * 2},{abs(point[1] - point1[1]) * 2}'
org_point2 = f"{point[0]},{point[1]}"

apikey = "ef67d706-4387-4517-8b08-50f4c0929dd7"
# Собираем параметры для запроса к StaticMapsAPI:
map_params = {
    "ll": ",".join([toponym_longitude, toponym_lattitude]),
    "spn": sp,
    "apikey": apikey,
    "pt": f"{org_point2},pm2dgl~{org_point},pm2dbl"
}

map_api_server = "https://static-maps.yandex.ru/v1"
# ... и выполняем запрос
print(org_name)
print(org_address)
print(organization["properties"]["CompanyMetaData"]['Hours']['text'])
print(lonlat_distance(map(float, org_point.split(',')), map(float, org_point2.split(','))))

response = requests.get(map_api_server, params=map_params)
im = BytesIO(response.content)
opened_image = Image.open(im)
opened_image.show()  # Создадим картинку и тут же ее покажем встроенным просмотрщиком операционной системы
