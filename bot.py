from discord.ext import commands
from discord.ext import tasks
import discord
import json
import requests
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

# from predict import * ## predict is imported from functions
from functions import *

# loads data from the .env file
load_dotenv()
# get the token for the server
MONGO_URI = os.getenv('MONGO_URI')
#get the token of the bot
BOT_TOKEN = os.getenv('BOT_TOKEN')
#get id of the test channel
CHANNEL_ID = os.getenv('CHANNEL_ID')

# Create a new client and connect to the server
client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
db = client.storage

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# links us to the discord client with the ability to call bot.event
bot = commands.Bot(command_prefix="$", intents=discord.Intents.all())

# global variable representing the predictions in mognodb
# should be updated whenever a prediction in mongodb is updated
list_predictions = pull_predictions()

# global variable representing the standings in mongodb
# should be updated whenever standings in mongodb are updated
stored_standings = pull_standings()


# get current scores (pull the current_score of each prediction, and sort by rank)


# graph historic standings (long term using built-in python graph functions)


# post-race-update
# check if the current f1 standings have changed, if so...
# call the update_score function for each prediction
# call push_all_predictions






## EVENTS ##

#called upon activation
@bot.event
async def on_ready(): 
    #channel = bot.get_channel()
    #await channel.send("")
    print("f1 predict bot is awake")


#bot.command only reacts if a message begins with the preset comand operator "$"
# used to test various features
@bot.command()
async def test(ctx):

    a = "hello"
    print(a[:4])
    print("this is a test")

# $driver: calls get_driver for a specific number
@bot.command()
async def driver(ctx, num):
    await ctx.send(get_driver(num))

# $clean: tests the clean_prediction function
@bot.command()
async def clean(ctx, *arr):
    # turn arr from tuple to list
    arr = list(arr)
    arr = clean_prediction(arr)
    await ctx.send(arr)
    

# **INCOMPLETE**
# $predict: recives an array of predictions, puts them through check_prediction(), then adds them to the db
@bot.command()
async def predict(ctx, *arr):
    # turn arr from tuple to list
    arr = list(arr)

    list_predictions.append(add_prediction(str(ctx.author), arr))
    pred = list_predictions[-1]
    await ctx.send(pred.id)
    await ctx.send(predict_to_dict(pred))
     
    # saved so I dont forget ;P
    #db.predictions.insert_one(
    #    {
    #        "message": arr,
    #        "author": str(ctx.author),
    #    }
    #)

# **INCOMPLETE**
# $getPredictions: returns the prediction of the author who requested the data
@bot.command()
async def getPredictions(ctx):
    author = str(ctx.author)
    key = {'author': author}


    for m in db.prediction.find(key):
        await ctx.send(m)
        print(m)
        pred = dict_to_predict(m)
        print(type(pred.prediction))
    

bot.run(BOT_TOKEN)
