from utilities import *
import random

data = read_data('duz-hat/ornek-veri.xlsx')
data = data[data['is_elemani'] != 'a']

for row in data['onculler']:
    if 'b' in row:
        row.remove('b')

print(data)