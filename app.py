from flask import Flask, render_template, request, json
import os
from database.database import Database
from dotenv import load_dotenv, find_dotenv


# Configuration
app = Flask(__name__)
load_dotenv(find_dotenv())

# Set the variables in the application
host = os.environ.get("340DBHOST")
user = os.environ.get("340DBUSER")
passwd = os.environ.get("340DBPW")
db = os.environ.get("340DB")
# enter the databae schema
schema = {
    "customer_contacts": ["id", "first_name", "last_name", "email", "phone_number", "house_id"],
    "houses": ["id", "street_address", "street_address_2", "city", "state", "zip_code", "yard_size_acres", "sales_manager_id"],
    "jobs": ["id", "date", "total_price", "house_id"],
    "job_workers": ["job_id", "worker_id"],
    "lawnmowers": ["id", "brand", "make_year", "model_name", "is_functional"],
    "sales_managers": ["id", "region", "first_name", "last_name", "email", "phone_number"],
    "workers": ["id", "first_name", "last_name", "email", "phone_number", "lawnmower_id"],
}
# instantiate a Database for ease of running queries
database = Database(host, user, passwd, db, schema)

# Routes 
@app.route('/',methods=['GET'])
def root():
    return render_template("index.j2")

@app.route('/customer-contacts',methods=['GET'])
def customer_contacts():
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    if not first_name and not last_name:
        results = database.select_all('customer_contacts')
    else:
        results = database.search_contacts(first_name, last_name)
    return render_template("customer-contacts.j2", name="Customer Contacts", table_data=results)

@app.route('/houses',methods=['GET'])
def houses():
    results = database.select_all('houses')
    return render_template("houses.j2", name="Houses", table_data=results)

@app.route('/job-workers',methods=['GET'])
def job_workers():
    results = database.select_all('job_workers')
    return render_template("job-workers.j2", name="Job Workers", table_data=results)

@app.route('/jobs',methods=['GET'])
def jobs():
    results = database.select_all('jobs')
    return render_template("jobs.j2", name="Jobs", table_data=results)

@app.route('/lawnmowers',methods=['GET'])
def lawnmowers():
    results = database.select_all('lawnmowers')
    return render_template("lawnmowers.j2", name="Lawnmowers", table_data=results)

@app.route('/sales-managers',methods=['GET'])
def sales_managers():
    results = database.select_all('sales_managers')
    return render_template("sales-managers.j2", name="Sales Managers", table_data=results)

@app.route('/workers',methods=['GET'])
def workers():
    results = database.select_all('workers')
    return render_template("workers.j2", name="Workers", table_data=results)


# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 7513))    
    app.run(port=port, debug=True) 
