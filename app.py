from flask import Flask, render_template, redirect, request, flash, json
from flask_mysqldb import MySQL
import os
from database.database import LennysDB
from dotenv import load_dotenv, find_dotenv


# Configuration
app = Flask(__name__)
load_dotenv(find_dotenv())

# Configure the db connection
app.config['MYSQL_HOST'] = os.environ.get("340DBHOST")
app.config['MYSQL_USER'] = os.environ.get("340DBUSER")
app.config['MYSQL_PASSWORD'] = os.environ.get("340DBPW")
app.config['MYSQL_DB'] = os.environ.get("340DB")
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

# configure secret for sessions
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")

# instantiate a Database for ease of running queries
database = LennysDB(mysql)

# Routes 
@app.route('/',methods=['GET'])
def root():
    return render_template("index.j2")

@app.route('/500',methods=['GET'])
def server_err():
    return render_template("500-error.j2") 

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

@app.route('/delete-job-worker', methods=['POST'])
def delete_job_woker():
    job_id = request.form.get('job_id')
    worker_id = request.form.get('worker_id')
    valid = database.delete_job_worker(job_id, worker_id)
    if valid:
        return redirect('/job-workers')
    else:
        return redirect("/500")

@app.route('/delete-job', methods=['POST'])
def delete_job():
    job_id = request.form.get('id')
    valid = database.delete_job(job_id)
    if valid:
        return redirect('/jobs')
    else:
        return redirect("/500")


@app.route('/customer-contacts',methods=['GET', 'POST'])
def customer_contacts():
    table = 'customer_contacts'
    name = "Customer Contacts"
    if request.method == 'POST':
        valid, res_msg = database.insert_into(table, request.form.copy())
        rsp_category = 'success' if valid else 'error'
        flash(res_msg, rsp_category)
        return redirect(request.url)
    if request.method == 'GET':
        # first and last name query params are used for the "Search" functionality
        first_name = request.args.get('first_name')
        last_name = request.args.get('last_name')
        # if no query params, show all data; otherwise, filter data based on the inputs
        if not first_name and not last_name:
            table_data = database.select_all(table)
        else:
            table_data = database.search_contacts(first_name, last_name)
        fields = database.get_table_fields(table)
        house_ids = database.select_house_ids()  # populates dropdown
        return render_template("customer-contacts.j2", name=name, fields=fields, table_data=table_data, house_ids=house_ids)

@app.route('/houses',methods=['GET', 'POST'])
def houses():
    table = 'houses'
    name = "Houses"
    if request.method == 'POST':
        form_data = request.form.copy()
        form_type = form_data.get('type')
        if form_type == 'update':
            house_id = form_data.get('id')
            sales_manager_id = form_data.get('sales_manager_id')
            valid, res_msg = database.update_houses_sales_manager(house_id, sales_manager_id)
            rsp_category = 'success' if valid else 'error'
            flash(res_msg, rsp_category)
        elif form_type == 'insert':
            valid, res_msg = database.insert_into(table, form_data)
            rsp_category = 'success' if valid else 'error'
            flash(res_msg, rsp_category)
        return redirect(request.url)
    if request.method == 'GET':
        table_data = database.select_all(table)
        fields = database.get_table_fields(table)
        sales_manager_ids = database.select_sales_manager_ids()  # populates dropdown
        return render_template("houses.j2", name=name, fields=fields, table_data=table_data, sales_manager_ids=sales_manager_ids)

@app.route('/job-workers',methods=['GET', 'POST'])
def job_workers():
    table = 'job_workers'
    name = "Job Workers"
    if request.method == 'POST':
        valid, res_msg = database.insert_into(table, request.form.copy())
        rsp_category = 'success' if valid else 'error'
        flash(res_msg, rsp_category)
        return redirect(request.url)
    if request.method == 'GET':
        table_data = database.select_all(table)
        fields = database.get_table_fields(table)
        job_ids = database.select_job_ids()  # populates dropdown
        worker_ids = database.select_worker_ids()  # populates dropdown
        return render_template("job-workers.j2", name=name, fields=fields, table_data=table_data, job_ids=job_ids, worker_ids=worker_ids)

@app.route('/jobs',methods=['GET', 'POST'])
def jobs():
    table = 'jobs'
    name = "Jobs"
    if request.method == 'POST':
        form_data = request.form.copy()
        form_type = form_data.get('type')
        if form_type == 'delete':
            job_id = form_data.get('id')
            valid, res_msg = database.delete_job(job_id)
            rsp_category = 'success' if valid else 'error'
            flash(res_msg, rsp_category)
        elif form_type == 'insert':
            valid, res_msg = database.insert_into(table, form_data)
            rsp_category = 'success' if valid else 'error'
            flash(res_msg, rsp_category)
        return redirect(request.url)
    if request.method == 'GET':
        table_data = database.select_all(table)
        fields = database.get_table_fields(table)
        house_ids = database.select_house_ids()  # populates dropdown
        return render_template("jobs.j2", name=name, fields=fields, table_data=table_data, house_ids=house_ids)

@app.route('/lawnmowers',methods=['GET', 'POST'])
def lawnmowers():
    table = 'lawnmowers'
    name = "Lawnmowers"
    if request.method == 'POST':
        form_data = request.form.copy()
        form_type = form_data.get('type')
        if form_type == 'update':
            lawnmower_id = form_data.get('id')
            is_functional = form_data.get('is_functional')
            valid, res_msg = database.update_lawnmower_status(lawnmower_id, is_functional)
            rsp_category = 'success' if valid else 'error'
            flash(res_msg, rsp_category)
        elif form_type == 'insert':
            valid, res_msg = database.insert_into(table, form_data)
            rsp_category = 'success' if valid else 'error'
            flash(res_msg, rsp_category)
        return redirect(request.url)
    if request.method == 'GET':
        table_data = database.select_all_lawnmowers()
        fields = database.get_table_fields(table)
        return render_template("lawnmowers.j2", name=name, fields=fields, table_data=table_data)

@app.route('/sales-managers',methods=['GET', 'POST'])
def sales_managers():
    table = 'sales_managers'
    name = "Sales Managers"
    if request.method == 'POST':
        form_data = request.form.copy()
        form_type = form_data.get('type')
        if form_type == 'delete':
            sales_manager_id = request.form.get('id')
            valid, res_msg = database.delete_sales_manager(sales_manager_id)
            rsp_category = 'success' if valid else 'error'
            flash(res_msg, rsp_category)
        elif form_type == 'insert':
            valid, res_msg = database.insert_into(table, form_data)
            rsp_category = 'success' if valid else 'error'
            flash(res_msg, rsp_category)
        return redirect(request.url)
    if request.method == 'GET':
        table_data = database.select_all(table)
        fields = database.get_table_fields(table)
        return render_template("sales-managers.j2", name=name, fields=fields, table_data=table_data)

@app.route('/workers',methods=['GET', 'POST'])
def workers():
    table = 'workers'
    name = "Workers"
    if request.method == 'POST':  # inserting a new entry
        valid, res_msg = database.insert_into(table, request.form.copy())
        rsp_category = 'success' if valid else 'error'
        flash(res_msg, rsp_category)
        return redirect(request.url)
    if request.method == 'GET':  # render the page
        table_data = database.select_all(table)
        fields = database.get_table_fields(table)
        lawnmower_ids = database.select_lawnmower_ids()  # populates dropdown
        return render_template("workers.j2", name=name, fields=fields, table_data=table_data, lawnmower_ids=lawnmower_ids)

# Listener
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 9597))    
    app.run(port=port, debug=True) 
