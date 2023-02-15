from __main__ import app, oauth
from crypt import methods
import os
from dotenv import load_dotenv
from flask import request, session, url_for, redirect
from src.Github.github import GithubService

load_dotenv()


github = oauth.register(
    name='github',
    client_id=os.getenv('GITHUB_CLIENT_ID'),
    client_secret=os.getenv('GITHUB_CLIENT_SECRET'),
    access_token_url='https://github.com/login/oauth/access_token',
    access_token_params=None,
    authorize_url='https://github.com/login/oauth/authorize',
    authorize_params=None,
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user:email repo'},
)
github_service = GithubService()

@app.route("/login/github")
def loginGithub():
    github = oauth.create_client("github")
    redirect_uri = url_for('authorizeGithub', _external=True)
    return github.authorize_redirect(redirect_uri)

@app.route('/authorize/github/')
def authorizeGithub():
    github = oauth.create_client("github")
    token = github.authorize_access_token()
    print(token)
    github_service.addToDb(session["username"], token)
    return redirect('http://localhost:8081/')

@app.route("/github/addRepo", methods=["POST"])
def addRepo():
    info = request.json
    username = session["username"]
    github_service.setUser(username)
    resp = github_service.addRepo(info)
    return ({"response": resp})

@app.route("/github/addDefaultBoardList", methods=["POST"])
def adddefaultTrello():
    info = request.json
    username = session["username"]
    github_service.setUser(username)
    resp = github_service.addDefaultBoardList(info)
    return ({"response": resp})


# @app.route("/github/test/<username>")
# def githubTest(username):
#     github_service.test(username)
#     return("yoyo")

# @app.route("/github/createIssue/<username>", methods=["POST"])
# def createIssue(username):
#     # username = session["username"]
#     info = request.json["info"]
#     resp = github_service.createIssue(username, info)
#     return({"response": resp})

# @app.route("/github/closeIssue/<username>", methods=["POST"])
# def closeIssue(username):
#     # username = session["username"]
#     info = request.json["info"]
#     resp = github_service.closeIssue(username, info)
#     return({"response": resp})

# @app.route("/github/createPull/<username>", methods=["POST"])
# def createPullRequest(username):
#     # username = session["username"]
#     info = request.json["info"]
#     resp = github_service.createPullRequest(username, info)
#     return({"response": resp})