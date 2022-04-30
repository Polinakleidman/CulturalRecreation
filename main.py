import pandas as pd
from information import get_information, get_random_places, get_places_in_certain_area

museums = pd.read_json('data/museums.json')
answer = get_random_places(museums, 5)
for i in range(5):
    print('\n'.join(answer[i]))

# museums = pd.read_json('data/museums.json')
# answer = get_places_in_certain_area(museums, 'Юго-Восточный административный округ', 5)
# for i in range(5):
#     print('\n'.join(answer[i]))
