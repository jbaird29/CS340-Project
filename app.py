from flask import Flask, render_template, request, json
import MySQLdb
import os
import database.db_queries as queries
from dotenv import load_dotenv, find_dotenv


# Configuration
app = Flask(__name__)
load_dotenv(find_dotenv())

# Set the variables in our application with those environment variables
host = os.environ.get("340DBHOST")
user = os.environ.get("340DBUSER")
passwd = os.environ.get("340DBPW")
db = os.environ.get("340DB")
conn = MySQLdb.connect(host,user,passwd,db)


# Routes 
@app.route('/',methods=['GET'])
def root():
    return render_template("index.j2")

@app.route('/customer-contacts',methods=['GET'])
def customer_contacts():
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    if not first_name and not last_name:
        results = queries.select_all(conn, 'customer_contacts')
    else:
        results = queries.search_contacts(conn, first_name, last_name)
    return render_template("customer-contacts.j2", name="Customer Contacts", table_data=results)

@app.route('/houses',methods=['GET'])
def houses():
    results = queries.select_all(conn, 'houses')
    return render_template("houses.j2", name="Houses", table_data=results)

@app.route('/job-workers',methods=['GET'])
def job_workers():
    results = queries.select_all(conn, 'job_workers')
    return render_template("job-workers.j2", name="Job Workers", table_data=results)

@app.route('/jobs',methods=['GET'])
def jobs():
    results = queries.select_all(conn, 'jobs')
    return render_template("jobs.j2", name="Jobs", table_data=results)

@app.route('/lawnmowers',methods=['GET'])
def lawnmowers():
    results = queries.select_all(conn, 'lawnmowers')
    return render_template("lawnmowers.j2", name="Lawnmowers", table_data=results)

@app.route('/sales-managers',methods=['GET'])
def sales_managers():
    results = queries.select_all(conn, 'sales_managers')
    return render_template("sales-managers.j2", name="Sales Managers", table_data=results)

@app.route('/workers',methods=['GET'])
def workers():
    results = queries.select_all(conn, 'workers')
    return render_template("workers.j2", name="Workers", table_data=results)


# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 7513))    
    app.run(port=port, debug=True) 
