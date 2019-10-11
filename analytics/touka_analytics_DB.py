import datetime
import pandas as pd
from pymongo import MongoClient
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d


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

client = MongoClient("localhost", 27017)
db = client['ToukaAnalytics']

members = db['members']
messages = db['messages']

data = []

for member in members.find({}):
    name = member['name']
    # messages.aggregate( [ { "$project" : { 'content' : 1 , 'date' : 1 } } ] )
    query_txt = {'$and': [ {'author': name}, {'content': {'$exists': True, '$ne': None } } ] }
    query_react = {'$and': [ {'author': name}, {'reaction': {'$exists': True, '$ne': None } } ] }

    member_messages = { msg['date'] : msg['content'] for msg in messages.find(query_txt) }
    member_types = [ msg['type'] for msg in messages.find() ]
    member_reacts = [ msg['reaction'] for msg in messages.find(query_react) ]
    n_msg = messages.find(query_txt).count()

    data.append( {'Name': member['pseudo'], 'txt_msg': member_messages, 'Type': member_types, 'Reaction' : member_reacts, 'msg_count' : n_msg} )

df = pd.DataFrame(data, columns=('Name', 'txt_msg', 'Type', 'Reaction', 'msg_count'))
df = df.set_index('Name')

nb_characters = []
nb_characters_total = []
for member in df.index:
    s = 0
    s_total = []
    for msg in df.loc[member, 'txt_msg'].values():
        s += len(msg)
        s_total.append(s)
    nb_characters.append(s_total)
    nb_characters_total.append(s)

df['n_char'] = nb_characters
df['n_char_total'] = nb_characters_total

df['ratio_char_msg'] = df['n_char_total'] / df['msg_count']

plt.bar(df.index, df['msg_count'])
plt.xticks(rotation=45, ha='right', size=10)
plt.ylabel('Nombre de messages total')
plt.title('Nombre de messages total envoyés sur Touka')
plt.savefig('../figures/bar_nb_messages_total.png')
plt.show()
plt.clf()

plt.bar(df.index, df['n_char_total'])
plt.xticks(rotation=45, ha='right', size=10)
plt.ylabel('Nombre de caractères écrits total')
plt.title('Nombre de caractères total envoyés sur Touka selon les toukas')
plt.savefig('../figures/bar_nb_char_total.png')
plt.show()
plt.clf()

plt.bar(df.index, df['ratio_char_msg'])
plt.xticks(rotation=45, ha='right', size=10)
plt.ylabel('Ratio')
plt.title('Ratio du nombre de caractères écrits par message sur Touka selon les toukas')
plt.savefig('../figures/bar_ratio_char_msg.png')
plt.show()
plt.clf()

for name in df.index:
    member_messages = df.loc[name, 'txt_msg']
    plt.plot(member_messages.keys(), range(len(member_messages.keys()))[::-1], label=name)

plt.gcf().autofmt_xdate()
plt.legend()
plt.ylabel('Nombre de messages')
plt.title('Nombre de messages total dans le temps par touka')
plt.savefig('../figures/nb_messages_dans_le_temps_par_touka.png')
plt.show()
plt.clf()

for name in df.index:
    member_chars = df.loc[name, 'n_char']
    plt.plot(member_chars, range(len(member_chars))[::-1], label=name)

plt.gcf().autofmt_xdate()
plt.legend()
plt.ylabel('Nombre de caractères')
plt.title('Nombre de caractères total dans le temps par touka')
plt.savefig('../figures/nb_caractères_dans_le_temps_par_touka.png')
plt.show()
plt.clf()

for name in df.index:
    timestamps = [datetime.timestamp(date) for date in df.loc[name, 'tzt_msg'].keys()]
    temps, activite_ = activite_interp(timestamps, range(len(timestamps)),
                                       dx=3600 * 24 * 30)  # Moyenné sur 1 mois
    date_list = [datetime.datetime.fromtimestamp(t) for t in temps]  # converted
    plt.plot(date_list, activite_, label=name)

plt.gcf().autofmt_xdate()
plt.legend()
plt.ylabel('Activité [messages/jour]')
plt.title('Activité dans le temps par touka\nmoyenné sur un mois')
plt.savefig('../figures/activite_dans_le_temps_par_touka_sans_total.png')
plt.show()
plt.clf()
