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
        table_data = database.select_all('customer_contacts')
    else:
        table_data = database.search_contacts(first_name, last_name)
    fields = database.get_table_fields('customer_contacts')
    house_ids = database.select_ids('houses')
    return render_template("customer-contacts.j2", name="Customer Contacts", fields=fields, table_data=table_data, house_ids=house_ids)

@app.route('/houses',methods=['GET'])
def houses():
    table_data = database.select_all('houses')
    fields = database.get_table_fields('houses')
    sales_manager_ids = database.select_ids('sales_managers')
    return render_template("houses.j2", name="Houses", fields=fields, table_data=table_data, sales_manager_ids=sales_manager_ids)

@app.route('/job-workers',methods=['GET'])
def job_workers():
    table_data = database.select_all('job_workers')
    fields = database.get_table_fields('job_workers')
    job_ids = database.select_ids('jobs')
    worker_ids = database.select_ids('workers')
    return render_template("job-workers.j2", name="Job Workers", fields=fields, table_data=table_data, job_ids=job_ids, worker_ids=worker_ids)

@app.route('/jobs',methods=['GET'])
def jobs():
    table_data = database.select_all('jobs')
    fields = database.get_table_fields('jobs')
    return render_template("jobs.j2", name="Jobs", fields=fields, table_data=table_data)

@app.route('/lawnmowers',methods=['GET'])
def lawnmowers():
    table_data = database.select_all('lawnmowers')
    fields = database.get_table_fields('lawnmowers')
    return render_template("lawnmowers.j2", name="Lawnmowers", fields=fields, table_data=table_data)

@app.route('/sales-managers',methods=['GET'])
def sales_managers():
    table_data = database.select_all('sales_managers')
    fields = database.get_table_fields('sales_managers')
    return render_template("sales-managers.j2", name="Sales Managers", fields=fields, table_data=table_data)

@app.route('/workers',methods=['GET'])
def workers():
    table_data = database.select_all('workers')
    fields = database.get_table_fields('workers')
    lawnmower_ids = database.select_ids('lawnmowers')
    return render_template("workers.j2", name="Workers", fields=fields, table_data=table_data, lawnmower_ids=lawnmower_ids)


# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 7513))    
    app.run(port=port, debug=True) 
