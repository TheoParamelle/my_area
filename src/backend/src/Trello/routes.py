from crypt import methods
import os
from dotenv import load_dotenv
from flask import request, session, redirect
from pymongo import MongoClient
from authlib.integrations.flask_client import OAuth
import requests
from __main__ import app, oauth
from src.Trello.trello import Trello


load_dotenv()

client = MongoClient("mongodb://db:27017/area",username="root", password="password", authSource="admin")
db = client.Area

trello_service = Trello()

@app.route("/login/trello")
def loginTrello():
    return (redirect("https://trello.com/1/authorize?expiration=never&scope=read,write,account&response_type=token&name=Server%20Token&key=15383cd45a97bf73ef9acad8f705ad8e&return_url=http://localhost:8080/authorize/trello"))

@app.route("/authorize/trello")
def getTrelloToken():
    return(
        "<div> <script> fetch('http://localhost:8080/login/trello/token?token=' +  window.location.hash.split('=')[1]) ; window.location.href = 'http://localhost:8081/' </script> You are going to be redirect </div>"
        )

@app.route("/login/trello/token")
def TrelloToken():
    db.users.update_one({"username": session["username"]}, {"$set": {"trello.token": request.args.get("token")}})
    trello_service.setInfo(session["username"])
    return ("void")

@app.route("/trello/addBoardToCheck", methods=["POST"])
def addBoardToCheck():
    username = session["username"]
    info = request.json
    trello_service.setInfo(username)
    trello_service.addBoardToCheck(info)
    return ({"response": "OK"})

@app.route("/trello/addDefaultLabel", methods=["POST"])
def addDefaultLabel():
    username = session["username"]
    info = request.json
    trello_service.setInfo(username)
    resp = trello_service.addDefaultLabelDb(info)
    return({"response": resp})

@app.route("/trello/addRepo", methods=["POST"])
def addRepoToTrello():
    username = session["username"]
    info = request.json
    trello_service.setInfo(username)
    resp = trello_service.addRepo(info)
    return ({"response": resp})

# @app.route("/trello/addCard/<username>", methods=["POST"])
# def test_addCard(username):
#     info = request.json["infoCard"]
#     resp = trello_service.addCard(username, info)
#     return ({"response": resp})

# @app.route("/trello/archiveCard/<username>", methods=["POST"])
# def test_archiveCard(username):
#     info = request.json["infoCard"]
#     resp = trello_service.archiveCard(username, info)
#     return ({"response": resp})

# @app.route("/trello/addList/<username>", methods=["POST"])
# def test_delListe(username):
#     info = request.json["infoCard"]
#     resp = trello_service.addList(username, info)
#     return ({"response": resp})

# @app.route("/trello/archiveList/<username>", methods=["POST"])
# def test_archiveListe(username):
#     info = request.json["infoCard"]
#     resp = trello_service.archiveList(username, info)
#     return ({"response": resp})

# @app.route("/trello/cardChangeList/<username>", methods=["POST"])
# def test_cardChangeList(username):
#     info =  request.json["infoCard"]
#     resp = trello_service.cardChangeList(username, info)
#     return ({"response": resp})
