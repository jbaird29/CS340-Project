from flask import Flask, render_template, redirect, request, json
import os
from database.database import LennysDB
from dotenv import load_dotenv, find_dotenv


# Configuration
app = Flask(__name__)
load_dotenv(find_dotenv())

# Set the variables in the application
host = os.environ.get("340DBHOST")
user = os.environ.get("340DBUSER")
passwd = os.environ.get("340DBPW")
db = os.environ.get("340DB")
# instantiate a Database for ease of running queries
database = LennysDB(host, user, passwd, db)

# Routes 
@app.route('/',methods=['GET'])
def root():
    return render_template("index.j2")

@app.route('/500',methods=['GET'])
def server_err():
    return render_template("500-error.j2") 

@app.route('/insert',methods=['POST'])
def insert_request():
    """This is the handler for EVERY insert operation; all forms POST to this route"""
    # TODO: might want to add more server-side form validation; only have client-side right now
    data: dict = request.form.copy()
    # every form data has a "table_name" key:value pair (inputted from the submit button)
    # this extracts it from the dict and uses it the table for the insert operation
    table_name: str = data.pop('table_name')
    valid = database.insert_into(table_name, data)
    if valid:
        route_name = table_name.replace('_', '-')
        return redirect(f'/{route_name}')  # effectively refreshes the page and shows the newly added table_data
    else:
        return redirect("/500") 

@app.route('/delete-sales-manager',methods=['POST'])
def delete_sales_manager():
    sales_manager_id = request.form.get('id')
    valid = database.delete_sales_manager(sales_manager_id)
    if valid:
        return redirect('/sales-managers')
    else:
        return redirect("/500")

@app.route('/update-lawnmower-status', methods=['POST'])
def update_lawnmower_status():
    lawnmower_id = request.form.get('id')
    is_functional = request.form.get('is_functional')
    valid = database.update_lawnmower_status(lawnmower_id, is_functional)
    if valid:
        return redirect('/lawnmowers')
    else:
        return redirect("/500")

@app.route('/update-houses-sales-manager', methods=['POST'])
def update_houses_sales_manager():
    house_id = request.form.get('id')
    sales_manager_id = request.form.get('sales_manager_id')
    valid = database.update_houses_sales_manager(house_id, sales_manager_id)
    if valid:
        return redirect('/houses')
    else:
        return redirect("/500")

@app.route('/update-job-worker', methods=['POST'])
def update_job_worker():
    old_job_id = request.form.get('old_job_id')
    old_worker_id = request.form.get('old_worker_id')
    new_worker_id = request.form.get('new_worker_id')
    new_job_id = request.form.get('new_job_id')
    valid = database.update_job_worker(old_job_id, old_worker_id, new_worker_id, new_job_id)
    if valid:
        return redirect('/job-workers')
    else:
        return redirect("/500")

@app.route('/customer-contacts',methods=['GET'])
def customer_contacts():
    # first and last name query params are used for the "Search" functionality
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    # if no query params, show all data; otherwise, filter data based on the inputs
    if not first_name and not last_name:
        table_data = database.select_all('customer_contacts')
    else:
        table_data = database.search_contacts(first_name, last_name)
    fields = database.get_table_fields('customer_contacts')
    house_ids = database.select_house_ids()  # populates dropdown
    return render_template("customer-contacts.j2", name="Customer Contacts", fields=fields, table_data=table_data, house_ids=house_ids)

@app.route('/houses',methods=['GET'])
def houses():
    table_data = database.select_all('houses')
    fields = database.get_table_fields('houses')
    sales_manager_ids = database.select_sales_manager_ids()  # populates dropdown
    return render_template("houses.j2", name="Houses", fields=fields, table_data=table_data, sales_manager_ids=sales_manager_ids)

@app.route('/job-workers',methods=['GET'])
def job_workers():
    table_data = database.select_all('job_workers')
    fields = database.get_table_fields('job_workers')
    job_ids = database.select_job_ids()  # populates dropdown
    worker_ids = database.select_worker_ids()  # populates dropdown
    return render_template("job-workers.j2", name="Job Workers", fields=fields, table_data=table_data, job_ids=job_ids, worker_ids=worker_ids)

@app.route('/jobs',methods=['GET'])
def jobs():
    table_data = database.select_all('jobs')
    fields = database.get_table_fields('jobs')
    house_ids = database.select_house_ids()  # populates dropdown
    return render_template("jobs.j2", name="Jobs", fields=fields, table_data=table_data, house_ids=house_ids)

@app.route('/lawnmowers',methods=['GET'])
def lawnmowers():
    table_data = database.select_all_lawnmowers()
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
    lawnmower_ids = database.select_lawnmower_ids()  # populates dropdown
    return render_template("workers.j2", name="Workers", fields=fields, table_data=table_data, lawnmower_ids=lawnmower_ids)


# Listener
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 9597))    
    app.run(port=port, debug=True) 
