import requests
import flask
from flask import request, render_template,session,redirect,url_for
from flask_cors import CORS
from ibm_db import connect
from ibm_db import fetch_assoc
from ibm_db import exec_immediate
from ibm_db import tables

import os


response=flask.Response()




app = flask.Flask(__name__, static_url_path='')
CORS(app)
app.secret_key=os.urandom(12)


    
#  try:
print("Connecting")
con=connect("DATABASE=bludb;HOSTNAME=fbd88901-ebdb-4a4f-a32e-9822b9fb237b.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32731;PROTOCOL=TCPIP;UID=snd70328;PWD=D2qdivZLjZ9qxlMC;SECURITY=SSL","","")
# except:
    # print("Unable to connect")

def results(command):

    ret = []
    result = fetch_assoc(command)
    while result:
        ret.append(result)
        result = fetch_assoc(command)
    return ret

@app.route('/', methods=['GET'])
def sendHomePage():
    return render_template('index.html')


@app.route('/register',methods=['GET','POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        sql1="select username from user1 where email='"+email+"'"
        #try:
        rows = results(exec_immediate(con, sql1))
        if rows:
            return render_template('index.html',msg="Email Already Registered")
        else:
            sql2="insert into user1(username,email,password) values('"+username+"','"+email+"','"+password+"')"
                
            exec_immediate(con,sql2)
            return render_template('login.html')
        # except:
        # print("Failed")
    return render_template('index.html')


@app.route('/gotologin',methods=['GET','POST'])
def gotologin():
    return render_template('login.html')

@app.route('/login',methods=['GET','POST'])
def login():
    msg = ''
    
    if request.method == 'POST' and  'password' in request.form and 'email' in request.form:
        
        password = request.form['password']
        email = request.form['email']
        sql1="select * from user1 where email='"+email+"' and password='"+password+"'"
        try:
            rows = results(exec_immediate(con, sql1))
            print(rows[0]['USERNAME'])
            if rows:
                ##login_user(rows[0]['UID'])
                session['uid']=email
                session['uname']=str(rows[0]['USERNAME'])
                return redirect('/home')
            
            else:
                return render_template('login.html',msg='Email or Password is Incorrect')
        except:
            print("Failed")
        
        print('uid' in session)
    elif 'uid' not in session:
        return render_template("login.html")
        
    return render_template('login.html')


@app.route('/home')
def home():
    if 'uid' in session:
        return render_template('dataform.html',msg=session['uname'])
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('uid',None)
    print('uid' in session)
    return redirect(url_for('login'))

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response


        

if __name__ == '__main__' :
    app.run(debug= False)
