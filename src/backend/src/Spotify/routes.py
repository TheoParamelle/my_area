from __main__ import app, oauth
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from flask import request, session, url_for, redirect
import spotipy
from spotipy.oauth2 import SpotifyOAuth

from src.Spotify.spotify import Spotify

load_dotenv()

# DB CONNECTION
client = MongoClient("mongodb://db:27017/area",username="root", password="password", authSource="admin")
db = client.Area

spotify_service = Spotify()

spotify_auth = SpotifyOAuth(
    scope="playlist-modify-public playlist-modify-private user-library-read user-library-modify user-modify-playback-state user-follow-modify user-follow-read",
    client_id=os.getenv('SPOTIFY_CLIENT_ID'),
    client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
    redirect_uri=os.getenv('SPOTIPY_REDIRECT_URI'))
    # ajout dans la db


@app.route("/login/spotify")
def loginSpotify():
    print("login spot")
    return(redirect(spotify_auth.get_authorize_url()))

@app.route("/authorize/spotify")
def authSpotify():
    print("auth")
    code = request.args["code"]
    token = spotify_auth.get_access_token(code)
    db.users.update_one({"username": session["username"]}, {"$set": {"spotify.token": token}})
    spotify_service.setInfo(session["username"])
    spotify_service.putInfoToDb()
    return (redirect("http://localhost:8081/Dashboard"))
