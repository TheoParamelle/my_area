import os
from dotenv import load_dotenv
from flask import Flask, request, session, url_for, redirect
from pymongo import MongoClient
from authlib.integrations.flask_client import OAuth
from src.login.login import Login
import threading
import json
import time

load_dotenv()

app = Flask(__name__)
app.secret_key = "random secret"
oauth = OAuth(app)

import src.Twitter.routes
import src.Trello.routes
import src.Github.routes
import src.Spotify.routes
from src.Pooling.pooling import lauchPooling

#############################################################
# DB Creationt

client = MongoClient("mongodb://db:27017/area",username="root", password="password", authSource="admin")
db = client.Area

#############################################################
# ROUTE

@app.route('/')
def welcome():
    email = dict(session).get("email", None)
    return (f"Welcome sur notre server back {email} !")

@app.route('/login', methods=['POST'])
def loginVerification():
    print("LoginVerification")
    login = Login()
    if (response := login.verification_login(request, db)):
        info = request.json
        session["username"] = info["username"]
    return (response)

#  Add an AREA

@app.route("/addArea", methods=["POST"])
def addArea():
    info = request.json
    username = session["username"]
    user = db.users.find_one({"username": username})
    if not (user.get("area")):
        db.users.update_one({"username": username}, {"$set": {"area": []}})
    if (db.users.find_one({"username": username, "area": {"$elemMatch" : {"action.service": info["action"]["service"], "action.type": info["action"]["type"]}}})):
        db.users.update_one({"username": username, "area": {"$elemMatch" : {"action.service": info["action"]["service"], "action.type": info["action"]["type"]}}},
        {"$set": {"area.$": info}})
    else:
        db.users.update_one({"username": username}, {"$push": {"area": info}})
    return ({"response": "OK"})

# Add a predone txt
@app.route("/addMessage", methods=["POST"])
def addMessage():
    info = request.json
    username = session["username"]
    service = info["service"] +".messages." + info["type"]
    db.users.update_one({"username": username}, {"$set": {service: info["message"]}})
    return ({"response": "OK"})

@app.route('/db', methods=['GET'])
def todo():
    db.users.insert_one({"name": "Graham", "age": "18"})
    _items = db.users.find()
    items = [item for item in _items]
    return ("yes")

@app.route('/api', methods=['GET'])
def index():
    return {
        "channel": "The show", 
        "tutorial": "React, flask and docker"
    }

@app.route("/about.json")
def about():
    f = open("about.json")
    content = json.load(f)
    # content["client"]["host"] = request.referrer
    # content["server"]["current_time"] = time.time
    return(content)

@app.route("/getArea")
def getArea():

    username = session["username"]
    user = db.users.find_one({"username": username})
    area = user.get("area")
    print(area)
    return ({"response": area})

def main():
    threads = list()

# START SERVER ON THREAD
    server = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=8080, debug=True, use_reloader=False))
    threads.append(server)
    server.start()

# Start Detection boucle
    boucle = threading.Thread(target=lauchPooling)
    threads.append(boucle)
    boucle.start()
# Waiting for everithing finish
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
    # lauchPooling()
    # app.run(host='0.0.0.0', port=8080, debug=True)
