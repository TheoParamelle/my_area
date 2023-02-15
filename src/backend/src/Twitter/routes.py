from __main__ import app, oauth
import os
from dotenv import load_dotenv
from flask import request, session, url_for, redirect
from pymongo import MongoClient
from src.Twitter.twitter import Twitter

load_dotenv()

client = MongoClient("mongodb://db:27017/area",username="root", password="password", authSource="admin")
db = client.Area

twitter = oauth.register(
    name='twitter',
    client_id=os.getenv("TWITTER_API_ID"),
    client_secret=os.getenv("TWITTER_API_SECRET"),
    request_token_url='https://api.twitter.com/oauth/request_token',
    request_token_params=None,
    access_token_url='https://api.twitter.com/oauth/access_token',
    access_token_params=None,
    authorize_url='https://api.twitter.com/oauth/authenticate',
    authorize_params="",
    api_base_url='https://api.twitter.com/1.1/',
    client_kwargs={"scope": "openid profile email"},
)
twitter_service = Twitter()

# -- Twitter ---

@app.route('/login/twitter/')
def loginTwitter():
    print("Twitter log")
    twitter = oauth.create_client("twitter")
    redirect_uri = url_for('authorizeTwitter', _external=True)
    return twitter.authorize_redirect(redirect_uri)

@app.route('/authorize/twitter/')
def authorizeTwitter():
    twitter = oauth.create_client("twitter")
    token = twitter.authorize_access_token()
    db.users.update_one({"username": session["username"]}, {"$set": {"twitter.token": token}})
    db.users.update_one({"username": session["username"]}, {"$set": {"twitter.info": {}}})
    twitter_service.setInfo(session["username"])
    twitter_service.putInfoToDB()
    return redirect('http://localhost:8081/')

@app.route("/twitter/addIdole", methods=["POST"])
def addIdole():
    username = session["username"]
    info = request.json
    twitter_service.setInfo(username)
    if not (twitter_service.putIdoleInfo(info["idole"])):
        return ({"response": "KO"})
    return ({"response": "OK"})

#  -- Twitter post
# @app.route("/twitter/post/<username>", methods=["POST"])
# def post_twitter(username):
#     message = request.json["message"]
#     resp = twitter_service.add_post(username, message)
#     return ({"response": resp})

# @app.route("/twitter/retweet/<username>", methods=["POST"])
# def retweet_twitter(username):
#     id_tweet = request.json["id_tweet"]
#     resp = twitter_service.retweet(username, id_tweet)
#     return ({"response": resp})

# @app.route("/twitter/followBack/<username>", methods=["POST"])
# def follow_back(username):
#     id_profile = request.json["id_profile"]
#     resp = twitter_service.follow(username, user_id=id_profile)
#     return ({"response": resp})

# @app.route("/twitter/sendMsg/<username>", methods=["POST"])
# def send_msg(username):
#     text = request.json["text"]
#     user_id = request.json["user_id"]
#     resp = twitter_service.send_dm(username, user_id, text)
#     return ({"response": resp})
