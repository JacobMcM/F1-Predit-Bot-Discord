import json
import requests
import re
from predict import *
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

# loads data from the .env file
load_dotenv()
# get the token for the server
MONGO_URI = os.getenv('MONGO_URI')


# Create a new client and connect to the server
client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
db = client.storage



## FUNCTIONS ##



# returns list of the data from mongodb transformed to Prediction classes
def pull_predictions():
    list = []
    for m in db.prediction.find():
        pred = dict_to_predict(m)
        list.append(pred)

    return list


# recieves a prediction object, uses the id of that prediction to insert it back into the mongodb
# called whenever a prediction is updated
def push_prediction(pred):
    id = pred.id
    try:
        db.prediction.find_one_and_replace({"_id":id}, predict_to_dict(pred))
    except Exception as e:
        print(e)


# given a list of predictions 
# for each in list call push_prediction
# called after succesful post_race_update
def push_all_predictions(list):
    for pred in list:
        if not isinstance(pred, Prediction):
            raise TypeError("not a list of predictions")
        
        push_prediction(pred)

# gets passed a list of driver codes which will be turned into a prediction and added to list_predictions and Mongodb, returns the newly created prediction
## note* requires check_prediction() & Prediction.update_score() before deployment
def add_prediction(author, pred):
    
    
    # ensure author is an author
    author = str(author)
    # ensure pred is a list, and not a tuple
    pred = list(pred)

    #Validate list
    # check_prediction(arr) # not currently finished

    historic_score = {}
    prediction = {}

    # for every driver in pred list, set its prediction value to 0
    for drv in pred:
        prediction[drv] = 0
    
    # create a new prediction with our state variables
    # note that id is set to temp, this is becuase it will be changed later to the mongo assigned _id
    new_prediction = Prediction("temp",author,historic_score,prediction)

    # our new_prediction will have no historic score and all prediction values will be 0, so we will update our prediction to have those values
    #new_prediction.update_score(init) ## NOTE doesnt exist yet
        
    # insert_one takes a dictionary inserts it into mongo, while .inserted_id will return the id of whats just been inserted
    id = db.prediction.insert_one(
        # predict_to_dict transforms a prediction object into a dictionary
        # note* predict_to_dict ignores the value of id, therefor skipping our id set to "temp"
        predict_to_dict(new_prediction)
    ).inserted_id

    #change our predictions id from "temp" to the mongo generated _id
    new_prediction.id = id

    # append our finalized new_prediction to list_predictions
    list_predictions.append(new_prediction)

    return list_predictions[-1]


# takes an array of predictions, shortens each to 3 letters, makes them capitol
# returns cleaned prediction, if driver cannot be cleaned (uses numbers, or less then 3 letters) returns string with reason
def clean_prediction(arr):
    
    # ensure arr is a list
    arr = list(arr)

    for i in range(len(arr)):
        # temp variable drv represent arr at i or driver at i
        drv = arr[i]

        # a regex of only alphabet characters
        regex = re.compile('[^a-zA-Z]')

        # remove any non-alphabet characters
        drv = regex.sub('', drv)

        # if the drv is less then 3 characters it wont match the api
        if len(drv) < 3:
            return arr[i] + " is not a valid driver"
        
        #shorten drv to 3 letters
        drv = drv[:3]

        # make drv all uppercase
        drv = drv.upper()

        # reassign arr at i to drv
        arr[i] = drv
    
    return arr

# **UNFINISHED** 
# given a driver (three letter capitol code), checks the f1 api to see if they exist
# returns true if they exist, otherwise false
def verify_driver(drv):
    return


# takes an array of predictions, makes sure its longer then 19 drivers, cleans the array, then verifies if the driver exists for this season
# returns the array upon completion, if it fails it returns a string containing the reason for failure
def check_prediction(arr):
    if len(arr) < 20:
        return "not enough drivers in prediction, there should be at least 20"
    
    arr = clean_prediction(arr)

    # if clean_prediction has found an error, it will return a string instead of a cleaned array
    # the string will be an error message deatailing what went wrong
    if isinstance(arr,str):
        return arr

    # for every driver in arr, if one doesnt appear in the standings we return a string with that driver and an error message
    for drv in arr:
        if not verify_driver(drv):
            return drv + " is not a driver in this seasons standings"
    
    # if all tests are passed, the arr returned will be a cleaned Array (rather then string)
    return arr