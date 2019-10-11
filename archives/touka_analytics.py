import json
import codecs
import datetime
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import numpy as np
from matplotlib import dates


def activite(temps, messages, dx=25):
    activite = [(messages[i + dx] - messages[i]) * 3600 / -(temps[i + dx] - temps[i]) for i in
                range(0, len(messages) - dx, dx)]
    temps = [temps[i] for i in range(0, len(messages) - dx, dx)]
    return temps, activite


def activite_interp(temps, messages, dx=3600):
    interp = interp1d(temps, messages)
    print("temps:", temps)
    x_new = np.arange(temps[0] - dx, temps[-1] + dx, -dx)
    print("x_new:", x_new)
    activite = [(interp(x - dx) - interp(x)) * 3600 * 24 / dx for x in x_new]  # Messages par jour
    print("activité:", activite)
    return x_new, activite


plt.style.use('seaborn-paper')

noms_touka = ['Jé Talbot', 'Roulo', 'Lakasse', 'Pierre-Poom', 'Krostif', 'Jirome', 'Vinssan', 'Godbout']

data = json.load(codecs.open('touka.json', 'r', 'utf-8'))  # Pour avoir les caractères spéciaux

map_touka = dict(zip([participant['name'] for participant in data['participants']], noms_touka))

comptes = [sum([message['sender_name'] == participant['name'] for message in data['messages']]) for participant in
           data['participants']]

timestamps_tout = [float(message['timestamp_ms'] / 1000) for message in data['messages']]

messages_participant = [[message for message in data['messages'] if message['sender_name'] == participant['name']] for
                        participant in
                        data['participants']]

nb_mess = [len(messages) for messages in messages_participant]
print(nb_mess)

# messages_participant: [[list de messages à jé talbot], [liste de message à roulo], ... ]

timestamps = [[float(message['timestamp_ms'] / 1000) for message in participant] for participant in
              messages_participant]  # [s]

nb_characters = []
nb_characters_total = []
for participant in messages_participant:
    s = 0
    s_total = []
    for message in participant:
        try:
            if message['content'][-17:] != "envoyé une photo.":
                s += len(message['content'])
        except:
            ValueError
        s_total.append(s)
    nb_characters.append(s_total)
    nb_characters_total.append(s)

ratio_char_msg = [char / msg for char, msg in zip(nb_characters_total, nb_mess)]

nb_messages = dict(zip([participant['name'] for participant in data['participants']], comptes))
toukas_name_sorted = sorted(nb_messages.items(), key=lambda kv: kv[1])
nb_messages = dict(sorted(nb_messages.items(), key=lambda kv: kv[1])[::-1])

nb_messages = dict((map_touka[key], value) for (key, value) in nb_messages.items())

plt.bar(nb_messages.keys(), nb_messages.values())
plt.xticks(rotation=45, ha='right', size=10)
plt.ylabel('Nombre de messages total')
plt.title('Nombre de messages total envoyés sur Touka')
plt.savefig('Figures/bar_nb_messages_total.png')
# plt.show()
plt.clf()

plt.bar(noms_touka, nb_characters_total)
plt.xticks(rotation=45, ha='right', size=10)
plt.ylabel('Nombre de caractères écrits total')
plt.title('Nombre de caractères total envoyés sur Touka selon les toukas')
plt.savefig('Figures/bar_nb_char_total.png')
# plt.show()
plt.clf()

plt.bar(noms_touka, ratio_char_msg)
plt.xticks(rotation=45, ha='right', size=10)
plt.ylabel('Ratio')
plt.title('Ratio du nombre de caractères écrits par message sur Touka selon les toukas')
plt.savefig('Figures/bar_ratio_char_msg.png')
# plt.show()
plt.clf()

for i in range((len(timestamps))):
    date_list = [datetime.datetime.fromtimestamp(t) for t in timestamps[i]]  # converted
    plt.plot(date_list, range(len(timestamps[i]))[::-1], label=noms_touka[i])

plt.gcf().autofmt_xdate()
plt.legend()
plt.ylabel('Nombre de messages')
plt.title('Nombre de messages total dans le temps par touka')
plt.savefig('Figures/nb_messages_dans_le_temps_par_touka.png')
# plt.show()
plt.clf()

for i in range((len(timestamps))):
    date_list = [datetime.datetime.fromtimestamp(t) for t in timestamps[i]]  # converted
    plt.plot(date_list, nb_characters[i][::-1], label=noms_touka[i])

plt.gcf().autofmt_xdate()
plt.legend()
plt.ylabel('Nombre de caractères')
plt.title('Nombre de caractères total dans le temps par touka')
plt.savefig('Figures/nb_caractères_dans_le_temps_par_touka.png')
# plt.show()
plt.clf()

for i in range((len(timestamps))):
    date_list = [datetime.datetime.fromtimestamp(t) for t in timestamps[i]]  # converted
    ratio = [char / msg for char, msg in zip(nb_characters[i][1:], range(1, len(timestamps[i])))]   # Pour éviter la division par 0
    plt.plot(date_list[101:], ratio[::-1][100:], label=noms_touka[i])   # À partir du 100e message

plt.gcf().autofmt_xdate()
plt.legend()
plt.ylabel('Nombre de messages')
plt.title('Ratio du nombre de caractères écrits par message sur Touka selon les toukas\nà partir du 100e message')
plt.savefig('Figures/ratio_char_msg_dans_le_temps_par_touka.png')
# plt.show()
plt.clf()

for i in range((len(timestamps))):
    temps, activite_ = activite_interp(timestamps[i], range(len(timestamps[i])),
                                       dx=3600 * 24 * 30)  # Moyenné sur 1 mois
    date_list = [datetime.datetime.fromtimestamp(t) for t in temps]  # converted
    plt.plot(date_list, activite_, label=noms_touka[i])

plt.gcf().autofmt_xdate()
plt.legend()
plt.ylabel('Activité [messages/jour]')
plt.title('Activité dans le temps par touka\nmoyenné sur un mois')
plt.savefig('Figures/activite_dans_le_temps_par_touka_sans_total.png')
# plt.show()
plt.clf()
