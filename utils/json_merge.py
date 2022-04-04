import os
import json
import codecs

files = [os.path.join("touka_04avril2022", f"message_{i+1}.json") for i in range(24)]
all_data = []

for file in files:
    with open(file) as f:
        f_data = json.load(f)
        all_data.append(f_data['messages'])

all_data = [item for sublist in all_data for item in sublist]


with open(os.path.join("touka_04avril2022", "touka_04avril2022.json"), "w") as json_file:
    json.dump(all_data, json_file, indent=4, sort_keys=True)

