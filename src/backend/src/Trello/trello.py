import os
from turtle import position
from pymongo import MongoClient
from dotenv import load_dotenv
from trello import TrelloClient

load_dotenv()

client = MongoClient("mongodb://db:27017/area",username="root", password="password", authSource="admin")
db = client.Area

class Trello():

    def __init__(self, username=None) -> None:
        self.username = None
        self.token = None
        self.trello = None
        self.client = None
        self.board = None
        self.list = None
        self.card = None
        self.dbUser = None
        self.area = None
        self.good = False
        if (username):
            self.setInfo(username)

    def setInfo(self, username):
        self.username = username
        self.dbUser = db.users.find_one({"username": username})
        if not (trelloInfo := self.dbUser.get("trello")):
            return (False)
        self.token = trelloInfo["token"]
        self.client = TrelloClient(
            api_key=os.getenv("TRELLO_API_KEY"),
            api_secret=os.getenv("TRELLO_API_SECRET"),
            token=self.token
        )
        self.good = True
        return (True)

    def addBoardToCheck(self, info):
        board_name = info.get("boardName")
        all_boards = self.client.list_boards(board_filter="open")
        for board in all_boards:
            if (board.name == board_name):
                cards = [{"cardId":card.id, "cardLabel": [label.id for label in card.labels], "cardList": card.list_id, "cardName": card.name} for card in board.get_cards(filters="open")]
                listIds =  [{"listId": liste.id, "listName": liste.name} for liste in board.get_lists(list_filter="open")]
                labelsIds = [{"labelId": label.id, "labelName": label.name} for label in board.get_labels()]
                info = {"name": board.name, "id":board.id, "cards": cards, "lists": listIds, "labels": labelsIds}
                if db.users.find_one({"username": self.username, "trello.info.boards": {"$elemMatch": {"name": board_name}}}):
                    db.users.update_one({"username": self.username, "trello.info.boards": {"$elemMatch": {"name": board_name}}}, {"$set": {"trello.info.boards.$": info}})
                else:
                    db.users.update_one({"username": self.username}, {"$push": {"trello.info.boards": info}})

    def addDefaultLabelDb(self, info):
        for board in self.dbUser["trello"]["info"]["boards"]:
            if board["name"] == info["boardName"]:
                for label in board["labels"]:
                    rLabel = self.client.get_label(label_id=label["labelId"], board_id=board["id"])
                    if rLabel.name == info["labelName"]:
                        db.users.update_one({"username": self.username, "trello.info.boards": {"$elemMatch": {"name": info["boardName"]}}}, {"$set": {"trello.info.boards.$.defaultLabel": label["labelId"]}})
                        return ("OK")
        return ("KO")
    
    def addRepo(self, info):
        for board in self.dbUser["trello"]["info"]["boards"]:
            if board["name"] == info["boardName"]:
                for repo in self.dbUser["github"]["repos"]:
                    if repo["name"] == info["repoName"]:
                        db.users.update_one({"username": self.username, "trello.info.boards": {"$elemMatch": {"name": info["boardName"]}}}, {"$set": {"trello.info.boards.$.repo": info["repoName"]}})
                        return ("OK")
        return ("KO")

    def setBoard(self, info):
        all_boards = self.client.list_boards()
        for board in all_boards:
            if (board.name == info["boardName"]):
                self.board = board
                return (True)
        return (False)

    def setList(self, info):
        all_lists = self.board.all_lists()
        for liste in all_lists:
            if (liste.name == info["listName"]):
                self.list = liste
                return (True)
        return (False)

    def setCard_List(self, info):
        all_cards = self.list.list_cards()
        for card in all_cards:
            if (card.name == info["cardName"]):
                self.card = card
                return (True)
        return (False)

    def setCard_Board(self, info):
        all_card = self.board.all_cards()
        for card in all_card:
            if (card.name == info["cardName"]):
                self.card = card
                return (True)
        return (False)

    def addCard(self, info):
        if not (self.setBoard(info) and self.setList(info)):
            print("ERROR: addCard trello !")
            return ("KO")
        self.list.add_card(info["cardName"], position="top") #on peut ajouter plein d'arguement pour plus de possibilite
        print("SELF. ADD CARD ")
        return ("OK")

    def archiveCard(self, username, info):
        #TODO peut etre pas besoin de prendre la liste, juste la carte a partie de la board
        if not (self.setInfo(username) and self.setBoard(info) and self.setList(info)
                and self.setCard_List(info)):
            print("ERROR: archiveCard trello !")
            return ("KO")
        self.card.delete()
        return("OK")

    def addList(self, info):
        if not (self.setBoard(info)):
            print("ERROR: delList trello !")
            return ("KO")
        self.board.add_list(info["listName"], pos="bottom")
        return ("OK")

    def archiveList(self, username, info):
        if not (self.setInfo(username) and self.setBoard(info) and self.setList(info)):
            print("ERROR: delList trello !")
            return ("KO")
        self.list.close()
        return("OK")

    def cardChangeList(self, username, info):
        if not (self.setInfo(username) and self.setBoard(info) and
                self.setCard_Board(info)):
            print("ERROR: delList trello !")
            return ("KO")
        all_liste = self.board.all_lists()
        for liste in all_liste:
            if (liste.name == info["listNameFinal"]):
                self.card.change_list(liste.id)
                return ("OK")
        return ("KO")

