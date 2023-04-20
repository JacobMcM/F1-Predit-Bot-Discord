# old code from a previous attempt at this project
# much of it made under a web program replit
# most of it is obsolete and simply here for code preservation

import os
import discord
import requests
import json
import random
from replit import db

inten = discord.Intents.default()
inten.message_content = True

client = discord.Client(intents=inten)  # links us to discord client
token = os.environ['F1PredictBot_Token']


class Prediction:
    def __init__(self, user, prediction):
        self.user = user
        self.curr_score = 0
        self.historic_score = []
        self.prediction = {}
        for driver in prediction:
            self.prediction[driver] = 0

    def update_score(curr_standings):
        # curr_standings is a list of the current standings

        self.curr_score = 0

        # self.prediction is a dict, this transforms in to a list of just the keys
        predict = list(self.prediction.keys())

        for key in predict:
            pre_index = predict.index(key)
            curr_index = curr_standings.index(key)
            deviation = abs(curr_index - pre_index)

            self.curr_score += deviation
            self.prediction[key] = deviation

        self.historic_score.append(self.curr_score)

    def rank_predictions():
        print("work_in_progress")


class bot:
    def __init__(self):
        self.total_preditions = []
        self.current_standings


# Restart development above this line


f1_words = ["pole", "goatifi", "constuctor", "dogwater", "softs", "spinalla", "scuderia", "RB", "podium"]
response_words = ["gp2 engine", "in in in, out out out", "NOOOOOOOOOOOOOOOOOOOOOOOOO", "Mein Gott muss das sein",
                  "Tires are gone"]

if "responding" not in db.keys():  # not to be confused with reponse lol
    db["responding"] = True


def get_Curr_standings(driver):
    url_json = "http://ergast.com/api/f1/current/driverStandings.json"
    # url_XML = "http://ergast.com/api/f1/current/driverStandings.json"

    payload = {}
    headers = {}

    response_j = requests.request("GET", url_json, headers=headers, data=payload)

    # print(response.text)
    json_data = json.loads(response_j.text)

    Standings = json_data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']

    return (Standings[driver])


def update_response(response_message):
    if "responses" in db.keys():
        responses = list(db["responses"])
        responses.append(response_message)
        db["responses"] = responses
    else:
        db["responses"] = [response_message]


def delete_response(index):
    responses = db["responses"]
    if len(responses) > index:
        del responses[index]
        db["responses"] = responses


@client.event
async def on_ready():  # asyncly called when on_ready or when bot is ready
    print("I'm awake, booted as {0.user}".format(client))
    # get_Curr_standings()


@client.event
async def on_message(msg):
    print(msg.content)
    if msg.author == client.user:
        print("returning")
        return

    if msg.content.startswith('$hello'):
        print("msg understood")
        await msg.channel.send('Hello!')

    if msg.content.startswith('$stand'):
        driver = random.randint(0, 19)
        await msg.channel.send('pulling driver' + str(driver))
        await msg.channel.send(get_Curr_standings(driver))

    if db["responding"]:
        options = response_words
        if "responses" in db.keys():
            options = options + list(db["responses"])

        if any(word in msg.content for word in f1_words):  # if any f1_word appears in msg
            await msg.channel.send(random.choice(options))

    if msg.content.startswith("$new"):
        response_message = msg.content.split("$new ", 1)[1]
        update_response(response_message)
        await msg.channel.send(response_message + " added to responses")

    if msg.content.startswith("$list"):
        responses = []
        if "responses" in db.keys():
            responses = list(db["responses"])
        await msg.channel.send(responses)

    if msg.content.startswith("$responding"):
        value = msg.content.split("$responding ", 1)[1]

        if value.lower() == "true":
            db["reponding"] = True
            await msg.channel.send("Responding is on")

        else:
            db["reponding"] = False
            await msg.channel.send("Responding is off")


client.run(token)