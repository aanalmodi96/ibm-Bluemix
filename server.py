# Name:Akshay Waikar
# ID:1001373973
# Course number- CSE 6331-003
import os
from flask import Flask,redirect,render_template,request
import urllib
import datetime
import json
import ibm_db

app = Flask(__name__)

# get service information if on IBM Cloud Platform
"""if 'VCAP_SERVICES' in os.environ:
    db2info = json.loads(os.environ['VCAP_SERVICES'])['dashDB For Transactions'][0]
    db2cred = db2info["credentials"]
    appenv = json.loads(os.environ['VCAP_APPLICATION'])
else:
    raise ValueError('Expected cloud environment')
"""
# handle database request and query city information
def city(name=None):
    # connect to DB2
    db2conn = ibm_db.connect("DATABASE="+db2cred['db']+";HOSTNAME="+db2cred['hostname']+";PORT="+str(db2cred['port'])+";UID="+db2cred['username']+";PWD="+db2cred['password']+";","","")
    if db2conn:
        # we have a Db2 connection, query the database
        sql="Select * from people where name=? "
        # Note that for security reasons we are preparing the statement first,
        # then bind the form input as value to the statement to replace the
        # parameter marker.
        stmt = ibm_db.prepare(db2conn,sql)
        ibm_db.bind_param(stmt, 1, name)
        ibm_db.execute(stmt)
        rows=[]
        # fetch the result
        result = ibm_db.fetch_assoc(stmt)
        while result != False:
            rows.append(result.copy())
            result = ibm_db.fetch_assoc(stmt)
        # close database connection
        ibm_db.close(db2conn)
    return render_template('city.html', ci=rows)

def searchforgrade():
    # connect to DB2
    db2conn = ibm_db.connect("DATABASE="+db2cred['db']+";HOSTNAME="+db2cred['hostname']+";PORT="+str(db2cred['port'])+";UID="+db2cred['username']+";PWD="+db2cred['password']+";","","")
    if db2conn:
        # we have a Db2 connection, query the database
        sql="Select * from people where grade<99 "
        # Note that for security reasons we are preparing the statement first,
        # then bind the form input as value to the statement to replace the
        # parameter marker.
        stmt = ibm_db.prepare(db2conn,sql)
        ibm_db.execute(stmt)
        rows=[]
        # fetch the result
        result = ibm_db.fetch_assoc(stmt)
        while result != False:
            rows.append(result.copy())
            result = ibm_db.fetch_assoc(stmt)
        # close database connection
        ibm_db.close(db2conn)
    return render_template('city.html', ci=rows)

def deleteuser(name=None):
    # connect to DB2
    db2conn = ibm_db.connect("DATABASE=BLUDB;HOSTNAME=dashdb-txn-sbox-yp-dal09-04.services.dal.bluemix.net;PORT=50000;PROTOCOL=TCPIP;UID=mpf20416;PWD=zqjs5@b82b42qmm8;"";","","")
    if db2conn:
        # we have a Db2 connection, query the database
        sql="Delete from people where name=Jees"
        # Note that for security reasons we are preparing the statement first,
        # then bind the form input as value to the statement to replace the
        # parameter marker.
        stmt = ibm_db.prepare(db2conn,sql)
        ibm_db.bind_param(stmt, 1, name)
        ibm_db.execute(stmt)
        rows=[]
        # fetch the result
        # close database connection
        ibm_db.close(db2conn)
    return render_template('update.html')

def updatekeywords(name=None,keywords=None):
    # connect to DB2
    db2conn = ibm_db.connect("DATABASE="+db2cred['db']+";HOSTNAME="+db2cred['hostname']+";PORT="+str(db2cred['port'])+";UID="+db2cred['username']+";PWD="+db2cred['password']+";","","")
    if db2conn:
        # we have a Db2 connection, query the database
        sql="Update people set keywords=? where name=? "
        stmt = ibm_db.prepare(db2conn,sql)
        ibm_db.bind_param(stmt, 1, keywords)
        ibm_db.bind_param(stmt, 2, name)
        ibm_db.execute(stmt)
        rows=[]
        # fetch the result
        # close database connection
        ibm_db.close(db2conn)
    return render_template('update.html')

def updategrade(name=None,grade=None):
    # connect to DB2
    db2conn = ibm_db.connect("DATABASE="+db2cred['db']+";HOSTNAME="+db2cred['hostname']+";PORT="+str(db2cred['port'])+";UID="+db2cred['username']+";PWD="+db2cred['password']+";","","")
    if db2conn:
        # we have a Db2 connection, query the database
        sql="Update people set grade=? where name=? "
        stmt = ibm_db.prepare(db2conn,sql)
        ibm_db.bind_param(stmt, 1, grade)
        ibm_db.bind_param(stmt, 2, name)
        ibm_db.execute(stmt)
        rows=[]
        # fetch the result
        # close database connection
        ibm_db.close(db2conn)
    return render_template('update.html')
# main page to dump some environment information
@app.route('/')
def index():
   return render_template('index.html', app=appenv)

# for testing purposes - use name in URI
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

@app.route('/search', methods=['GET'])
def searchroute():
    name = request.args.get('name', '')
    return city(name)

@app.route('/searchforgrade', methods=['GET'])
def searchgrade():
    return searchforgrade()

@app.route('/removedave', methods=['GET'])
def deluser():
    name = request.args.get('name', '')
    return deleteuser(name)

@app.route('/updatekeywords', methods=['GET'])
def updatekey():
    name = request.args.get('name', '')
    keywords = request.args.get('keywords', '')
    return updatekeywords(name,keywords)

@app.route('/updategrade', methods=['GET'])
def updategrad():
    name = request.args.get('name', '')
    grade = request.args.get('grade', '')
    return updategrade(name,grade)    

@app.route('/city/<name>')
def cityroute(name=None):
    return city(name)

port = os.getenv('PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))
