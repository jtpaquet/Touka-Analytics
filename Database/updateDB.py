import json
import codecs
from datetime import datetime
from mongoengine import connect, Document
from utilsDB import Members, Messages

# Connect to DB
db = connect('ToukaAnalytics')


data = json.load(codecs.open('touka.json', 'r', 'utf-8')
                 )  # Pour avoir les caractères spéciaux

for participant in data['participants']:
    Members(name=participant['name']).save()
i=1
for message in data['messages']:
    if not i%100:
        print(i)
    msg = Messages(author=message['sender_name'], date=datetime.fromtimestamp(int(
        message['timestamp_ms']/1000)), type=message['type'])
    
    if 'content' in message:
        msg['content'] = message['content']

    if 'share' in message:
        msg['share'] = message['share']

    if 'reactions' in message:
        msg['reactions'] = message['reactions']

    if 'files' in message:
        msg['file'] = message['files']

    if 'photos' in message:
        msg['photo'] = message['photos']

    if 'audio_files' in message:
        msg['audio_file'] = message['audio_files']

    msg.save()
    i+=1
