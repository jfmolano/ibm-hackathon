# Copyright 2015 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import ibm_db
import os
import watson_developer_cloud
import couchdb
import ast
from flask import Flask, jsonify
import json
from flask_cors import CORS, cross_origin
import requests
from watson_developer_cloud import AlchemyLanguageV1

url = 'https://developer.ibm.com/watson/blog/2015/11/03/price-reduction-for-watson-personality-insights/'

with open('conf.json', 'r') as f:
    try:
        conf = json.load(f)
    except ValueError:
        conf = {}

dsn_hostname = conf["dsn_hostname"]
dsn_uid = conf["dsn_uid"]
dsn_pwd = conf["dsn_pwd"]

#Enter the values for you database connection
dsn_driver = "IBM DB2 ODBC DRIVER"
dsn_database = "BLUDB"            # e.g. "BLUDB"
dsn_port = "50000"                # e.g. "50000" 
dsn_protocol = "TCPIP"            # i.e. "TCPIP"

app = Flask(__name__)
CORS(app)

dsn = (
    "DRIVER={{IBM DB2 ODBC DRIVER}};"
    "DATABASE={0};"
    "HOSTNAME={1};"
    "PORT={2};"
    "PROTOCOL=TCPIP;"
    "UID={3};"
    "PWD={4};").format(dsn_database, dsn_hostname, dsn_port, dsn_uid, dsn_pwd)

conn = ibm_db.connect(dsn, "", "")

conn = ibm_db.connect(dsn, "", "")

cloudant_user = conf["cloudant_user"]
cloudant_pass = conf["cloudant_pass"]
alchemy_key = conf["alchemy_key"]
alchemy_language = AlchemyLanguageV1(api_key=alchemy_key)

couch = couchdb.Server("https://%s.cloudant.com" % cloudant_user)
couch.resource.credentials = (cloudant_user, cloudant_pass)

# accessing a database
db = couch['tweets_s']

@app.route('/')
def Welcome():
    return app.send_static_file('index.html')

@app.route('/myapp')
def WelcomeToMyapp():
    return 'Welcome again to my app running on Bluemix!'

@app.route('/test')
def test():
    # test query
    query = "SELECT * FROM EMPLEADOS;"
    # run direct SQL
    stmt = ibm_db.exec_immediate(conn, query)
    l = ibm_db.fetch_both(stmt)
    print l
    return 'Welcome again to my app running on Bluemix!' + str(l)

@app.route('/api/people')
def GetPeople():
    list = [
        {'name': 'John', 'age': 28},
        {'name': 'Bill', 'val': 26}
    ]
    return jsonify(results=list)

@app.route('/test_rest', methods=['GET'])
def test_rest():
    query = "SELECT * FROM EMPLEADOS;"
    # run direct SQL
    stmt = ibm_db.exec_immediate(conn, query)
    l = ibm_db.fetch_both(stmt)
    return jsonify(l)

@app.route('/api/people/<name>')
def SayHello(name):
    message = {
        'message': 'Hello ' + name
    }
    return jsonify(results=message)

@app.route('/get_tweets/<word>')
def get_tweets(word):
    url = "http://"+cloudant_user+".cloudant.com/tweets_s/_find"

    data = "{" + \
              "\"selector\": {" + \
                "\"_id\": {" + \
                  "\"$gt\": null" + \
                "}," + \
                "\"text\": {" + \
                  "\"$regex\": \".* "+word+" .*\"" + \
                "}" + \
              "}," + \
              "\"limit\":60"+ \
            "}"

    print data

    headers = {
        'Content-Type': "application/json"
        }

    response = requests.request("POST", url, data=data, headers=headers, auth=(cloudant_user, cloudant_pass))
    #print response.text
    #print ast.literal_eval(response.text)["docs"]
    l_tweets = ast.literal_eval(response.text)["docs"]
    l_resp = []
    for tweet in l_tweets:
        original_text = tweet["text"]
        #print text
        text = original_text.replace("#","").replace("@","").replace("://","").replace("/","")
        #print text
        #print alchemy_language.targeted_sentiment(text=text,targets=['eps'], language='spanish')["results"][0]["sentiment"]
        sentiment = alchemy_language.targeted_sentiment(text=text,targets=[word], language='spanish')["results"][0]["sentiment"]
        score = 0
        if "score" in sentiment:
            score = sentiment["score"]
        sentiment = sentiment["type"]
        l_resp.append({"sentiment":sentiment,"text":original_text,"score":score})
        #print l_resp
    return jsonify(result=l_resp)

port = os.getenv('PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))
