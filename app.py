from flask import Flask, url_for, render_template
import json
import os 
from gevent.pywsgi import WSGIServer
import os
from pymongo import MongoClient

def getContent():
	dburl = os.environ['MONGODB_URI']

	client = MongoClient(dburl)

	db = client.get_default_database()

	members = db.members
	
	data = []

	for mem in members.find():
		data.append(mem)
	
	return data

app = Flask(__name__, static_url_path='/static')

content = getContent()

@app.route("/")
def hello():
	return render_template('index.html',context=content)

if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))
	http_server = WSGIServer(('',port),app)
	http_server.serve_forever()
	# app.run(host='0.0.0.0', port=port)
