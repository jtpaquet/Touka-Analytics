import pandas as pd
from datetime import datetime
from flask import Flask
from flask import render_template
from pymongo import MongoClient
import json
from bson import json_util
from bson.json_util import dumps

app = Flask(__name__)

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
MONGODB_URI = "mongodb+srv://jtpaquet:pv9E9SB5gAVzKWbW@toukaanalytics-epm7v.gcp.mongodb.net/ToukaAnalytics?retryWrites=true&w=majority"
DBS_NAME = 'ToukaAnalytics'
FIELDS = {'content': True, 'author' : True, 'timestamp' : True, 'type' : True, 'reactions': True}


@app.route("/")
def index():
	return render_template("index.html")

	
@app.route("/ToukaAnalytics")
def ToukaAnalytics():
	t0 = datetime.now()
	connection = MongoClient(MONGODB_URI)
	database = connection[DBS_NAME]
	members = database['members']
	messages = database['messages']
	print('connexion time:', datetime.now()-t0)
	t0 = datetime.now()
	projects = messages.find(projection=FIELDS)
	print('fetch time:', datetime.now()-t0)
	json_projects = [project for project in projects]
	pseudos = [author['pseudo'] for author in list(members.find(projection={'pseudo':True}))]
	# Make and arrange DataFrame
	t0 = datetime.now()
	df = pd.DataFrame(json_projects)
	print('making df time:', datetime.now()-t0)
	t0 = datetime.now()
	for member in members.find():
		df = df.replace(member['name'], member['pseudo'])
	print('replacing name time: ', datetime.now()-t0)
	t0 = datetime.now()
	df['date'] = pd.to_datetime(df["timestamp"], unit='ms')
	print('timestamp to datetime time: ', datetime.now()-t0)
	connection.close()

	# Compile overall data on whole database
	t0 = datetime.now()
	data = {}
	data['n_msg'] = df.groupby(['author']).count()['_id']
	data['n_word'] = df.groupby(['author'])['content'].agg(lambda x: sum([len(str(msg).split(' ')) for msg in x]))
	data['n_char'] = df.groupby(['author'])['content'].agg(lambda x: sum([len(str(msg)) for msg in x]))
	data['ratio_char_msg'] = data['n_char'] / data['n_msg']
	data['ratio_word_msg'] = data['n_word'] / data['n_msg']
	data['total_msg'] = len(df.index)
	data['date_min'] = min(df['timestamp'])
	data['date_max'] = max(df['timestamp'])
	data['n_msg_by_hour'] = df.groupby(['author', df['date'].dt.hour])['_id'].count()
	data['n_msg_by_weekday'] = df.groupby(['author', df['date'].dt.dayofweek])['_id'].count()
	data['n_msg_by_month'] = df.groupby(['author', pd.DatetimeIndex(df['date']).to_period("M")])['date'].count()
	data['total_msg_by_month'] = df.groupby(pd.DatetimeIndex(df['date']).to_period("M"))['_id'].count()
	for key in data.keys():
		print(key)
		if key != 'total_msg':
			data[key] = data[key].to_dict() # Transform series objects to dict for further json conversion
	print('compiling data time: ', datetime.now()-t0)
	return json.dumps(data)


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)

def count_word(df_):
	s = 0
	for msg in df_['content']:
		s += len(msg.split(' '))
	return 
	
def count_char(df_):
	s = 0
	for msg in df_['content']:
		s += len(msg)
	return s

def count_total_msg(df_):
	s = 0
	for count in pd.DatetimeIndex(df_['date']).to_period("M").count():
		s += count
	return s

