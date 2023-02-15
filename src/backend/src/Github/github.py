from github import Github
from pymongo import MongoClient


client = MongoClient("mongodb://db:27017/area",username="root", password="password", authSource="admin")
db = client.Area

class GithubService():
    
    def __init__(self, username=None) -> None:
        self.g = None
        self.username = None
        self.accessToken = None
        self.repo = None
        self.dbUser = None
        self.good = False
        if username:
            self.setUser(username)

    def setUser(self, username):
        self.username = username
        self.dbUser = db.users.find_one({"username": username})
        if not self.dbUser.get("github"):
            return
        self.accessToken = self.dbUser["github"]["token"]["access_token"]
        self.g = Github(self.accessToken)
        self.good = True

    def addToDb(self, username, token):
        db.users.update_one({"username": username}, {"$set": {"github.token": token, "github.repos": []}})

    def addRepo(self, info):
        repo = self.g.get_user().get_repo(info["repoName"])
        issues = [issue.number for issue in repo.get_issues()]
        branches = [branch.name for branch in repo.get_branches()]
        pulls = [pull.title for pull in repo.get_pulls()]
        info = {"name": repo.name, "issues": issues, "branches": branches, "pulls": pulls}
        if db.users.find_one({"username": self.username, "github.repos": {"$elemMatch": {"name": repo.name}}}):
            print("UPDATE")
            db.users.update_one({"username": self.username, "github.repos": {"$elemMatch": {"name": repo.name}}}, {"$set": {"github.repos.$": info}})
        else:
            db.users.update_one({"username": self.username}, {"$push": {"github.repos": info}})
        return ("OK")
    
    def addDefaultBoardList(self, info):
        db.users.update_one({"username": self.username, "github.repos": {"$elemMatch": {"name": info["repoName"]}}}, {"$set": {"github.repos.$.trelloBoard": info["boardName"], "github.repos.$.trelloList": info["listName"]}})
        return ("OK")

    def test(self, username):
        self.setUser(username)
        for repo in self.g.get_user().get_repos():
            print(repo.name)

    def createIssue(self, username, info):
        self.setUser(username)
        self.repo = self.g.get_user().get_repo(info["repo_name"])
        if (self.repo == None):
            return ("KO")
        self.repo.create_issue(title=info["title"], body=info["body"])
        return("OK")

    def closeIssue(self, username, info):
        self.setUser(username)
        self.repo = self.g.get_user().get_repo(info["repo_name"])
        if ((self.repo != None) and (issues := self.repo.get_issues())):
            for issue in issues:
                if (issue.title == info["issue_name"]):
                    issue.edit(state="closed")
                    return ("OK")
        return ("KO")

    def createPullRequest(self, username, info):
        self.setUser(username)
        self.repo = self.g.get_user().get_repo(info["repo_name"])
        if (self.repo == None):
            return ("KO")
        self.repo.create_pull(title=info["title"], body=info["body"], head=info["head"], base=info["base"])
        return ("OK")

    # --------------PUSH EVENT -----------------

    def addComment(self, info):
        if (self.area["action"]["type"] == "newIssue"):
            for repo in self.dbUser["github"]["repos"]:
                rRepo = self.g.get_user().get_repo(repo["name"])
                for issue in info["newIssues"]:
                    if issue["number"] in repo["issues"]:
                        print("JE VAIS COMMENTER")
                        rIssue = rRepo.get_issue(issue["number"])
                        rIssue.create_comment("Cheh !")

    def addIssue(self, info):
        if (self.area["action"]["type"] == "newLabel"):
            for label in info["labelNames"]:
                repo = self.g.get_user().get_repo(label["repo"])
                repo.create_issue(title=label["name"])

    def pullRequest(self, info):
        if (self.area["action"]["type"] == "archivedList"):
            for liste in info["lists"]:
                if ("BRANCH" in liste["listName"]):
                    repo = self.g.get_user().get_repo(liste["repo"])
                    branch = liste["listName"].split(' ')[2]
                    repo.create_pull(title="New pull (from trello)", body="JE pense que le fix est bon", head=branch, base="main")

    def pushEvent(self, info):
        self.dbUser = db.users.find_one({"username": self.username})
        self.area = info["area"]
        for service in self.area["reaction"]:
            if service["service"] == "github":
                for type_ in service["type"]:
                    if (type_ == "addComment"):
                        self.addComment(info)
                    if (type_ == "addIssue"):
                        self.addIssue(info)
                    if (type_ == "pullRequest"):
                        self.pullRequest(info)
                return
        return
    

# ---------------- PULL EVENT -------------------

    def checkNewIssue(self):
        newIssues = list()
        for oldRepo in self.dbUser["github"]["repos"]:
            oldIssues = oldRepo["issues"]
            rIssues = self.g.get_user().get_repo(oldRepo["name"]).get_issues()
            Issues = [issue.number for issue in rIssues]
            db.users.update_one({"username": self.username, "github.repos": {"$elemMatch": {"name": oldRepo["name"]}}}, {"$set": {"github.repos.$.issues": Issues}})
            for issue in rIssues:
                if (issue.number not in oldIssues):
                    newIssues.append({"number": issue.number, "title": issue.title, "repoName": oldRepo["name"]})
        if newIssues:
            info = {"area": self.area, "newIssues": newIssues}
            print(info["newIssues"])
            return (info)
        return (None)

    def checkNewBranch(self):
        newBranches = list()
        for oldRepo in self.dbUser["github"]["repos"]:
            oldBranches = oldRepo["branches"]
            rBranches = self.g.get_user().get_repo(oldRepo["name"]).get_branches()
            Branches = [branch.name for branch in rBranches]
            db.users.update_one({"username": self.username, "github.repos": {"$elemMatch": {"name": oldRepo["name"]}}}, {"$set": {"github.repos.$.branches": Branches}})
            for branch in rBranches:
                if (branch.name not in oldBranches):
                    newBranches.append({"name": branch.name, "repoName": oldRepo["name"]})
        if newBranches:
            info = {"area": self.area, "newBranches": newBranches}
            return (info)
        return (None)

    def checkNewPull(self):
        newPulls = list()
        for oldRepo in self.dbUser["github"]["repos"]:
            oldPulls = oldRepo["pulls"]
            rPulls = self.g.get_user().get_repo(oldRepo["name"]).get_pulls()
            Pulls = [pull.title for pull in rPulls]
            db.users.update_one({"username": self.username, "github.repos": {"$elemMatch": {"name": oldRepo["name"]}}}, {"$set": {"github.repos.$.pulls": Pulls}})
            for pull in rPulls:
                if (pull.title not in oldPulls):
                    newPulls.append({"title": pull.title, "repoName": oldRepo["name"]})
        if newPulls:
            print("NOUVELLE PULL Request !!")
            info = ({"area": self.area, "newPulls": newPulls})
            return (info)
        return (None)

    def pullEvent(self, area):
        self.area = area
        if (self.area["action"]["type"] == "newIssue"):
            return (self.checkNewIssue())
        if (self.area["action"]["type"] == "newBranch"):
            return (self.checkNewBranch())
        if (self.area["action"]["type"] == "newPull"):
            return (self.checkNewPull())
