# connecting to your Cloudant instance
import couchdb
import json

with open('conf.json', 'r') as f:
    try:
        conf = json.load(f)
    except ValueError:
        conf = {}

cloudant_user = conf["cloudant_user"]
cloudant_pass = conf["cloudant_pass"]

couch = couchdb.Server("https://%s.cloudant.com" % cloudant_user)
couch.resource.credentials = (cloudant_user, cloudant_pass)

with open('conf.json', 'r') as f:
    try:
        conf = json.load(f)
    except ValueError:
        conf = {}

# accessing a database
db = couch['tweets']
# or, creating one
#db = couch.create('prueba')

# accessing a document
#doc = db[DOCUMENT_ID]
# or, creating one
db.save({
  'name': 'jfmolano1587',
  'title': 'Fun Captain',
  'superpower': 'More fun than a hallucinogenic trampoline'
})
#doc = db[doc_id]

#Query results are treated as iterators, like this:

# print all docs in the database
#for doc in db:
#  print doc
# or, do the same on a pre-defined index
# where 'DDOC/INDEX' maps to '_design/DDOC/_view/INDEX'
# in the HTTP API
#for doc in db.view('DDOC/INDEX'):
#  print doc