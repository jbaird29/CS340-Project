from flask import Flask, render_template
import os

# Configuration

app = Flask(__name__)

# Routes 

@app.route('/',methods=['GET'])
def root():
    return render_template("index.j2")

@app.route('/customer-contacts',methods=['GET'])
def customerContacts():
    return render_template("customer-contacts.j2")

@app.route('/houses',methods=['GET'])
def houses():
    return render_template("houses.j2")

@app.route('/job-workers',methods=['GET'])
def jobWorkers():
    return render_template("job-workers.j2")

@app.route('/jobs',methods=['GET'])
def jobs():
    return render_template("jobs.j2")

@app.route('/lawnmowers',methods=['GET'])
def lawnmowers():
    return render_template("lawnmowers.j2")

@app.route('/sales-managers',methods=['GET'])
def salesManagers():
    return render_template("sales-managers.j2")

@app.route('/workers',methods=['GET'])
def workers():
    return render_template("workers.j2")


# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 7513))    
    app.run(port=port, debug=True) 
