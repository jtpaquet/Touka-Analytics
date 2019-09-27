import json
import codecs
from datetime import datetime
from mongoengine import connect, Document

list= []

data = json.load(codecs.open('touka.json', 'r', 'utf-8')
                 )  # Pour avoir les caractères spéciaux

for message in data['messages']:
    for att in message.keys():
        if att not in list:
            list.append(att)

print(list)
print(len(data['messages']))