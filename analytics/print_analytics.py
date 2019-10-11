import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
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

touka_dir = os.path.dirname(os.path.dirname(__file__))
fig_dir = os.path.join(touka_dir, 'figures')
localDB_dir = os.path.join(touka_dir, 'localDB')

data = pd.read_csv(os.path.join(localDB_dir, "df.csv") )
df = pd.DataFrame(data)
df = df.set_index('Name')

plt.bar(df.index, df['msg_count'])
plt.xticks(rotation=45, ha='right', size=10)
plt.ylabel('Nombre de messages total')
plt.title('Nombre de messages total envoyés sur Touka')
plt.savefig(os.path.join(fig_dir, 'bar_nb_messages_total.png'))
# plt.show()
plt.clf()

plt.bar(df.index, df['n_char_total'])
plt.xticks(rotation=45, ha='right', size=10)
plt.ylabel('Nombre de caractères écrits total')
plt.title('Nombre de caractères total envoyés sur Touka selon les toukas')
plt.savefig(os.path.join(fig_dir, 'bar_nb_char_total.png'))
# plt.show()
plt.clf()

plt.bar(df.index, df['ratio_char_msg'])
plt.xticks(rotation=45, ha='right', size=10)
plt.ylabel('Ratio')
plt.title('Ratio du nombre de caractères écrits par message sur Touka selon les toukas')
plt.savefig(os.path.join(fig_dir, 'bar_ratio_char_msg.png'))
# plt.show()
plt.clf()

for name in df.index:
    dates = df.loc[name, 'date_msg']

    plt.plot(dates, range(len(dates),0,-1), label=name)

plt.gcf().autofmt_xdate()
plt.legend()
plt.ylabel('Nombre de messages')
plt.title('Nombre de messages total dans le temps par touka')
plt.savefig(os.path.join(fig_dir, 'nb_messages_dans_le_temps_par_touka.png'))
# plt.show()
plt.clf()

for name in df.index:
    member_chars = df.loc[name, 'n_char']
    plt.plot(member_chars, range(len(member_chars))[::-1], label=name)

plt.gcf().autofmt_xdate()
plt.legend()
plt.ylabel('Nombre de caractères')
plt.title('Nombre de caractères total dans le temps par touka')
plt.savefig(os.path.join(fig_dir, 'nb_caractères_dans_le_temps_par_touka.png'))
# plt.show()
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
plt.savefig(os.path.join(fig_dir, 'activite_dans_le_temps_par_touka_sans_total.png'))
# plt.show()
plt.clf()
