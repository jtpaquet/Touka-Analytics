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
FIELDS = {'content': True, 'author' : True, 'timestamp' : True, 'type' : True}


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/rawDB")
def rawDB():
	connection = MongoClient(MONGODB_URI)
	database = connection[DBS_NAME]
	collection = database['messages']
	projects = collection.find(projection=FIELDS, limit=5000)
	json_projects = [project for project in projects]
	json_projects = json.dumps(json_projects, default=json_util.default)
	connection.close()
	return json_projects

	
@app.route("/ToukaAnalytics")
def ToukaAnalytics():
	connection = MongoClient(MONGODB_URI)
	database = connection[DBS_NAME]
	members = database['members']
	messages = database['messages']

	data = []
	t0 = datetime.now()
	for member in members.find():
		name = member['name']
		query_txt = {'$and': [ {'author': name}, {'content': {'$exists': True, '$ne': None } } ] }
		query_react = {'$and': [ {'author': name}, {'reaction': {'$exists': True, '$ne': None } } ] }
		fields = {'content': True, 'timestamp': True, 'type': True, 'reactions': True, '_id': False}
        
		fetched_data = list(messages.find(query_txt, fields))
		
		member_data = {}
		for field in list(fields.keys())[:-1]:
			if field == 'timestamp':
				member_data[field] = list(map(lambda d: int(d[field]), fetched_data))
			else:
				member_data[field] = list(map(lambda d: d[field], fetched_data))
			if field == 'content':
				s = 0
				for msg in member_data[field]:
					s += len(msg)
		
		member_data['n_char'] = s
		member_data['n_msg'] = len(member_data['content'])
		member_data['ratio_char_msg'] = member_data['n_char'] / member_data['n_msg']
		member_data['name'] = member['pseudo']

		data.append(member_data)

	t1 = datetime.now()
	print("total fetch data time:", t1-t0)
	df = pd.DataFrame(data, columns=('name', 'content', 'timestamp', 'type', 'reactions', 'n_msg', 'n_char', 'ratio_char_msg'))
	df = df.set_index('name')

	df = df.drop(columns=["content", "type", "reactions"])
	
	df_json = json.dumps(df.to_json(), default=json_util.default)
	connection.close()
	return df_json

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)