# -----------------PUSH EVENTS ------------------------

    def setDefaultLabel(self, info):
        for card in info["newCardsIds"]:
            card = self.client.get_card(card_id=card["id"])
            if len(card.labels) == 0:
                for board in self.dbUser["trello"]["info"]["boards"]:
                    if board["id"] == card.board_id:
                        label = self.client.get_label(label_id=board["defaultLabel"], board_id=board["id"])
                        card.add_label(label)
                        break
        return

    def createNewCard(self, info):
        self.dbUser = db.users.find_one({"username": self.username})
        infoCard = {}
        if (self.area["action"]["type"] == "newIssue"):
            for issue in info["newIssues"]:
                for repo in self.dbUser["github"]["repos"]:
                    if issue["repoName"] == repo["name"]:
                        infoCard["boardName"] = repo["trelloBoard"]
                        infoCard["listName"] = repo["trelloList"]
                        infoCard["cardName"] = issue["title"]
                        break
                self.addCard(infoCard)
        if (self.area["action"]["type"] == "newList"):
            for liste in info["listNames"]:
                rListe = self.client.get_list(liste["id"])
                rListe.add_card("JE TE VOIS !")
        return

    def createNewList(self, info):
        infoList = {}
        if (self.area["action"]["type"] == "newBranch"):
            for branch in info["newBranches"]:
                for repo in self.dbUser["github"]["repos"]:
                    if branch["repoName"] == repo["name"]:
                        infoList["boardName"] = repo["trelloBoard"]
                        infoList["listName"] = "BRANCH : " + branch["name"]
                        break
                self.addList(infoList)

    def pushEvent(self, info):
        self.area = info["area"]
        for service in self.area["reaction"]:
            if service["service"] == "trello":
                for type_ in service["type"]:
                    if (type_ == "defaultLabel"):
                        self.setDefaultLabel(info)
                    if (type_ == "addCard"):
                        self.createNewCard(info)
                    if (type_ == "addList"):
                        self.createNewList(info)
                return
        return
