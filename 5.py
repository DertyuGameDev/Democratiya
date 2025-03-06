import sys
import requests

toponym_to_find = " ".join(sys.argv[1:])

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

geocoder_params = {
    "apikey": "7baececd-be0e-4475-a6ae-f15bef0b9622",
    "geocode": toponym_to_find,
    "format": "json"}

response = requests.get(geocoder_api_server, params=geocoder_params)

if not response:
    pass

json_response = response.json()
toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
toponym_coodrinates = toponym["Point"]["pos"]
geocoder_params = {
    "apikey": "7baececd-be0e-4475-a6ae-f15bef0b9622",
    "geocode": toponym_coodrinates,
    "format": "json"}

response = requests.get(geocoder_api_server, params=geocoder_params)
json_response = response.json()
a = json_response["response"]["GeoObjectCollection"]["featureMember"][2]["GeoObject"]

print(a['metaDataProperty']['GeocoderMetaData']['Address']['Components'][5]['name'])
