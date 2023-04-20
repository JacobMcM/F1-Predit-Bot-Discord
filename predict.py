import json

class Prediction:
    def __init__(self, id="", user="", historic_score={}, prediction={}):
        # string representing the mongo-assigned id
        self.id = id

        # string representing the user who made the prediction
        self.user = user

        # Dictionary whith keys representing the date a score is change, and entry representing the new score
        self.historic_score = historic_score 
        
        # int of the most recent score, retireved from the most recent addition to historic_score
        ## probably a better Idea to have current score be a returnable function, becuase historic score will likly be empty
        # self.current_score = self.historic_score[len(self.historic_score)-1]
        
        # Dictionary of f1 drivers in the order of their predition, tied to their offset
        self.prediction = prediction

        ## Class Invarient: 
        ## the sum of each each entry in prediction must equal the the current_score
        ## current_score must always equal the most recent entry of historic_score
    



# takes in a predition object, and returns a dictionary made from its state variables
def predict_to_dict(pred):
    if not isinstance(pred, Prediction):
        raise TypeError("can only convert Prediction objects to dictionary")
    
    # first we convert our state variables into a dictionary
    prediction_dictionary = dict(id=pred.id, user=pred.user, historic_score=pred.historic_score, prediction=pred.prediction)

    return prediction_dictionary


## UNFINISHED ##
# takes a dictionary, and transforms it into a new prediction
def dict_to_predict(dict):
    id = dict['_id']
    user = dict['user']
    historic_score = dict['historic_score']
    prediction = dict['prediction']

    pred = Prediction(id,user,historic_score,prediction)
    return pred

