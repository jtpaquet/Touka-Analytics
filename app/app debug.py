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
msg_by_month_pipeline = [{"$project": {"date" : {"$toDate" : "$timestamp"}}}, {"$group" : {"_id" : { "$dateToString": { "format": "%m-%Y", "date": "$date" }}, "n_msg": {"$sum": 1}}}]
msg_by_year_pipeline = [{"$project": {"date" : {"$toDate" : "$timestamp"}}}, {"$group" : {"_id" : { "$dateToString": { "format": "%Y", "date": "$date" }}, "n_msg": {"$sum": 1}}}]
msg_by_author_by_hour_pipeline = [{"$project": {"author": 1, "date" : {"$toDate" : "$timestamp"}}}, {"$group" : {"_id" : {"author": "$author", "hour": {"$dateToString": { "format": "%H", "date": "$date" }}}, "n_msg": {"$sum": 1}}}]
msg_by_author_by_weekday_pipeline = pipeline = [{"$project": {"author": 1, "date" : {"$toDate" : "$timestamp"}}}, {"$group" : {"_id" : {"author": "$author", "weekday": {"$dateToString": { "format": "%w", "date": "$date" }}}, "n_msg": {"$sum": 1}}}]
msg_by_author_by_month_pipeline = [{"$project": {"author": 1, "date" : {"$toDate" : "$timestamp"}}}, {"$group" : {"_id" : {"author": "$author", "date": {"$dateToString": { "format": "%m-%Y", "date": "$date" }}}, "n_msg": {"$sum": 1}}}]
msg_by_author_by_year_pipeline = pipeline = [{"$project": {"author": 1, "date" : {"$toDate" : "$timestamp"}}}, {"$group" : {"_id" : {"author": "$author", "year": {"$dateToString": { "format": "%Y", "date": "$date" }}}, "n_msg": {"$sum": 1}}}]
# Faire les groupes par hour, weekday et month
data['n_msg_by_hour'] = {(d['_id']['author'], d['_id']['hour'] ) : d['n_msg'] for d in messages.aggregate(msg_by_author_by_hour_pipeline)}
data['n_msg_by_weekday'] = {(d['_id']['author'], d['_id']['weekday'] ) : d['n_msg'] for d in messages.aggregate(msg_by_author_by_weekday_pipeline)}
data['n_msg_by_month'] = {(d['_id']['author'], d['_id']['date'] ) : d['n_msg'] for d in messages.aggregate(msg_by_author_by_month_pipeline)}
data['n_msg_by_year'] = {(d['_id']['author'], d['_id']['year'] ) :  d['n_msg'] for d in messages.aggregate(msg_by_author_by_year_pipeline)}
data['total_msg_by_month'] = {d['_id']: d['n_msg'] for d in messages.aggregate(msg_by_month_pipeline)}
data['total_msg_by_year'] = {d['_id']: d['n_msg'] for d in messages.aggregate(msg_by_year_pipeline)}

for stat in ["n_msg_by_hour", "n_msg_by_weekday", "n_msg_by_month", "n_msg_by_year"]: # Transform in nested dict for further json conversion
	new_dict = {}
	for key, value in data[stat].items():
		author, date = key
		if author not in new_dict.keys():
			new_dict[author] = {}
		new_dict[author][date] = value
	data[stat] = new_dict
# Faire les reactions
print('compiling data time: ', datetime.now()-t0)
json.dumps(data)
print("bruh")