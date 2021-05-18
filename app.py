from flask import Flask, render_template, json
import MySQLdb
import os
from dotenv import load_dotenv, find_dotenv


# Configuration
app = Flask(__name__)
load_dotenv(find_dotenv())

# Set the variables in our application with those environment variables
host = os.environ.get("340DBHOST")
user = os.environ.get("340DBUSER")
passwd = os.environ.get("340DBPW")
db = os.environ.get("340DB")
db_connection = MySQLdb.connect(host,user,passwd,db)


# Routes 
@app.route('/',methods=['GET'])
def root():
    return render_template("index.j2")

@app.route('/customer-contacts',methods=['GET'])
def customer_contacts():
    query = "SELECT * FROM customer_contacts"
    cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(query, args=None)
    db_connection.commit()
    results = cursor.fetchall()
    return render_template("customer-contacts.j2", table_data=results)

@app.route('/houses',methods=['GET'])
def houses():
    return render_template("houses.j2")

@app.route('/job-workers',methods=['GET'])
def job_workers():
    return render_template("job-workers.j2")

@app.route('/jobs',methods=['GET'])
def jobs():
    return render_template("jobs.j2")

@app.route('/lawnmowers',methods=['GET'])
def lawnmowers():
    return render_template("lawnmowers.j2")

@app.route('/sales-managers',methods=['GET'])
def sales_managers():
    return render_template("sales-managers.j2")

@app.route('/workers',methods=['GET'])
def workers():
    return render_template("workers.j2")


# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 7513))    
    app.run(port=port, debug=True) 
