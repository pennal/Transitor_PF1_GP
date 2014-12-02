# -*- coding: utf-8 -*-
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

def getConnectionsPointToPoint(stationFrom,stationTo,via = None,date=None, time=None,isArrivalTime = None,transportations=None,limit=None,direct=None,sleeper=None,couchette=None,bike=None):
    """
    Get all the connections from point to point
    :param stationFrom: [MANDATORY] Departure station.                                  {string}
    :param stationTo: [MANDATORY] Arrival station.                                      {string}
    :param via: [OPTIONAL] Through which station the trip has to go through             {string}
    :param date: [OPTIONAL] Date pf departure                                           {YYYY-MM-DD}
    :param time: [OPTIONAL] Time of departure                                           {hh:mm}
    :param isArrivalTime: [OPTIONAL] whether the time/date entered is the arrival one   {0/1}
    :param transportations: [OPTIONAL] What kind of transportation to use               {ice_tgv_rj, ec_ic, ir, re_d, ship, s_sn_r, bus, cableway, arz_ext, tramway_underground}
    :param limit: [OPTIONAL] Amount of entries requested                                {1-6}
    :param direct: [OPTIONAL] does the connection have to be direct                     {0/1}
    :param sleeper: [OPTIONAL] whether overnight trains with beds are a must            {0/1}
    :param couchette: [OPTIONAL] whether overnight trains with couchettes are a must    {0/1}
    :param bike: [OPTIONAL] whether bikes have to be allowed on the train               {0/1}
    :return: JSON data of the connections
    """
    urlForRequest = apiURL + "connections"
    # Get all input elements
    inputElements = locals()
    # Transform in a list
    inputElementsKeys = list(inputElements.keys())
    inputElementsValues = list(inputElements.values())

    # Holds the final input Values
    finalValues = []
    # Add all items that are not the restricted ones, as well as are not 'None'
    for i in range(0,len(inputElementsKeys)):
        if inputElementsKeys[i] != "stationFrom" and inputElementsKeys[i] != "stationTo" and inputElementsKeys[i] != "urlForRequest" and inputElementsValues[i] != None:
            finalValues.append([inputElementsKeys[i],inputElementsValues[i]])

    # We start by adding the departure station and the destination
    urlForRequest += "?from=" + getCorrectLocationURLFormatted(stationFrom) + "&to=" + getCorrectLocationURLFormatted(stationTo)

    for i in range(0,len(finalValues)):
        if finalValues[i][0] == "via":
            urlForRequest += "&" + str(finalValues[i][0]) + "=" + getCorrectLocationURLFormatted(str(finalValues[i][1]))
        else:
            urlForRequest += "&" + str(finalValues[i][0]) + "=" + str(finalValues[i][1])

    # HTTP Request with the data needed
    rawJSON = doRequest(urlForRequest)

    # Do some additional processing

    return rawJSON


print(json.dumps(getConnectionsPointToPoint("Lugano","Zürich HB"),indent=4))