## FUNCTIONS ## - note* move functions to other files

# returns the current f1 standings
def get_standings():
    url = "http://ergast.com/api/f1/current/driverStandings.json"
    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    data = json.loads(response.text)

    standings = data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']
    return standings

# returns driver at position 'pos' in the standings
def get_driver(pos):
    return get_standings()[int([pos])]

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