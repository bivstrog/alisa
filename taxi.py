import requests

def take_coor(address):
    response = None
    geocoder_request = 'http://geocode-maps.yandex.ru/1.x/?geocode=' + address + '&format=json'
    response = requests.get(geocoder_request)
    if response:
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
        toponym_coodrinates = toponym["Point"]["pos"].split()
        return toponym_address, toponym_coodrinates
    else:
        return False, False
