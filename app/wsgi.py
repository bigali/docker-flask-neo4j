# -*- coding: utf-8 -*-

from watson import WatsonRelationshipExtractionService, WatsonUserModelingService
import tweepy
from flask import Flask, request, jsonify
import os

application = Flask(__name__)

auth = tweepy.OAuthHandler("VGbGua2zcrvAt8q7rFzYcF7Pp", "LC7DxOcHjzaoHH61MjlWwJvkERWhvnNIHKIasvvvDq9i3J8fGf")
auth.set_access_token("273164662-rcIu2uf0crCAolbKpGJETrU9iMc5XhDHjEo2Oupq",
                      "QxjyYfMQlK83GqwxVZmD4AZFIjtVNTbALFmrGLFdfjfjo")

api = tweepy.API(auth)


def flattenPortrait(tree):
    nodes = []
    edges = []

    def f(t):
        if t is None:
            return None
        # if level > 0 and (("children" not in t) or level != 2):
        if t["id"] == 'r':
            nodes.append({
                "id": t["id"],
                "label": "portrait",
                "shape": "circle",
                "value": 300
            })
        else:
            nodes.append({
                "id": t["id"],
                "label": t["name"]+"\n"+("%d%%" % int(t["percentage"] * 100) if "percentage" in t else ""),
                "group": t["category"] if "category" in t else "",
                "shape": "dot",
                "value": int(t["percentage"] * 100) if "percentage" in t else 100
            })
        if "children" in t:
            for elem in t["children"]:
                if t["id"] != elem["id"]:
                    edges.append({
                        "from": t["id"],
                        "to": elem["id"]
                    })
                f(elem)

    f(tree)
    return nodes, edges


userModeling = WatsonUserModelingService(url="https://gateway.watsonplatform.net/systemu/service/",
                                         user="072abbf5-28cd-48e8-920a-cd147fb83578", password="CQjtluCopyFo")
relationshipExtration = WatsonRelationshipExtractionService(user="d9d905bb-70f9-42a0-9200-2db9e5c6af69",


@application.route('/', methods=['GET'])
def index():
    return 'Hello form iocontext!'

@app.route('/api/v1/portrait/<screen_name>')
def getPortrait(screen_name):
    # tweets = api.user_timeline(id=screen_name,  )
    tweets = tweepy.Cursor(api.user_timeline, id=screen_name).items(200)
    text = ""
    for tweet in tweets:
        text += tweet.text + "\n " + "\n"
    portrait = userModeling.requestPortrait(text)
    nodes, edges = flattenPortrait(portrait["tree"])

    return jsonify({'nodes': nodes,
                    'edges': edges})

@app.route('/api/v1/viz/<screen_name>')
def viz(screen_name):
    # tweets = api.user_timeline(id=screen_name,  )
    tweets = tweepy.Cursor(api.user_timeline, id=screen_name).items(200)
    text = ""
    for tweet in tweets:
        text += tweet.text + "\n " + "\n"
    portrait = userModeling.requestPortrait(text)
    viz = userModeling.requestVisualization(portrait)
    return viz

@app.route('/api/v1/interests/<screen_name>')
def getRelationship(screen_name):
    # tweets = api.user_timeline(id=screen_name,  )
    tweets = tweepy.Cursor(api.user_timeline, id=screen_name).items(20)
    text = ""
    for tweet in tweets:
        text += tweet.text + "\n " + "\n"
    relationship = relationshipExtration.extractRelationship(text)
    return jsonify({'relationship': relationship})


@app.route('/api/v1/getPeople')
def searchUser():
    users = api.search_users(request.args['name'])
    return jsonify({'users': [
        {'name': user.name,
         'description': user.description,
         'profile_image_url': user.profile_image_url,
         'screen_name': user.screen_name
        } for user in users
    ]})


def test():
    application.run(debug=True)

if __name__ == '__main__':
    test()
