import json
import requests

class Prediction:
    def __init__(self, id="", author="", historic_score={}, prediction={}):
        # string representing the mongo-assigned id
        self.id = id

        # string representing the author who made the prediction
        self.author = author

        # Dictionary whith keys representing the date a score is change, and entry representing the new score
        self.historic_score = historic_score 
                
        # Dictionary of f1 drivers in the order of their predition, tied to their offset
        self.prediction = prediction

        ## Class Invarient: 
        ## the sum of each each entry in prediction must equal the most recent entry of historic_score

    # update_score(race)
    # should only be called if current standings have changed, after a race
    # compares standings to prediction, changing values along the way
    # sum the new values of prediction
    # adds a new value to historic score with key as (race) and entry as new prediction sum

    # update_prediction
    # abstracted out of update_score
    # creates variable sum
    # iterate through prediction alongside current standings
    # if difference exist find out how far those offsets are and save them to prediction
    # save each final prediction value to sum
    # return sum

    # get_curr_score
    # if historic_score is empty, return 0
    # else return the last value of historic score

    # ranked_predictions
    # create a new empty dict
    # iterate for i in range len(prediction)
    #   if len(dict) = len(prediction) return dict
    # else insert any value from prediction that matches i
    # 
    # the returned dictionary will be the prediction in order of best to worst prediction
    

# takes in a predition object, and returns a dictionary made from its state variables
def predict_to_dict(pred):
    if not isinstance(pred, Prediction):
        raise TypeError("can only convert Prediction objects to dictionary")
    
    # we convert our state variables into a dictionary
    # note* this dictionary does not contain _id, in an effor to prevent the overriding of mongo assigned _id's
    # if the i'd of a prediction is needed, it should be pulled from the prediction itself, not this dictionary
    prediction_dictionary = dict(author=pred.author, historic_score=pred.historic_score, prediction=pred.prediction)

    # return the dictionary
    return prediction_dictionary


# takes a dictionary, and transforms it into a new prediction
def dict_to_predict(dict):
    id = dict['_id']
    author = dict['author']
    historic_score = dict['historic_score']
    prediction = dict['prediction']

    pred = Prediction(id,author,historic_score,prediction)
    return pred

# returns the current f1 standings
def get_standings():
    url = "http://ergast.com/api/f1/current/driverStandings.json"
    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    data = json.loads(response.text)

    standings = data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']
    print(type(standings))
    return standings

# returns driver at position 'pos' in the standings
def get_driver(pos):
    return get_standings()[int([pos])]
