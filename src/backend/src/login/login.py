import pymongo

class Login ():
    def __init__(self):
        self.username = None
        self.passwd = None
        self.response = {}
        self.user = None
        self.newAccount = False

    def set_data(self, dict_, db):
        self.username = dict_.get("username")
        self.passwd = dict_.get("password")
        self.newAccount = dict_.get("newAccount")

    def checkPass(self):
        if (self.user["password"] == self.passwd):
            self.response["password"] = True
        else:
            self.response["password"] = False

    def checkInDb(self, db):
        len_users = db.users.count_documents({"username": self.username})
        if (len_users > 0):
            self.user = db.users.find_one({"username": self.username})
            self.response["username"] = True
            return (True)
        else:
            self.response["username"] = False
            return (False)

    def createNewAccount(self, db):
        if (db.users.count_documents({"username": self.username}) >= 1):
            self.response["username"] = True
            return
        db.users.insert_one({"username": self.username, "password": self.passwd})
        self.response["username"] = False
        return 

    def verification_login(self, request, db):
        dict_ = request.json
        print(dict_)
        self.set_data(dict_, db)
        if not (self.newAccount):
            if (self.checkInDb(db)):
                self.checkPass()
        else:
            self.createNewAccount(db)
        return (self.response)
