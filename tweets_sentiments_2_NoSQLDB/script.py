# connecting to your Cloudant instance
import ibm_db
import couchdb
import json

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

dsn = (
    "DRIVER={{IBM DB2 ODBC DRIVER}};"
    "DATABASE={0};"
    "HOSTNAME={1};"
    "PORT={2};"
    "PROTOCOL=TCPIP;"
    "UID={3};"
    "PWD={4};").format(dsn_database, dsn_hostname, dsn_port, dsn_uid, dsn_pwd)

conn = ibm_db.connect(dsn, "", "")

cloudant_user = conf["cloudant_user"]
cloudant_pass = conf["cloudant_pass"]

couch = couchdb.Server("https://%s.cloudant.com" % cloudant_user)
couch.resource.credentials = (cloudant_user, cloudant_pass)

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

query = "SELECT * FROM MINSA_TWEETS;"
    # run direct SQL
stmt = ibm_db.exec_immediate(conn, query)
tuple_db = ibm_db.fetch_tuple(stmt)
while tuple_db != False:
    print "Tweet text : ", tuple_db[1]
    tuple_db = ibm_db.fetch_tuple(stmt)
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