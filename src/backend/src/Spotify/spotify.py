import os
import spotipy
from pymongo import MongoClient
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import time
import json
load_dotenv()

client = MongoClient("mongodb://db:27017/area",username="root", password="password", authSource="admin")
db = client.Area

class Spotify():
    
    def __init__(self, username=None) -> None:
        self.username = None
        self.client = None
        self.access_token = None
        self.dbUser = None
        self.auth = SpotifyOAuth(scope="playlist-modify-public playlist-modify-private user-library-read user-library-modify user-modify-playback-state user-follow-modify user-follow-read", client_id=os.getenv('SPOTIFY_CLIENT_ID'), client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'), redirect_uri=os.getenv('SPOTIPY_REDIRECT_URI'))
        self.area = None
        self.good = False
        if (username):
            self.setInfo(username)

    def setInfo(self, username):
        self.username = username
        self.dbUser = db.users.find_one({"username": username})
        if not (spotiInfo := self.dbUser.get("spotify")):
            return ("Error: No spotify")
        spotiInfo = spotiInfo["token"]
        self.access_token = spotiInfo["access_token"]
        self.client = spotipy.Spotify(auth=self.access_token , auth_manager=self.auth)  
        self.userId = self.client.me()["id"]
        self.good = True

    def getAlbums(self):
        offset = 0
        response = self.client.current_user_saved_albums(limit=50)
        albums = response["items"]
        lenAlbums = len(response["items"])
        while lenAlbums == 50:
            offset += lenAlbums
            response = self.client.current_user_saved_albums(limit=50, offset=offset)
            albums.extend(response["items"])
            lenAlbums = len(response["items"])
        albumIds = [album["album"]["id"] for album in albums]
        return (albumIds)

    def getAlbumsFromArtist(self, artistId):
        albums = self.client.artist_albums(artist_id=artistId)
        albumsIds = [elem["id"] for elem in albums["items"]]
        return (albumsIds)
    

    def getArtists(self):
        response = self.client.current_user_followed_artists(limit=50)
        artists = response["artists"]["items"]
        lenArtiste = len(response["artists"]["items"])
        while lenArtiste == 50:
            after = response["artists"]["cursors"]["after"]
            response = self.client.current_user_followed_artists(limit=50, after=after)
            artists.extend(response["artists"]["items"])
            lenArtiste = len(response["artists"]["items"])
        artistIds = [artist["id"] for artist in artists]
        artists = []
        for id_ in artistIds:
            albumsIds = self.getAlbumsFromArtist(id_)
            info = {"id": id_, "albums": albumsIds}
            artists.append(info)
        return (artists)

    def getSavedSong(self):
        offset = 0
        response = self.client.current_user_saved_tracks(limit=50)
        songs = [elem["track"]["id"] for elem in response["items"]]
        lenResponse = len(response["items"])
        while lenResponse == 50:
            offset += 50
            response = self.client.current_user_saved_tracks(limit=50, offset=offset)
            songs.extend([elem["track"]["id"] for elem in response["items"]])
            lenResponse = len(response["items"])
            time.sleep(0.01)
        return (songs)

    def getPlaylists(self):
        offset = 0
        response = self.client.current_user_playlists(limit=50)
        playlists = response["items"]
        lenResponse = len(response["items"])
        while lenResponse == 50:
            offset += 50
            response = self.client.current_user_playlists(limit=50, offset=offset)
            playlists.extend(response["items"])
            lenResponse = response["items"]
            time.sleep(0.01)
        return (playlists)

    def putInfoToDb(self):
        # RECUP LES ARTISTE LIKER
        artistsInfo = self.getArtists()
        db.users.update_one({"username": self.username}, {"$set": {"spotify.info.artists": artistsInfo}})

        #RECUP LES ALBUM LIKER => pas utiliser
        # albumIds = self.getAlbums()
        # db.users.update_one({"username": self.username}, {"$set": {"spotify.info.albums": albumIds}})
        
        # RECUP LES TRACKS LIKER
        savedTracksId = self.getSavedSong()
        db.users.update_one({"username": self.username}, {"$set": {"spotify.info.savedTracks": savedTracksId}})
        
        # RECUP LES PLAYLIST CREE
        playlists = self.getPlaylists()
        playlistsId = [playlist["id"] for playlist in playlists]
        db.users.update_one({"username": self.username}, {"$set": {"spotify.info.playlists": playlistsId}})
        return ("OK")

# ---------------PUSH EVENT ----------------------------------

    def saveAlbum(self, info):
        print("saveAlbum")
        if (self.area["action"]["type"] == "newArtistAlbum"):
            self.client.current_user_saved_albums_add(info["newAlbums"])
    
    def nextTrack(self, info):
        if (self.area["action"]["type"] == "newCard" and info["modList"]):
            self.client.next_track()
        return

    def getTracksInfo(self, tracks):
        tracksInfo = []
        for track in tracks["tracks"]:
            info = {}
            genres = []
            artistsId = [artist["id"] for artist in track["album"]["artists"]]
            artists = self.client.artists(artistsId)
            for artist in artists["artists"]:
                genres.extend(artist["genres"])
            info["id"] = track["id"]
            info["genre"] = genres[0] if genres else "Autres"
            tracksInfo.append(info)
        return (tracksInfo)

    def getPlaylistInfo(self):
        playlistsInfo = []
        playlists = self.getPlaylists()
        for playlist in playlists:
            info = {}
            info["id"] = playlist["id"]
            info["name"] = playlist["name"]
            info["public"] = playlist["public"]
            playlistsInfo.append(info)
        return (playlistsInfo)

    def newSavedTrack(self, info):
        tracks = self.client.tracks(info["newTracks"])
        tracksInfo = self.getTracksInfo(tracks)
        playlistInfo = self.getPlaylistInfo()
        for track in tracksInfo:
            genre = track["genre"]
            cond = 0
            for playlist in playlistInfo:
                if genre == playlist["name"]:
                    cond = 1
                    self.client.playlist_add_items(playlist["id"], [track["id"]], position=0)
                    break
            if cond == 0:
                newPlaylist = self.client.user_playlist_create(user=self.userId, name=genre)
                self.client.playlist_add_items(newPlaylist["id"], [track["id"]], position=0)
                playlistInfo = self.getPlaylistInfo()
        return

    def pushEvent(self, info):
        self.dbUser = db.users.find_one({"username": self.username})
        self.area = info["area"]
        for service in self.area["reaction"]:
            if service["service"] == "spotify":
                for type_ in service["type"]:
                    if (type_ == "saveAlbum"):
                        self.saveAlbum(info)
                    if (type_ == "nextTrack"):
                        self.nextTrack(info)
                    if (type_ == "newSavedTrack"):
                        self.newSavedTrack(info)
                return
        return

# ---------------PULL EVENT ----------------------------------

    def checkNewAlbumOfArtist(self):
        newAlbums = []
        for artist in self.dbUser["spotify"]["info"]["artists"]:
            cond = 0
            oldAlbums = artist["albums"]
            albums = self.getAlbumsFromArtist(artist["id"])
            for album in albums:
                if album not in oldAlbums:
                    cond = 1
                    newAlbums.append(album)
            if cond == 1:
                db.users.update_one({"username": self.username, "spotify.info.artists": {"$elemMatch": {"id": artist["id"]}}}, 
                    {"$set": {"spotify.info.artists.$.albums": albums}})
        if (newAlbums):
            return ({"area": self.area, "newAlbums": newAlbums})
        return None

    def checkNewSavedTrack(self):
        oldTracks = self.dbUser["spotify"]["info"]["savedTracks"]
        rTracks = self.getSavedSong()
        newTracks = set(rTracks) - set(oldTracks)
        db.users.update_one({"username": self.username}, {"$set": {"spotify.info.savedTracks": rTracks}})
        if newTracks:
            return ({"area": self.area, "newTracks": newTracks})
        return (None)
    
    def checkNewPlaylists(self):
        newPlaylists = []
        oldPlaylists = self.dbUser["spotify"]["info"]["playlists"]
        rPlaylists = self.getPlaylists()
        playlistIds = [elem["id"] for elem in rPlaylists]
        db.users.update_one({"username": self.username}, {"$set": {"spotify.info.playlists": playlistIds}})
        newPlaylistsIds = set(rPlaylists) - set(oldPlaylists)
        if newPlaylistsIds:
            for id_ in newPlaylistsIds:
                playlist = self.client.playlist(playlist_id=id_)
                link = playlist["external_urls"]["spotify"]
                newPlaylists.append({"id": id_, "link": link})
            return ({"area": self.area, "newPlaylists": newPlaylists})
        return (None)

    def pullEvent(self, area):
        self.area = area
        if (self.area["action"]["type"] == "newArtistAlbum"):
            return (self.checkNewAlbumOfArtist())
        if (self.area["action"]["type"] == "newSavedTrack"):
            return(self.checkNewSavedTrack())
        if (self.area["action"]["type"] == "newPlaylist"):
            return(self.checkNewPlaylists())
