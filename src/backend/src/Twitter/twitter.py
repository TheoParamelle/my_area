import os
from pymongo import MongoClient
from dotenv import load_dotenv
import tweepy

load_dotenv()

client = MongoClient("mongodb://db:27017/area",username="root", password="password", authSource="admin")
db = client.Area


class Twitter():
    
    def __init__(self, username=None) -> None:
        self.auth = tweepy.OAuthHandler(os.getenv("TWITTER_API_ID"), os.getenv("TWITTER_API_SECRET"))
        self.username = None
        self.api = None
        self.access_token = None
        self.access_token_secret = None
        self.area = None
        self.dbUser = None
        self.good = False
        if (username):
            self.setInfo(username)

    def setInfo(self, username):
        self.username = username
        self.dbUser = db.users.find_one({"username": username})
        if not (twitter_info := self.dbUser.get("twitter")):
            return ("Not tweeter info, add your twitter account to continue")
        twitter_info = twitter_info["token"]
        self.access_token = twitter_info["oauth_token"]
        self.access_token_secret = twitter_info["oauth_token_secret"]
        self.auth.set_access_token(self.access_token, self.access_token_secret)
        self.api = tweepy.API(self.auth, wait_on_rate_limit=False)
        self.good = True

    def putInfoToDB(self):
        #Put followers
        followers = self.api.get_followers()
        followers_name = [follower.screen_name for follower in followers]
        db.users.update_one({"username": self.username}, {"$set": {"twitter.info.followers": followers_name}})

        # Put last message receve
        lastmessages = self.api.get_direct_messages(count=10)
        for msg in lastmessages:
            if (msg.message_create["sender_id"] != self.dbUser["twitter"]["token"]["user_id"]):
                db.users.update_one({"username": self.username}, {"$set": {"twitter.info.dm": msg.id}})
                return ()

    def putIdoleInfo(self, screen_name):
        try:
            tweets = self.api.user_timeline(screen_name=screen_name, include_rts=False)
            info = {}
            info["name"] = screen_name
            info["tweet_ids"] = [tweet.id for tweet in tweets]
            db.users.update_one({"username": self.username}, {"$push": {"twitter.info.idoles": info}})
            return (True)
        except Exception as e:
            print(e)
            return (False)

    def add_post(self, message=None):
        print("Add POST")
        try:
            self.api.update_status(message)
            return ("OK")
        except Exception as e:
            print(e)
        return("KO")

    def retweet(self, tweet_id=None):
        print("Retweet")
        try:
            self.api.retweet(tweet_id)
            print(f"Retweet success {tweet_id}")
            return ("OK")
        except Exception as e:
            print(e)
        return ("KO")
    
    def like(self, tweet_id=None):
        print("like a tweet")
        try:
            self.api.create_favorite(id=tweet_id)
        except Exception as e:
            print(e)
            return ("KO")

    def follow(self,user_id=None, screen_name=None):
        print("Follow")
        try:
            if (user_id):
                self.api.create_friendship(user_id=user_id)
                print(f"Friendship create with success !")
                return ("OK")
            elif (screen_name):
                self.api.create_friendship(screen_name=screen_name)
                print(f"Friendship create with success !")
                return ("OK")
        except Exception as e:
            print(e)
        return ("KO")

    def send_dm(self,user_id, text):
        try:
            self.api.send_direct_message(recipient_id=user_id, text=text)
            print(f"DM send with success !")
            return ("OK")
        except Exception as e:
            print(e)
            return("KO")

