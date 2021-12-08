import json
import codecs
from datetime import datetime
import os

msg_att= []
authors = []

filename = os.path.join("touka_08dec2021", "messages_all.json")

data = json.load(codecs.open(filename, 'r', 'utf-8'))  # Pour avoir les caractères spéciaux

for message in data:
    for att in message.keys():
        if att not in msg_att:
            msg_att.append(att)
    
    if message['author'] not in authors:
        authors.append(message['author'])

print(msg_att)
print(authors)
# print(len(data['messages']))