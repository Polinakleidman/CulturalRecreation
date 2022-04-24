import pandas as pd


def get_information(row_number, data):
    answer = [data['ShortName'][row_number],
              data['ObjectAddress'][row_number][0]['Address'],
              data['WebSite'][row_number],
              'Часы работы:']
    working_hours = [data['WorkingHours'][0][i]['DayWeek'] + ' ' + data['WorkingHours'][0][i]['WorkHours'] for i in range(7)]
    answer = answer + working_hours
    return answer

