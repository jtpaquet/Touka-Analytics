import pandas as pd
import matplotlib.pyplot as plt
from pymongo import MongoClient

client = MongoClient("localhost", 27017)
db = client['ToukaAnalytics']

members = db['members']
messages = db['messages_7mai2021']

# recherche = input("Entrez le mot à rechercher: ")
recherche = 'ftcdg'

data = []
for member in members.find({}):
    name = member['name']
    query = {"$and": [{"content": {"$regex" : '^'+recherche, "$options": 'i'}}, {"author": name}] }
    count = messages.find(query).count()
    dates = messages.distinct('date', query)
    data.append({'Name': member['pseudo'], 'Count': count, 'Date': dates, 'Range' : range(count,0,-1)})

df = pd.DataFrame(data, columns=('Name', 'Count', 'Date', 'Range'))
df = df.sort_values('Date', ascending=True)
df = df.set_index('Name')

ax = df.plot.bar(y='Count', use_index=True)
plt.ylabel('Nombre de mentions du mot {}'.format(recherche))
plt.title('Nombre de mentions du mot {} par touka'.format(recherche))
plt.show()
plt.clf()

for name in df.index.values:
    plt.plot(df.loc[name, 'Date'], df.loc[name, 'Range'], label=name)
plt.gcf().autofmt_xdate()
plt.yscale('linear')
plt.legend()
plt.ylabel('Nombre de mentions du mot {}'.format(recherche))
plt.title('Nombre de mentions du mot {} dans le temps par touka'.format(recherche))
plt.show()
plt.clf()