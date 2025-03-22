import math
import sys
from io import BytesIO
import requests
from PIL import Image
from module import spn1


def lonlat_distance(a, b):
    degree_to_meters_factor = 111 * 1000  # 111 километров в метрах
    a_lon, a_lat = a
    b_lon, b_lat = b

    # Берем среднюю по широте точку и считаем коэффициент для нее.
    radians_lattitude = math.radians((a_lat + b_lat) / 2.0)
    lat_lon_factor = math.cos(radians_lattitude)

    # Вычисляем смещения в метрах по вертикали и горизонтали.
    dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
    dy = abs(a_lat - b_lat) * degree_to_meters_factor

    # Вычисляем расстояние между точками.
    distance = math.sqrt(dx * dx + dy * dy)

    return distance


# Пусть наше приложение предполагает запуск:
# python search.py Москва, ул. Ак. Королева, 12
toponym_to_find = " ".join(sys.argv[1:])

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

geocoder_params = {
    "apikey": "7baececd-be0e-4475-a6ae-f15bef0b9622",
    "geocode": toponym_to_find,
    "format": "json"
}

response = requests.get(geocoder_api_server, params=geocoder_params)

if not response:
    pass

json_response = response.json()
toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
toponym_coodrinates = toponym["Point"]["pos"]
toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

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
    pass

json_response1 = response.json()

organization = json_response1["features"][:10]

min_lon = min(org["geometry"]["coordinates"][0] for org in organization)
max_lon = max(org["geometry"]["coordinates"][0] for org in organization)
min_lat = min(org["geometry"]["coordinates"][1] for org in organization)
max_lat = max(org["geometry"]["coordinates"][1] for org in organization)

spn_lon = abs(max_lon - min_lon)
spn_lat = abs(max_lat - min_lat)

org_points = list(map(lambda x: (f"{x[0][0]},{x[0][1]}", x[1]),
                      [(i["geometry"]["coordinates"], i["properties"]["CompanyMetaData"]['Hours']['text'])
                       for i in organization]))


def metki(org_points):
    t = []
    for i in org_points:
        if 'круглосуточно' in i[1]:
            t.append(f'{i[0]},pm2gnl')
        elif 'некруглосуточно' in i[1]:
            t.append(f'{i[0]},pm2bll')
        else:
            t.append(f'{i[0]},pm2wtl')
    return '~'.join(t)


map_params = {
    "ll": ",".join([toponym_longitude, toponym_lattitude]),
    "spn": f"{spn_lon},{spn_lat}",
    "apikey": "ef67d706-4387-4517-8b08-50f4c0929dd7",
    "pt": metki(org_points)
}

map_api_server = "https://static-maps.yandex.ru/v1"

response = requests.get(map_api_server, params=map_params)
im = BytesIO(response.content)
opened_image = Image.open(im)
opened_image.show()
