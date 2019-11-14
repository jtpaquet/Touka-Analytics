import pandas as pd
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
FIELDS = {'content': True, 'author' : True, 'timestamp' : True, 'type' : True}
connection = MongoClient(MONGODB_URI)
database = connection[DBS_NAME]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/rawDB")
def rawDB():
	collection = database['messages']
	projects = collection.find(projection=FIELDS, limit=5000)
	json_projects = [project for project in projects]
	json_projects = json.dumps(json_projects, default=json_util.default)
	return json_projects

	
@app.route("/ToukaAnalytics")
def ToukaAnalytics():
	members = database['members']
	messages = database['messages']
	
	data = []
	for member in members.find():
		name = member['name']
		# messages.aggregate( [ { "$project" : { 'content' : 1 , 'date' : 1 } } ] )
		query_txt = {'$and': [ {'author': name}, {'content': {'$exists': True, '$ne': None } } ] }
		query_react = {'$and': [ {'author': name}, {'reaction': {'$exists': True, '$ne': None } } ] }

		member_messages, member_timestamps, member_types, member_reacts = [], [], [], []

		for msg in messages.find(query_txt): # Changer ça ici, c'est long af
			member_messages.append(msg['content'])
			member_timestamps.append(msg['timestamp'])
			member_types.append(msg['type'])
			member_reacts.append(msg['reactions'])

		n_msg = messages.find(query_txt).count()

		data.append( {'Name': member['pseudo'], 'txt_msg': member_messages, 'msg_timestamps' : member_timestamps, 'Type': member_types, 'Reaction' : member_reacts, 'msg_count' : n_msg} )

	df = pd.DataFrame(data, columns=('Name', 'txt_msg', 'msg_timestamps', 'Type', 'Reaction', 'msg_count'))
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

	df['char_count'] = nb_characters_total

	df['ratio_char_msg'] = df['char_count'] / df['msg_count']

	df = df.drop(columns=["txt_msg", "Type", "Reaction"])
	
	df_json = json.dumps(df.to_json(), default=json_util.default)
	return df.to_json()

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)
