import pandas as pd
import random as rd


def get_information(row_number, data):  # get information about certain place
    answer = [data['CommonName'][row_number],
              data['ObjectAddress'][row_number][0]['Address'],
              data['WebSite'][row_number],
              'Часы работы:']
    working_hours = [
        data['WorkingHours'][row_number][i]['DayWeek'] + ' ' + data['WorkingHours'][row_number][i]['WorkHours'] for i in
        range(7)]
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
        return ['Мы не поняли запрос, поэтому подобрали вам рандомное место:\n'] + get_information(rd.randint(0, len(temp_data.index) - 1), data)
    if len(temp_data.index > 0):
        ind = temp_data.index[0]
        return [get_information(ind, data)]
    else:
        return ['Место не найдено :(']


def get_places_in_certain_area(main_data, area_name, number):  # returns numbers of random places in certain area
    data_with_areas = main_data
    data_with_areas['Area'] = [main_data['ObjectAddress'][i][0]['AdmArea'] for i in range(len(main_data.index))]
    data = pd.DataFrame(data_with_areas[data_with_areas['Area'] == area_name])  #
    number_of_places = min(number, len(data.index))
    answer = [0] * number_of_places
    for i in range(number_of_places):
        place = rd.randint(0, len(data.index) - 1)
        while place in answer:
            place = rd.randint(0, len(data.index) - 1)
        answer[i] = place
    return [get_information(answer[i], data) for i in range(number_of_places)]
