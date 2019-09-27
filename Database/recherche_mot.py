import json
import codecs
import datetime
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import numpy as np
from matplotlib import dates

plt.style.use('seaborn-paper')

noms_touka = ['Jé Talbot', 'Roulo', 'Lakasse', 'Pierre-Poom', 'Krostif', 'Jirome', 'Vinssan', 'Godbout']
pourcentages = ['35%', '60%', '75%', '90%', '93%', '96%', '99%', '100%']

data = json.load(codecs.open('touka.json', 'r', 'utf-8'))  # Pour avoir les caractères spéciaux

map_touka = dict(zip([participant['name'] for participant in data['participants']], noms_touka))

timestamps_tout = [float(message['timestamp_ms'] / 1000) for message in data['messages']]

messages_participants = [[message for message in data['messages'] if message['sender_name'] == participant['name']] for
                         participant in data['participants']]

timestamps = [[float(message['timestamp_ms'] / 1000) for message in participant] for participant in
              messages_participants]  # [s]

# messages_participants: [[list de messages à jé talbot], [liste de message à roulo], ... ]
# timestamps: [[timestamps à jé talbot], [timestamps à roulo], ... ]
# comptes_part_mot: [[0,0,0,0,1,0,0,0,2,0,0, ...], [liste d'occurence pour roulo], [...]]

recherche = input("Entrez le mot à rechercher: ")
# recherche = 'moua'

timestamps_part_mot = []
comptes_part_mot = []
timestamps_mot = []


# Retourne e nombre de fois que le mot est trouvé dans le message
def find_mot(mot, message):
    try:
        mot, message = mot.lower(), message.lower()
        return message.count(mot)
    except:
        ValueError
    return 0


for messages_participant in messages_participants:
    # for message_data in messages_participant:
    #     print(message_data.get('timestamp_ms'))
    stats_mot = [find_mot(recherche, message_data.get('content')) for message_data in messages_participant]

    comptes_part_mot.append(stats_mot)

for i in range(len(comptes_part_mot)):
    compte = []
    for j in range(len(comptes_part_mot[i])):
        compte.append(sum(comptes_part_mot[i][::-1][:j])) # À l'envers
    comptes_part_mot[i] = compte
    print('Opération complétée à {}'.format(pourcentages[i]))

for i in range((len(timestamps))):
    date_list = [datetime.datetime.fromtimestamp(t) for t in timestamps[i][::-1]]  # converted
    # print(date_list)
    # print(comptes_part_mot[i])
    plt.plot(date_list, comptes_part_mot[i], label=noms_touka[i])

plt.gcf().autofmt_xdate()
plt.yscale('linear')
plt.legend()
plt.ylabel('Nombre de mentions du mot {}'.format(recherche))
plt.title('Nombre de mentions du mot {} dans le temps par touka'.format(recherche))
plt.savefig('Mots/nb_mentions_{}_par_touka.png'.format(recherche))
plt.show()
plt.clf()
