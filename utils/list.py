import json
import codecs
from datetime import datetime
from mongoengine import connect, Document

msg_att= []
authors = []

data = json.load(codecs.open('touka.json', 'r', 'utf-8'))  # Pour avoir les caractères spéciaux

for message in data['messages']:
    for att in message.keys():
        if att not in msg_att:
            msg_att.append(att)
    
    if message['sender_name'] not in authors:
        authors.append(message['sender_name'])

print(msg_att)
print(authors)
print(len(data['messages']))