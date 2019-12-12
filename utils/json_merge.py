import os
import json

files = [os.path.join("touka 10dec2019", "message_{}.json".format(i+1)) for i in range(17)]
all_data = []

for file in files:
    with open(file) as f:
        f_data = json.load(f)
        all_data.append(f_data['messages'])

all_data = [item for sublist in all_data for item in sublist]

with open('touka_10dec2019.json', 'w') as f:
    json.dump(all_data, f)