# ------------Push event ------

    def followBack(self, info):
        for elem in info["users_screen_name"]:
            self.follow(screen_name=elem)

    def post(self, info):
        if self.area["action"]["type"] == "follow":
            message = self.dbUser["twitter"]["messages"]["follow"]
            topost = message
            for elem in info["users_screen_name"]:
                topost += " @" + elem
            return(self.add_post(message=topost))
        if self.area["action"]["service"] == "spotify":
            self.fromSpotify(info)

    def retweetIdoles(self, info):
        if (self.area["action"]["type"] == "idolesTweets"):
            print("je vais retweet tout les tweet de mes idoles")
            for tweet_id in info["tweet_ids"]:
                self.retweet(tweet_id=tweet_id)
            return ({"response": "OK"})

    def likeIdoles(self, info):
        if (self.area["action"]["type"] == "idolesTweets"):
            print("je vais love les tweet de mes idoles")
            for tweet_id in info["tweet_ids"]:
                self.like(tweet_id=tweet_id)
            return ({"response": "OK"})

    def markRead(self, info):
        print("makrRead")
        if (self.area["action"]["type"] == "dm"):
            self.api.mark_direct_message_read(last_read_event_id=info["dm"], recipient_id=info["sender_id"])
            return ("OK")

    def fromTrello(self, info):
        # NOUVELLE CARTE
        if self.area["action"]["type"] == "newCard":
            for card in info["newCardsIds"]: 
                message = "Une nouvelle carte a ete ajoute sur trello : '" + card["name"]+"'."
                self.send_dm(user_id=self.dbUser["twitter"]["token"]["user_id"], text=message)
            for card in info["modList"]:
                message = "La carte '" + card + "' a changer de liste."
                self.send_dm(user_id=self.dbUser["twitter"]["token"]["user_id"], text=message)
            for card in info["modLabel"]:
                message = "La carte '" + card + "' a changer de label."
                self.send_dm(user_id=self.dbUser["twitter"]["token"]["user_id"], text=message)

        # NOUVELLE LISTE
        elif self.area["action"]["type"] == "newList":
            for liste in info["listNames"]:
                message = "Une nouvelle liste a ete ajouter au trello : '" + liste["name"] + "'."
                self.send_dm(user_id=self.dbUser["twitter"]["token"]["user_id"], text=message)
        # Archived list
        elif self.area["action"]["type"] == "archivedList":
            for liste in info["lists"]:
                message = "La liste '" + liste["listName"] +"' a ete archive !"
                self.send_dm(user_id=self.dbUser["twitter"]["token"]["user_id"], text=message)
        # NOUVEAU LABEL
        elif self.area["action"]["type"] == "newLabel":
            for label in info["labelNames"]:
                message = "Un nouveau label a ete ajouter au trello : '" + label["name"]+ "'."
                self.send_dm(user_id=self.dbUser["twitter"]["token"]["user_id"], text=message)

    def fromGithub(self, info):
        # NOUVELLE ISSUE
        if self.area["action"]["type"] == "newIssue":
            for issue in info["newIssues"]:
                messages = "Une nouvelle issue a ete cree sur '" + issue["repoName"]+"': '"+ issue["title"] +"'."
                self.send_dm(user_id=self.dbUser["twitter"]["token"]["user_id"], text=messages)

        # NOUVELLE BRANCHE
        if self.area["action"]["type"] == "newBranch":
            for branch in info["newBranches"]:
                messages = "Une nouvelle branch a ete cree sur '" + branch["repoName"] + "': '" + branch["name"] + "'."
                self.send_dm(user_id=self.dbUser["twitter"]["token"]["user_id"], text=messages)

        # NOUVELLE PULL REQUEST
        if self.area["action"]["type"] == "newPull":
            for pull in info["newPulls"]:
                messages = "Une nouvelle MergeRequest a ete cree sur '" + pull["repoName"] + "': '" + pull["title"] + "'."
                self.send_dm(user_id=self.dbUser["twitter"]["token"]["user_id"], text=messages)
        return

    def fromSpotify(self, info):
        # TODO a tester (les deux)
        if self.area["action"]["type"] == "newArtistAlbum":
            message = "Une de tes artistes prefere viens de sortir un nouvelle album !"
            self.send_dm(user_id=self.dbUser["twitter"]["token"]["user_id"], text=message)
        if self.area["action"]["type"] == "newPlaylist":
            for elem in info["newPlaylists"]:
                message = "Allez checker ma nouvelle playlist sur spotify !" + elem["link"]
                self.add_post(message=message)

    def sendDm(self, info):
        if (self.area["action"]["type"] == "dm"):
            return(self.send_dm(user_id=info["sender_id"], text=self.dbUser["twitter"]["messages"]["dm"]))
        elif (self.area["action"]["service"] == "github"):
            self.fromGithub(info)
        elif (self.area["action"]["service"] == "trello"):
            self.fromTrello(info)
        elif (self.area["action"]["service"] == "spotify"):
            self.fromSpotify(info)

    def pushEvent(self, info):
        self.area = info["area"]
        for service in self.area["reaction"]:
            if service["service"] == "twitter":
                for type_ in service["type"]:
                    print(f"type boucle type_ = {type_}")
                    if (type_ == "followback"):
                        self.followBack(info)
                    elif (type_ == "post"):
                        print("yes")
                        self.post(info)
                    elif (type_ == "retweet"):
                        self.retweetIdoles(info)
                    elif (type_ == "like"):
                        self.likeIdoles(info)
                    elif (type_ == "markRead"):
                        self.markRead(info)
                    elif (type_ == "sendDm"):
                        self.sendDm(info)
                return
        return
# ------------Pull event ------

    def checkNewFollow(self):
        oldFollowers = self.dbUser["twitter"]["info"]["followers"]
        followers = self.api.get_followers()
        newFollowers = list()
        dbFollowers = list()
        for elem in followers:
            dbFollowers.append(elem.screen_name)
            if elem.screen_name not in oldFollowers:
                newFollowers.append(elem.screen_name)
        db.users.update_one({"username": self.username}, {"$set": {"twitter.info.followers": dbFollowers}})
        if newFollowers:
            return ({"users_screen_name": newFollowers, "area": self.area})
        return (None)

    def checkNewTweetFromIdole(self):
        idoles = self.dbUser["twitter"]["info"]["idoles"]
        newTweets = list()
        for idole in idoles:
            dbTweetIds = list()
            oldTweets = idole["tweet_ids"]
            lastTweets = self.api.user_timeline(screen_name=idole["name"], include_rts=False)
            for elem in lastTweets:
                id_ = elem.id
                dbTweetIds.append(id_)
                if id_ not in oldTweets:
                    newTweets.append(id_)
            db.users.update_one({"username": self.username, "twitter.info.idoles.name": idole["name"]}, {"$set": {"twitter.info.idoles.$.tweet_ids": dbTweetIds}})
        if newTweets:
            return ({"area": self.area, "tweet_ids": newTweets})
        return (None)

    def checkLastDm(self):
        oldDm = self.dbUser["twitter"]["info"]["dm"]
        lastDms = self.api.get_direct_messages(count=2)
        for lastDm in lastDms:
            if (lastDm.message_create["sender_id"] != self.dbUser["twitter"]["token"]["user_id"] and
                lastDm.id != oldDm):
                db.users.update_one({"username": self.username}, {"$set": {"twitter.info.dm": lastDm.id}})
                info = {"area": self.area, "dm": lastDm.id, "sender_id": lastDm.message_create["sender_id"]}
                return (info)
            return (None)
        return (None)

    def pullEvent(self, area):
        self.area = area
        if (area["action"]["type"] == "follow"):
            return (self.checkNewFollow())
        if (area["action"]["type"] == "idolesTweets"):
            return (self.checkNewTweetFromIdole())
        if (area["action"]["type"] == "dm"):
            return(self.checkLastDm())

