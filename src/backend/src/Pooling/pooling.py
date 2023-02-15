import os
import threading
from pymongo import MongoClient
from dotenv import load_dotenv
import tweepy


load_dotenv()

client = MongoClient("mongodb://db:27017/area",username="root", password="password", authSource="admin")
db = client.Area


from src.Twitter.twitter import Twitter
from src.Github.github import GithubService
from src.Trello.trello import Trello
from src.Spotify.spotify  import Spotify

class Area():
    def __init__(self) -> None:
        self.action = None

    def doActions(self, user):
        twitter = Twitter(username=user["username"])
        github = GithubService(username=user["username"])
        trello = Trello(username=user["username"])
        spotify = Spotify(username=user["username"])
        services = {"trello" : trello, "github": github, "spotify": spotify, "twitter": twitter}
        reactions = list()
        print(user["username"])
        area = user.get("area")
        for elem in area:
            for key, value in services.items():
                if (elem["action"]["service"] == key and value.good == True):
                    reactions.append(value.pullEvent(elem))
                    # break
        for elem in reactions:
            if elem != None:
                for service in elem["area"]["reaction"]:
                    value = services[service["service"]]
                    if value.good:
                        value.pushEvent(elem)
 
    def lauchActions(self):
        Threads = list()
        users = db.users.find()
        # Changer les boucle ici car on pers des user, le 'for' n'es pas bon
        for user in users:
            if (user.get("area") and len(user["area"]) > 0 and (len(Threads) <= 20)):
                x = threading.Thread(target=self.doActions(user))
                Threads.append(x)
                x.start()
        for thread in Threads:
            thread.join()
        print("fin Du Fetch")

def lauchPooling():
    # changer l'endroit de l'instance area
    print("pooling")
    area = Area()
    threading.Timer(20, lauchPooling).start()
    area.lauchActions()

