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
    
def taxi(coordinatesX_1, coodinatesY_1, coordinatesX_2, coordinatesY_2, clas):

    url = ' https://taxi-routeinfo.taxi.yandex.net/taxi_info'

    parameters = {
        "clid": None, # мой код
        "apikey": None, # мой код
        "rll": str(coordinatesX_1) + ',' + str(coodinatesY_1) + '~' + str(coordinatesX_2) + ',' + str(coordinatesY_2),
        "class": clas, # econom — «Эконом». business — «Комфорт». comfortplus — «Комфорт+». minivan — «Минивен». vip — «Бизнес».
        "lang": "ru"
    }

    response = requests.get(url, parameters).json()
    json_response = response.json()
    
    return json_response

def taxi_zaglushka(coordinatesX_1, coodinatesY_1, coordinatesX_2, coordinatesY_2, clas):
    return {
        "currency": "RUB",
        "distance": 61529.771101536542,
        "options": [
            {
                "class_level": 50,
                "class_name": "econom",
                "class_text": "Эконом",
                "min_price": 495,
                "price": 10945,
                "price_text": "10945 руб.",
                "waiting_time": 203.98798614740372
            }
        ],
        "time": 3816.9397069215775
    }
