from flask import Flask, render_template, redirect, request, flash, url_for, json
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
db = LennysDB(mysql)

# Routes 
@app.route('/',methods=['GET'])
def root():
    return render_template("index.j2")

@app.route('/500',methods=['GET'])
def server_err():
    return render_template("500-error.j2") 

@app.route('/customer-contacts',methods=['GET', 'POST'])
def customer_contacts():
    if request.method == 'POST':
        valid, res_msg = db.customer_contacts.insert_into(request.form.copy())
        rsp_category = 'success' if valid else 'error'
        flash(res_msg, rsp_category)
        return redirect(url_for('customer_contacts'))
    if request.method == 'GET':
        # first and last name query params are used for the "Search" functionality
        first_name = request.args.get('first_name')
        last_name = request.args.get('last_name')
        # if no query params, show all data; otherwise, filter data based on the inputs
        if not first_name and not last_name:
            table_data = db.customer_contacts.select_all()
        else:
            table_data = db.customer_contacts.search(first_name, last_name)
        name = db.customer_contacts.get_title()
        fields = db.customer_contacts.get_field_titles()
        house_ids = db.houses.select_ids()  # populates dropdown
        return render_template("customer-contacts.j2", name=name, fields=fields, table_data=table_data, house_ids=house_ids)

@app.route('/houses',methods=['GET', 'POST'])
def houses():
    if request.method == 'POST':
        form_data = request.form.copy()
        form_type = form_data.get('type')
        if form_type == 'update':
            house_id = form_data.get('id')
            sales_manager_id = form_data.get('sales_manager_id')
            valid, res_msg = db.houses.update_sales_manager(house_id, sales_manager_id)
            rsp_category = 'success' if valid else 'error'
            flash(res_msg, rsp_category)
        elif form_type == 'insert':
            valid, res_msg = db.houses.insert_into(form_data)
            rsp_category = 'success' if valid else 'error'
            flash(res_msg, rsp_category)
        return redirect(url_for('houses'))
    if request.method == 'GET':
        name = db.houses.get_title()
        table_data = db.houses.select_all()
        fields = db.houses.get_field_titles()
        sales_manager_ids = db.sales_managers.select_ids()  # populates dropdown
        return render_template("houses.j2", name=name, fields=fields, table_data=table_data, sales_manager_ids=sales_manager_ids)

@app.route('/job-workers',methods=['GET', 'POST'])
def job_workers():
    if request.method == 'POST':
        form_data = request.form.copy()
        form_type = form_data.get('type')
        if form_type == 'delete':
            job_id = request.form.get('job_id')
            worker_id = request.form.get('worker_id')
            valid, res_msg = db.job_workers.delete(job_id, worker_id)
            rsp_category = 'success' if valid else 'error'
            flash(res_msg, rsp_category)
        elif form_type == 'update':
            old_job_id = request.form.get('old_job_id')
            old_worker_id = request.form.get('old_worker_id')
            new_worker_id = request.form.get('new_worker_id')
            new_job_id = request.form.get('new_job_id')
            valid, res_msg = db.job_workers.update(old_job_id, old_worker_id, new_worker_id, new_job_id)
            rsp_category = 'success' if valid else 'error'
            flash(res_msg, rsp_category)
        elif form_type == 'insert':
            valid, res_msg = db.job_workers.insert_into(form_data)
            rsp_category = 'success' if valid else 'error'
            flash(res_msg, rsp_category)
        return redirect(url_for('job_workers'))
    if request.method == 'GET':
        name = db.job_workers.get_title()
        table_data = db.job_workers.select_all()
        fields = db.job_workers.get_field_titles()
        job_ids = db.jobs.select_ids()  # populates dropdown
        worker_ids = db.workers.select_ids()  # populates dropdown
        return render_template("job-workers.j2", name=name, fields=fields, table_data=table_data, job_ids=job_ids, worker_ids=worker_ids)

@app.route('/jobs',methods=['GET', 'POST'])
def jobs():
    if request.method == 'POST':
        form_data = request.form.copy()
        form_type = form_data.get('type')
        if form_type == 'delete':
            job_id = form_data.get('id')
            valid, res_msg = db.jobs.delete(job_id)
            rsp_category = 'success' if valid else 'error'
            flash(res_msg, rsp_category)
        elif form_type == 'insert':
            valid, res_msg = db.jobs.insert_into(form_data)
            rsp_category = 'success' if valid else 'error'
            flash(res_msg, rsp_category)
        return redirect(url_for('jobs'))
    if request.method == 'GET':
        name = db.jobs.get_title()
        table_data = db.jobs.select_all()
        fields = db.jobs.get_field_titles()
        house_ids = db.houses.select_ids()  # populates dropdown
        return render_template("jobs.j2", name=name, fields=fields, table_data=table_data, house_ids=house_ids)

@app.route('/lawnmowers',methods=['GET', 'POST'])
def lawnmowers():
    if request.method == 'POST':
        form_data = request.form.copy()
        form_type = form_data.get('type')
        if form_type == 'update':
            lawnmower_id = form_data.get('id')
            is_functional = form_data.get('is_functional')
            valid, res_msg = db.lawnmowers.update_status(lawnmower_id, is_functional)
            rsp_category = 'success' if valid else 'error'
            flash(res_msg, rsp_category)
        elif form_type == 'insert':
            valid, res_msg = db.lawnmowers.insert_into(form_data)
            rsp_category = 'success' if valid else 'error'
            flash(res_msg, rsp_category)
        return redirect(url_for('lawnmowers'))
    if request.method == 'GET':
        name = db.lawnmowers.get_title()
        table_data = db.lawnmowers.select_all()
        fields = db.lawnmowers.get_field_titles()
        return render_template("lawnmowers.j2", name=name, fields=fields, table_data=table_data)

@app.route('/sales-managers',methods=['GET', 'POST'])
def sales_managers():
    if request.method == 'POST':
        form_data = request.form.copy()
        form_type = form_data.get('type')
        if form_type == 'delete':
            sales_manager_id = request.form.get('id')
            valid, res_msg = db.sales_managers.delete(sales_manager_id)
            rsp_category = 'success' if valid else 'error'
            flash(res_msg, rsp_category)
        elif form_type == 'insert':
            valid, res_msg = db.sales_managers.insert_into(form_data)
            rsp_category = 'success' if valid else 'error'
            flash(res_msg, rsp_category)
        return redirect(url_for('sales_managers'))
    if request.method == 'GET':
        name = db.sales_managers.get_title()
        table_data = db.sales_managers.select_all()
        fields = db.sales_managers.get_field_titles()
        return render_template("sales-managers.j2", name=name, fields=fields, table_data=table_data)

@app.route('/workers',methods=['GET', 'POST'])
def workers():
    if request.method == 'POST':  # inserting a new entry
        valid, res_msg = db.workers.insert_into(request.form.copy())
        rsp_category = 'success' if valid else 'error'
        flash(res_msg, rsp_category)
        return redirect(url_for('workers'))
    if request.method == 'GET':  # render the page
        name = db.workers.get_title()
        table_data = db.workers.select_all()
        fields = db.workers.get_field_titles()
        lawnmower_ids = db.lawnmowers.select_ids()  # used to populate drop down
        return render_template("workers.j2", name=name, fields=fields, table_data=table_data, lawnmower_ids=lawnmower_ids)

# Listener
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 9597))    
    app.run(port=port, debug=True) 
