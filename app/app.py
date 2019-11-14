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
	
	df_json = json.dumps(df.to_json(), default=json_util.default)
	return df_json

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)
