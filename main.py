import pandas as pd
from information import get_information

museums = pd.read_json('data/museums.json')
print('\n'.join(get_information(5, museums)))