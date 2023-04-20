from discord.ext import commands
from discord.ext import tasks
import discord
import json
import requests
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

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

# links us to the client with the ability to call bot.event
bot = commands.Bot(command_prefix="$", intents=discord.Intents.all())


## FUCTIONS ##

# returns the json data of a driver from the f1 api, based on the entered number
def get_driver(driver):
    url_json = "http://ergast.com/api/f1/current/driverStandings.json"
    payload = {}
    headers = {}

    response = requests.request("GET", url_json, headers=headers, data=payload)

    data = json.loads(response.text)

    Standings = data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']

    print(len(Standings))
    return (Standings[int(driver)])

# takes an array of predictions, shortens each to 3 letters, makes them capitol
# returns cleaned prediction, raises exception if driver cannot be cleaned (uses numbers, or less then 3 letters)
def clean_prediction(arr):
    return


# given a driver (three letter capitol code), checks the discord api to see if they exist
# returns true if they exist, otherwise false
def verify_driver(drv):
    return


# takes an array of predictions, makes sure its longer then 19 drivers, cleans the array, then verifies if the driver exists for this season
# returns the array upon completion, raises an Exception if a problem occurs
def check_prediction(arr):
    return


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
async def test(ctx, prt):
    print("this is a test")

# $driver: calls get_driver for a specific number
@bot.command()
async def driver(ctx, num):
    await ctx.send(get_driver(num))
    
# **INCOMPLETE**
# $predict: recives an array of predictions, puts them through check_prediction(), then adds them to the db
@bot.command()
async def predict(ctx, *arr):

    db.predictions.insert_one(
        {
            "message": arr,
            "author": str(ctx.author),
        }
    )

# **INCOMPLETE**
# $getPredictions: returns the prediction of the user who requested the data
@bot.command()
async def getPredictions(ctx):
    auth = str(ctx.author)
    key = {'author': auth}

    for m in db.server_messages_log.find(key):
        print(m)
    

bot.run(BOT_TOKEN)