# -----------------PULL EVENTS ------------------------

    def checkNewCards(self):
        allOldCards = list()
        cards = list()
        newCards = list()
        cardModLabel = list()
        cardModList = list()
        # Get toutes les cards ---------------
        for board in self.dbUser["trello"]["info"]["boards"]:
            oldCards = board["cards"]
            allOldCards.extend([card["cardId"] for card in oldCards])
            rBoard = self.client.get_board(board["id"])
            bCards = [{"cardId":card.id, "cardLabel": [label.id for label in card.labels], "cardList": card.list_id, "cardName": card.name} for card in rBoard.get_cards(filters="open")]
            cards.extend(bCards)
            # Check si elle a ete modifier ---------------------------------
            for old in oldCards:
                for now in bCards:
                    if old["cardId"] == now["cardId"]:
                        for label in now["cardLabel"]:
                            if label not in old["cardLabel"]:
                                cardModLabel.append(now["cardName"])
                        if old["cardList"] != now["cardList"]:
                            cardModList.append(now["cardName"])
                        break
            # Update en DB ------------------------------
            db.users.update_one({"username": self.username, "trello.info.boards": {"$elemMatch": {"id": board["id"]}}}, {"$set": {"trello.info.boards.$.cards": bCards}})
        # Check si il y en a des nouvelles -------------------------
        for card in cards:
            if (card["cardId"] not in allOldCards):
                newCards.append({"name": card["cardName"], "id": card["cardId"]})
        # Return les information -----------------------------
        if newCards or cardModLabel or cardModList:
            return({"area": self.area, "newCardsIds": newCards, "modLabel": cardModLabel, "modList": cardModList})    
        return (None)
    
    def checkNewLists(self):
        oldLists = list()
        lists = list()
        newLists = list()
        for board in self.dbUser["trello"]["info"]["boards"]:
            oldLists.extend(liste["listId"] for liste in board["lists"])
            rBoard = self.client.get_board(board["id"])
            bLists = [{"listId": liste.id, "listName": liste.name} for liste in rBoard.get_lists(list_filter="open")]
            db.users.update_one({"username": self.username, "trello.info.boards": {"$elemMatch": {"id": board["id"]}}}, {"$set": {"trello.info.boards.$.lists": bLists}})
            lists.extend(bLists)
        for liste in lists:
            if (liste["listId"]not in oldLists):
                newLists.append({"name": liste["listName"], "id": liste["listId"]})
        if newLists:
            return({"area": self.area, "listNames": newLists})
        return None

    def archivedList(self):
        archivedLists = list()
        for board in self.dbUser["trello"]["info"]["boards"]:
            rBoard = self.client.get_board(board["id"])
            bLists = [{"listId": liste.id, "listName": liste.name} for liste in rBoard.get_lists(list_filter="open")]
            for liste in board["lists"]:
                if (liste not in bLists):
                    liste["repo"] = board["repo"]
                    archivedLists.append(liste)
            db.users.update_one({"username": self.username, "trello.info.boards": {"$elemMatch": {"id": board["id"]}}}, {"$set": {"trello.info.boards.$.lists": bLists}})
        if archivedLists:
            return ({"area": self.area, "lists": archivedLists})
        return None

    def checkNewLabel(self):
        newLabels = list()
        for dbBoard in self.dbUser["trello"]["info"]["boards"]:
            oldLabels = [label["labelId"] for label in dbBoard["labels"]]
            realBoard = self.client.get_board(dbBoard["id"])
            bLabels = [{"labelId": label.id, "labelName": label.name} for label in realBoard.get_labels()]
            db.users.update_one({"username": self.username, "trello.info.boards": {"$elemMatch": {"id": dbBoard["id"]}}}, {"$set": {"trello.info.boards.$.labels": bLabels}})
            for label in bLabels:
                if (label["labelId"] not in oldLabels):
                    newLabels.append({"name":label["labelName"], "repo": dbBoard["repo"]})
        if newLabels:
            return ({"area": self.area, "labelNames": newLabels})
        return (None)

    def pullEvent(self, area):
        self.area = area
        if (self.area["action"]["type"] == "newCard"):
            return (self.checkNewCards())
        # TODO 
        # faire attention parce que si il choise les deux il y a un des deux qui ne marche pas a cause de l'update en db
        # if (self.area["action"]["type"] == "newList"):
        #     return (self.checkNewLists())
        if (self.area["action"]["type"] == "archivedList"):
            return (self.archivedList())
        ###################################
        if (self.area["action"]["type"] == "newLabel"):
            return (self.checkNewLabel())