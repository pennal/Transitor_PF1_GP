import requests         # Used to request the data from the APIs
import json             # Used to pretty print the incoming JSON data
import jinja2 #Used to substitute the tags in the html
import os

# Base URL for the API
apiURL = 'http://transport.opendata.ch/v1/'

def jinjaSubstitution(dictWithValues,jinjaFilename):
    templateLoader = jinja2.FileSystemLoader( searchpath="/" )
    #Get the current path of this file. From here, put togehter the path of the template file
    basePath = os.path.dirname(os.path.abspath(__file__))
    # An environment provides the data necessary to read and
    #   parse our templates.  We pass in the loader object here.
    templateEnv = jinja2.Environment( loader=templateLoader )

    # This constant string specifies the template file we will use.
    #TEMPLATE_FILE = basePath + "/JinjaTemplates/table.jinja"
    TEMPLATE_FILE = basePath + "/JinjaTemplates/" + jinjaFilename
    # Read the template file using the environment object.
    # This also constructs our Template object.
    template = templateEnv.get_template( TEMPLATE_FILE )

    # Specify any input variables to the template as a dictionary.
    templateVars = dictWithValues

    # Finally, process the template to produce our final text.
    outputText = template.render( templateVars )

    return outputText

def doRequest(urlForQuery):
    """
    Perform the actual HTTP request. Kept in a separate function to handle all exceptions
    :param urlForQuery: URL for the query
    :return: JSON formatted data
    """
    #We trigger a false positive, as to go into the while loop
    hasTimedOut = True
    #While the text returned is a timeout, continue trying
    while hasTimedOut:
        try:
            response = requests.get(urlForQuery)
            data = json.loads(response.text)
            #Check if what was returned is actually a timeout issue
            if "errors" in data:
                if "Connection timed out" in data["errors"][0]["message"]:
                    hasTimedOut = True
                    print("Connection timed out. Retrying...")
            else:
                hasTimedOut = False
        except ConnectionError:
            print("ConnectionError: Check your internet connection, and retry")
        except:
            print("UnknownError: An unknown error has occured")



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