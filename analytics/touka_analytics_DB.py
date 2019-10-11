import pandas as pd
from pymongo import MongoClient
import numpy as np
from scipy.interpolate import interp1d
import os

touka_dir = os.path.dirname(os.path.dirname(__file__))
localDB_dir = os.path.join(touka_dir, 'localDB')

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

    member_messages = [ msg['content'] for msg in messages.find(query_txt) ]
    member_dates = [ msg['date'] for msg in messages.find(query_txt) ]
    member_timestamps = [ msg['timestamp'] for msg in messages.find(query_txt) ]
    member_types = [ msg['type'] for msg in messages.find() ]
    member_reacts = [ msg['reaction'] for msg in messages.find(query_react) ]
    n_msg = messages.find(query_txt).count()

    data.append( {'Name': member['pseudo'], 'txt_msg': member_messages, 'msg_timestamps' : member_timestamps, 'date_msg' : member_dates, 'Type': member_types, 'Reaction' : member_reacts, 'msg_count' : n_msg} )

df = pd.DataFrame(data, columns=('Name', 'txt_msg', 'msg_timestamps', 'date_msg', 'Type', 'Reaction', 'msg_count'))
df = df.set_index('Name')

nb_characters = []
nb_characters_total = []
for member in df.index:
    s = 0
    s_total = []
    for msg in df.loc[member, 'txt_msg']:
        s += len(msg)
        s_total.append(s)
    nb_characters.append(s_total)
    nb_characters_total.append(s)

df['n_char'] = nb_characters
df['n_char_total'] = nb_characters_total

df['ratio_char_msg'] = df['n_char_total'] / df['msg_count']

df.to_csv(os.path.join(localDB_dir, 'df.csv'))