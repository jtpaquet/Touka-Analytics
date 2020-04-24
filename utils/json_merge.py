import os
import json
import codecs

files = [os.path.join("utils", "touka_23avril", "message_{}.json".format(i+1)) for i in range(19)]
all_data = []

for file in files:
    with open(file) as f:
        f_data = json.load(f)
        all_data.append(f_data['messages'])

all_data = [item for sublist in all_data for item in sublist]


with open(os.path.join("utils", "touka_23avril2020.json"), "w") as json_file:
    json.dump(all_data, json_file, indent=4, sort_keys=True)

