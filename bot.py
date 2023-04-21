from discord.ext import commands
from discord.ext import tasks
import discord
import json
import requests
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

from predict import *
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

# used as a global variable to store all current Prediction objects
# is assigned the list of predictions on MongoDB on startup 
list_predictions = pull_predictions()

for l in list_predictions:
    print(l.id)



# add prediction
# get passed a prediction in the form of a list
# verify the list is a valid f1 prediction
# create a dictionary in the style of a prediction object
# insert that dict into mongo (to generate a new _id)
# pull that prediction from mongo, turn it into a Prediction object
# run update_score(start) on the prediction
# call push_push(prediction) to update mongo
# add predict to list_prediction


# get current standings (pull the current_score of each prediction, and sort by rank)


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

    ## in the future, will instead use add_prediction(arr)
    # the following is for testing
    
    
    author = str(ctx.author)
    historic_score = {}
    prediction = {}

    for drv in arr:
        prediction[drv] = 0

    #instead of immediatly making a prediction object, we will instead make a dictionary, place it into
    prediction_dictionary = dict(author=author, historic_score=historic_score, prediction=prediction)
        
    # insert one takes the value of a dictionary and converts into into JSON on it's own
    db.prediction.insert_one(
        prediction_dictionary
    )    
    
    #arr = check_prediction(arr)

    # if arr is a string instead of an arr, the string will contain information about why the process failed, and then we exit (return)
    #if isinstance(arr, str):
    #    await ctx.send(arr)
    #    return

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
