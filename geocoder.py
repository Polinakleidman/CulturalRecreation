import requests
import pandas as pd


def find_coordinates(adress):  # строка формата 'город Москва, улица Арбат, дом 55/32'
    list_adress = adress.split(', ')
    adress = '+'.join(list_adress)
    geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apike" \
                       f"y=40d1649f-0493-4b70-98ba-98533de7710b&geocode={adress}&format=json"
    response = requests.get(geocoder_request)
    json_response = response.json()
    return json_response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']


# как мы получили координаты, их в начальных таблицах не было
data = pd.read_json('data/food.json')
data = data[:500]
coord = []
# data = data[data['Address'].str.contains('улица')]
for i in range(len(data.index)):
    print(i)
    print(data['Address'][i])
    coord.append(find_coordinates(data['Address'][i]))
data['Coordinates'] = coord
data.to_json('data/food.json')
