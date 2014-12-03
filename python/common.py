import requests         # Used to request the data from the APIs
import json             # Used to pretty print the incoming JSON data

# Base URL for the API
apiURL = 'http://transport.opendata.ch/v1/'


def doRequest(urlForQuery):
    """
    Perform the actual HTTP request. Kept in a separate function to handle all exceptions
    :param urlForQuery: URL for the query
    :return: JSON formatted data
    """
    try:
        #Actual http request
        response = requests.get(urlForQuery)
    except ConnectionError:
        print("Not connected to the internet")
    except:
        print("An unknown error has occured")

    # Convert incoming data to JSON, and return it
    return json.loads(response.text)

def getCorrectLocation(userInput):
    """
    Gets the correct station, based on the users input. Will always return the one with the highest score
    :param userInput: Name of the station entered by the user
    :return: (string) Name of the correct station
    """
    locationToCheck = userInput.replace(" ","%20")

    # Convert incoming data to JSON
    data = doRequest(apiURL + 'locations?query=' + locationToCheck)
    stringToReturn = str(data["stations"][0]["name"])


    return stringToReturn

def getCorrectLocationURLFormatted(userInput):
    return getCorrectLocation(userInput).replace("ü","ue").replace("ä","ae").replace("ö","oe").replace(" ","%20")