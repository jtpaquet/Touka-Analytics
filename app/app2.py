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
FIELDS = {'content': True, 'author' : True, 'timestamp' : True, 'type' : True, '_id': False}


@app.route("/")
def index():
    return render_template("index2.html")

	
@app.route("/ToukaAnalytics")
def ToukaAnalytics():
    connection = MongoClient(MONGODB_URI)
    database = connection[DBS_NAME]
    members = database['members']
    collection = database['messages']
    projects = collection.find(projection=FIELDS)
    json_projects = []
    for project in projects:
        json_projects.append(project)
    json_projects = json.dumps(json_projects, default=json_util.default)
    connection.close()
    return json_projects

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)
