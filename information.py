import pandas as pd
import random as rd

CITY_X = 37.617734
CITY_Y = 55.752004


def get_information(row_number, data):  # get information about certain place
    answer = [data['CommonName'][row_number],
              data['Address'][row_number],
              data['WebSite'][row_number]]
    if 'WorkingHours' in data.columns:
        working_hours = ['Часы работы']
        working_hours += [data['WorkingHours'][row_number][i]['DayWeek']
                          + ' ' + data['WorkingHours'][row_number][i]['WorkHours'] for i in range(7)]
        answer = answer + working_hours

    if 'ClarificationOfWorkingHours' in data.columns and str(data['ClarificationOfWorkingHours'][row_number]) != 'nan':
        answer.append(data['ClarificationOfWorkingHours'][row_number])
    answer = list(map(str, filter(lambda x: x != 'nan', answer)))
    return answer


def get_random_places(data, number=1):  # returns information about random places
    number_of_places = min(number, len(data.index) - 1)
    answer = [0] * number_of_places
    for i in range(number_of_places):
        place = rd.randint(0, len(data.index) - 1)
        while place in answer:
            place = rd.randint(0, len(data.index) - 1)
        answer[i] = place
    return [get_information(answer[i], data) for i in range(number_of_places)]


def get_information_about_certain_place(data, name):
    temp_data = data
    flag = False
    temp_data['Name'] = temp_data['CommonName'].str.lower()
    for name1 in list(filter(lambda x: (x.isalpha() and len(x) > 2) or x.isdigit(), name.lower().split())):
        flag = True
        temp_data = temp_data[temp_data['Name'].str.contains(name1)]
    if not flag:
        return [['Мы не поняли запрос, поэтому подобрали вам рандомное место:\n']] + [
            get_information(rd.randint(0, len(temp_data.index) - 1), data)]
    if len(temp_data.index) > 0:
        ind = temp_data.index[0]
        return [get_information(ind, data)]
    else:
        return [['Место не найдено :(']]


def get_random_in_district(data, area_name, number=1):  # returns numbers of random places in certain area
    temp_data = data
    areas = list(set(temp_data['Area']))
    name = area_name.lower()
    answer = None
    for i in range(len(areas)):
        if len(area_name) > 4 and area_name in areas[i]:
            answer = areas[i]
            break
        is_same = 0
        for j in range(min(len(areas[i]), len(name))):
            is_same += areas[i][j] == name[j]
        if (is_same / len(areas[i])) > 0.8:
            answer = areas[i]
            break
    if answer is None:
        return [['Место не найдено :(']]
    index_list = temp_data[temp_data['Area'] == answer].index
    if number > len(index_list):
        number = len(index_list)
        return [['В этом округе не так много мест, поэтому вот они слева направо:\n']] + \
               [get_information(index_list[i], data) for i in range(len(index_list))]
    answer = [0] * number
    for i in range(number):
        place = rd.randint(0, len(index_list) - 1)
        while place in answer:
            place = rd.randint(0, len(index_list) - 1)
        answer[i] = index_list[place]
    return [get_information(answer[i], data) for i in range(number)]


def get_km_from_city_center(data, max_dist, number=1):
    temp_data = data
    dist = []
    for i in range(len(data.index)):
        dist.append((((float(data['Coordinates'][i].split()[0]) - CITY_X) ** 2
                      + (float(data['Coordinates'][i].split()[1]) - CITY_Y) ** 2) ** 0.5) * 111.1 / 1.5)
    temp_data['Dist'] = dist
    index_list = temp_data[temp_data['Dist'] < max_dist].index
    if number > len(index_list):
        number = len(index_list)
        return [['В этом округе не так много мест, поэтому вот они слева направо:\n']] + \
               [get_information(index_list[i], data) for i in range(len(index_list))]
    answer = [0] * number
    for i in range(number):
        place = rd.randint(0, len(index_list) - 1)
        while place in answer:
            place = rd.randint(0, len(index_list) - 1)
        answer[i] = index_list[place]
    print(temp_data['Dist'][answer[0]])
    return [get_information(answer[i], data) for i in range(number)]
