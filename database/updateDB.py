import json
import codecs
from datetime import datetime
from mongoengine import connect, Document
from utilsDB import Members, Messages

# Connect to DB
db = connect('ToukaAnalytics2')


data = json.load(codecs.open('touka.json', 'r', 'utf-8')
                 )  # Pour avoir les caractères spéciaux

for participant in data['participants']:
    if not(Members.objects(name=participant['name'])):
        Members(name=participant['name']).save()


max_timestamp = max(Messages.objects.distinct(field='timestamp')) # Message le plus recent
for message in data['messages']:
    if message['timestamp_ms'] < max_timestamp:
        data['messages'].remove(message)

i=1
t_0 = datetime.now()
for message in data['messages']:
    if not i%500:
        delta_t = datetime.now()-t_0
        progression = i / len(data['messages'])
        t_restant = delta_t * (1 / progression - 1)
        m, s = divmod(t_restant.total_seconds(), 60)
        h, m = divmod(m, 60)
        M, S = divmod(delta_t.total_seconds(), 60)
        H, M = divmod(M, 60)
        print('{0} / {1}'.format(i, len(data['messages'])))
        print('Progression: {0:.2%}, temps restant estimé: {1:.0f}h {2:02d}m {3:02d}s, temps écoulé: {4:.0f}h {5:02d}m {6:02d}s'.format(progression, h, int(m), int(s), H, int(M), int(S)))
    
    if not(Messages.objects(timestamp=message['timestamp_ms'])): # prendre selon max(timestamp)
        msg = Messages(author=message['sender_name'], timestamp=message['timestamp_ms'], date=datetime.fromtimestamp(int(
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
