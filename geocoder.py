import requests

def find_coordinates(adress): # строка формата 'город Москва, улица Арбат, дом 55/32'
    list_adress = adress.split(', ')
    list_adress[0] = list_adress[0][6:]
    list_adress[1] = list_adress[1][6:]
    list_adress[2] = list_adress[2][4:]
    adress = '+'.join(list_adress)
    geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={adress}&format=json"
    response = requests.get(geocoder_request)
    json_response = response.json()
    print(json_response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'])


find_coordinates('город Москва, улица Арбат, дом 55/32')