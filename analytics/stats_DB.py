import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import json
import os


with open('json_data.djezeune') as f:
    data = json.load(f)


members = {'Charles Pilon': "Charles", 'Christophe Landry-bergeron': "Krostif", 'Coralie Beaulieu': "Co", 'Jérémy Talbot-Pâquet': "Djézeune", 'Jérôme Sirois Charron': "Jirome", 'Meggie Lacasse': "Méganie", 'Pierre-Olivier Marotte': "Pierre-Poom", 'Vincent Masson-Boutin': "Vinssan", 'William Lacasse': "Lakasse", 'Étienne Godbout': "Godbout", 'Étienne Rouleau': "Roulo"}

# Bar chart msg per person

data_ = dict(sorted(data["n_msg"].items(), key=lambda item: item[1], reverse=True))
data_.pop('Charles Pilon', None)
data_.pop('Estère', None)
data_.pop('Kaven', None)
data_.pop('Marcel Leboeuf', None)
data_.pop('Pat Laf', None)

plt.bar(range(len(data_)), list(data_.values()), align='center')
plt.xticks(range(len(data_)), list(data_.keys()), rotation=30)
plt.title("Nombre de messages par personne")
plt.tight_layout()
plt.savefig("stats\\stats_7mai2021\\n_msg.png")
# plt.show()
plt.clf()


# Bar word ratio per msg

data_ = dict(sorted(data["ratio_word_msg"].items(), key=lambda item: item[1], reverse=True))
data_.pop('Charles Pilon', None)
data_.pop('Estère', None)
data_.pop('Kaven', None)
data_.pop('Marcel Leboeuf', None)
data_.pop('Pat Laf', None)

plt.bar(range(len(data_)), list(data_.values()), align='center')
plt.xticks(range(len(data_)), list(data_.keys()), rotation=30)
plt.title("Ratio moyen de mots par message")
plt.tight_layout()
plt.savefig("stats\\stats_7mai2021\\word_per_msg.png")
# plt.show()
plt.clf()


# Bar chart reacts per person

data_ = {}
for doc in data["react_made_by_actor"]:
    data_[members[doc["_id"]]] = doc["count"]

data_ = dict(sorted(data_.items(), key=lambda item: item[1], reverse=True))
data_.pop('Charles', None)
data_.pop('Estère', None)
data_.pop('Kaven', None)
data_.pop('Marcel Leboeuf', None)
data_.pop('Pat Laf', None)

plt.bar(range(len(data_)), list(data_.values()), align='center')
plt.xticks(range(len(data_)), list(data_.keys()), rotation=30)
plt.title("Nombre de reacts par personne")
plt.tight_layout()
plt.savefig("stats\\stats_7mai2021\\reacts_per_person.png")
# plt.show()
plt.clf()


# Msg per month

data_ = {}
for doc in data["total_msg_by_month"]:
    data_[doc["_id"]] = doc["n_msg"]
data_ = np.array(sorted(data_.items(), key = lambda x:datetime.datetime.strptime(x[0], '%m-%Y'), reverse=False))
x_values = [datetime.datetime.strptime(m, '%m-%Y') for m in data_[:,0]]
y_values = data_[:,1]
y_values = y_values.astype('int')

fig, ax = plt.subplots()
ax.plot(x_values, y_values)
date_form = mdates.DateFormatter("%b-%Y")
ax.xaxis.set_major_formatter(date_form)
# ax.xaxis.set_minor_locator(mdates.MonthLocator(interval=3))
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=4))
ax.xaxis.set_minor_locator(mdates.MonthLocator(interval=1))
ax.tick_params(axis="x", which="major", length=8, grid_linewidth=1.5)
ax.tick_params(axis="x", which="minor", length=3, grid_linewidth=0.75)
plt.grid(True, "both")
fig.set_size_inches(20.,12.)
ax.set_xlim([datetime.date(2014, 8, 1), datetime.date(2021, 6, 1)])
plt.savefig("stats\\stats_7mai2021\\msg_per_month.png")
plt.show()
plt.clf()


# Msg per year

data_ = {}
for doc in data["total_msg_by_year"]:
    data_[doc["_id"]] = doc["n_msg"]
data_ = np.array(sorted(data_.items(), key = lambda x:datetime.datetime.strptime(x[0], '%Y'), reverse=False))
year = data_[:,0]
msg = [int(n) for n in data_[:,1]]

plt.bar(range(len(year)), msg, align='center')
plt.xticks(range(len(data_)), year)
plt.title("Message par année")
plt.tight_layout()
plt.savefig("stats\\stats_7mai2021\\msg_per_year.png")
# plt.show()
plt.clf()

# print(data)



