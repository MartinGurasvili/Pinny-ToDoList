from flask import Flask, render_template, session, redirect,request, make_response
from functools import wraps
import os
import pymongo
import random
import ssl

app = Flask(__name__)
passw = "8Uxpz8VOXG9gmLMF"
key = "mongodb+srv://web:{}@testrig.wpw1fku.mongodb.net/?retryWrites=true&w=majority".format(passw)
# passw = "jondi1-ryqtix-cAzhok"
# key = "mongodb+srv://Martingur:{}@cluster0.vjrer4s.mongodb.net/?retryWrites=true&w=majority".format(passw)
# Database
client = pymongo.MongoClient(key,connectTimeoutMS=30000, socketTimeoutMS=None, connect=False, maxPoolsize=1)
maindb = client.user_login_system
db = maindb.user_login_system
folders = maindb.user_notes

def idgen():
    num = random.randint(10000,99999)
    while (db.find_one({'id': num})):
        num = random.randint(10000,99999)
    return num

@app.route('/<path:path>')
def catch_all(path):
    print(path)
    if path.startswith('/?email='):
        return redirect('/app/')

@app.route('/', methods=['GET', 'POST'])
def home():
  global db
  print(request.path)

  if request.method == 'POST':
            passw = "8Uxpz8VOXG9gmLMF"
            key = "mongodb+srv://web:{}@testrig.wpw1fku.mongodb.net/?retryWrites=true&w=majority".format(passw)
            # passw = "jondi1-ryqtix-cAzhok"
            # key = "mongodb+srv://Martingur:{}@cluster0.vjrer4s.mongodb.net/?retryWrites=true&w=majority".format(passw)
            # passw = "jondi1-ryqtix-cAzhok"

            # key = "mongodb://martingur:{}@testrig.wpw1fku.mongodb.net/?retryWrites=true&w=majority".format(passw)
            # Database
            client = pymongo.MongoClient(key,connectTimeoutMS=30000, socketTimeoutMS=None, connect=False, maxPoolsize=1)
            maindb = client.user_login_system
            db = maindb.user_login_system
            if request.form['tip'] == "create":
                print("CREATE ACCOUNT")
                email = request.form['email']
                name = request.form['name']
                id = idgen()
                password = request.form['password']
                existing_user = db.find_one({'email': email})
                if existing_user:
                    return redirect('/error/')
                else:
                    print("correct")
                    db.insert_one({'id':str(id),'email': email,'name':name, 'password': password})
                    resp = make_response(redirect('/app/'))
                    resp.set_cookie('idd', str(id))
                    resp.set_cookie('name', name)
                    resp.set_cookie('email', email)
                    return resp


            elif request.form['tip'] == "login":
                print("Login")

                email = request.form['email']
                print(email)
                password = request.form['password']
                print(password)
                user = db.find_one({'email': email, 'password': password})
                print(user)
                if not user:
                    return redirect('/error/')
                else:
                    print("correct")
                    resp = make_response(redirect('/app/'))
                    print(user['id'])
                    resp.set_cookie('idd', str(user['id']))
                    resp.set_cookie('name', user['name'])
                    resp.set_cookie('email', user['email'])

                    return resp

            else:
                return redirect('/app/')

  else:
      name = request.cookies.get('name')
      # Render the index template

      if name or request.args:
            if db.find_one({'email': request.args.get('email'), 'password': request.args.get('password')}):
                return redirect('/app/')
            else:
                return redirect('/error/')

      else:
        return render_template('base.html')



@app.route('/app/', methods=['GET', 'POST'])
def appp():
    global folders
    if request.method == 'POST':
        if request.form['tip'] == "getNames":
            id = request.form['id']

            documents = folders.find({'id': id})
            document_names = [doc['name'] for doc in documents]
            document_names = ",".join(document_names)
            return document_names

        if request.form['tip'] == "rename":
            id = request.form['id']
            print(id)
            last = request.form['lastname']
            print(last)
            new = request.form['newname']
            print(new)
            elements = folders.find_one({'id':str(id),'name': last})["elements"]
            folders.delete_one({'id':str(id),'name': last})
            folders.find_one_and_update({'id':str(id),'name': new},{"$set": {'elements': elements}} ,upsert=True)
            return new
        if request.form['tip'] == "saveF":
            id = request.form['id']
            print(id)
            name = request.form['name']
            print(name)
            elements = request.form['el']
            print(elements)
            if elements == "":
                folders.delete_one({'id':str(id),'name': name})
            else:
                folders.find_one_and_update({'id':str(id),'name': name},{"$set": {'elements': elements}} ,upsert=True)
            return('', 204)
        if request.form['tip'] == "loadF":
            id = request.form['id']
            name = request.form['name']
            print(id)
            print(name)
            content = folders.find_one({'id':str(id),'name': name})
            if content:
                return content["elements"]
            else:
                return ('', 204)

    else:
        return render_template('app.html')



@app.route('/error/')
def erro():
  return render_template('incorrectpass.html')



