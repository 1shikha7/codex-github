from flask import Flask, url_for, render_template, request
import json
import os
from gevent.pywsgi import WSGIServer
from pymongo import MongoClient
from dotenv import load_dotenv
from difflib import SequenceMatcher as SM

load_dotenv()

def getContent():
    dburl = os.environ.get('MONGODB_URI')

    client = MongoClient(dburl)

    db = client.get_default_database()

    members = db.members

    data = []

    for mem in members.find():
        data.append(mem)

    data = sorted(data, key=lambda k: k['totalCommits'])

    return data[::-1]


app = Flask(__name__, static_url_path='/static')


@app.route("/")
def index():
    content = getContent()
    total = sum([x['totalCommits'] for x in content])
    return render_template('content.html', context=content, totalC=total, search=False)


@app.route("/search")
def searchMember():
    query = request.args.get("query")
    # print(query)
    content = getContent()

    ratios = [ { "ratio" : SM(None, x['name'].lower(), query.lower()).ratio(), "data": x } for x in content ]
    
    result = [ x['data'] for x in ratios if x['ratio'] > 0.4 ]

    found = len(result) != 0
    
    return render_template('content.html', context=result, search=True, found=found)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    http_server = WSGIServer(('', port), app)
    http_server.serve_forever()
