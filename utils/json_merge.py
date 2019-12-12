import os
import json

def parse_obj(obj):
    for key in obj:
        if isinstance(obj[key], str):
            obj[key] = obj[key].encode('latin_1').decode('utf-8')
        elif isinstance(obj[key], list):
            obj[key] = list(map(lambda x: x if type(x) != str else x.encode('latin_1').decode('utf-8'), obj[key]))
        pass
    return obj

files = [os.path.join("utils", "touka 10dec2019", "message_{}.json".format(i+1)) for i in range(17)]
all_data = []

for file in files:
    with open(file) as f:
        f_data = json.load(f)
        all_data.append(f_data['messages'])

all_data = [item for sublist in all_data for item in sublist]


with open(os.path.join("utils", "touka_10dec2019.json"), "w") as json_file:
    # json.dump(all_data, f, indent=4, sort_keys=True, ensure_ascii=False)
    json_string = json.dumps(all_data, ensure_ascii=False).encode('utf8').decode('utf8')
    json.dump(json_string, json_file, ensure_ascii=False)

