import pandas as pd
from datetime import datetime
from flask import Flask
from flask import render_template
from pymongo import MongoClient
import json
from bson import json_util
from bson.json_util import dumps


MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
MONGODB_URI = "mongodb+srv://jtpaquet:pv9E9SB5gAVzKWbW@toukaanalytics-epm7v.gcp.mongodb.net/ToukaAnalytics?retryWrites=true&w=majority"
DBS_NAME = 'ToukaAnalytics'
FIELDS = {'content': True, 'author' : True, 'timestamp' : True, 'type' : True, 'reactions': True}

t0 = datetime.now()
connection = MongoClient(MONGODB_URI)
database = connection[DBS_NAME]
members = database['members']
messages = database['messages']
print('connexion time:', datetime.now()-t0)
pseudos = {author['name'] : author['pseudo'] for author in list(members.find())}
df = pd.DataFrame()
connection.close()

# Compile overall data on whole database
t0 = datetime.now()
data = {}
data['n_msg'] = {pseudos[d['_id']] : d['count'] for d in list(messages.aggregate([{"$sortByCount": "$author"}]))}
n_word_pipeline = [{"$match": {"content": {"$exists":True}}},{"$project": {"author": 1, "n_word": {"$size": {"$split": ["$content", " "]}}}}, {"$group" : { "_id" : "$author", "n_word" : {"$sum":"$n_word"}}}]
data['n_word'] = {pseudos[d['_id']] : d['n_word'] for d in list(messages.aggregate(n_word_pipeline))}
n_char_pipeline = [{"$match": {"content": {"$exists":True}}},{"$project": {"author": 1, "n_char": {"$strLenCP" : "$content"}}}, {"$group" : { "_id" : "$author", "n_char" : {"$sum":"$n_char"}}}]
data['n_char'] = {pseudos[d['_id']] : d['n_char'] for d in list(messages.aggregate(n_char_pipeline))}
data['ratio_char_msg'] = {name : data['n_char'][name]/data['n_msg'][name] for name in pseudos.values()}
data['ratio_word_msg'] = {name : data['n_word'][name]/data['n_msg'][name] for name in pseudos.values()}
data['total_msg'] = list(messages.aggregate( [ { "$collStats": { "storageStats": { } } } ] ))[0]['storageStats']['count']
data['date_min'] = list(messages.aggregate([{"$group":{"_id": {}, "date_min": { "$min": "$timestamp" }}}]))[0]['date_min']
data['date_max'] = list(messages.aggregate([{"$group":{"_id": {}, "date_max": { "$max": "$timestamp" }}}]))[0]['date_max']
print('mongo pipeline time:', datetime.now()-t0)
date_pipeline = [{"$project": {"date" : {"$toDate" : "$timestamp"}}}, {"$group" : {"_id" : { "$dateToString": { "format": "%m-%Y", "date": "$date" }}, "n_msg": {"$sum": 1}}}]
# Faire les groupes par hour, weekday et month
data['n_msg_by_hour'] = df.groupby(['author', df['date'].dt.hour])['_id'].count()
data['n_msg_by_weekday'] = df.groupby(['author', df['date'].dt.dayofweek])['_id'].count()
data['n_msg_by_month'] = df.groupby(['author', pd.DatetimeIndex(df['date']).to_period("M")])['date'].count()
data['total_msg_by_month'] = df.groupby(pd.DatetimeIndex(df['date']).to_period("M"))['_id'].count()
# Faire les reactions
for key in data.keys():
	if key not in ['total_msg', 'date_min', 'date_max']:
		if key in ['n_msg_by_hour', 'n_msg_by_weekday']:
			data[key] = {k: v.droplevel(0).to_dict() for k, v in data[key].groupby(level=0)}
		elif key == 'n_msg_by_month':
			data[key] = {k: v.droplevel(0).to_dict() for k, v in data[key].groupby(level=0)}
			for author in pseudos:
				data[key][author] = {k.strftime("%Y-%m"): v for k,v in data[key][author].items()}
		elif key == 'total_msg_by_month':
			data[key] = {k.strftime("%Y-%m"): v for k, v in data[key].items()}
		else:
			data[key] = data[key].to_dict() # Transform series objects to dict for further json conversion
print('compiling data time: ', datetime.now()-t0)
json.dumps(data)
