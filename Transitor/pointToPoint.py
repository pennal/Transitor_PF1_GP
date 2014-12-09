import common
import jinja2 #Used to substitute the tags in the html
import os
import json

def getDateAntTimeSplit(inputString):
    splitInputData = inputString.split("T")
    tempData = splitInputData[0].split("-")
    date = ""
    for el in range(0,len(tempData)):
        if el != 0:
            date += "/"
        date += tempData[len(tempData)-el-1]

    time = splitInputData[1][:-8]
    return time,date

def returnHTMLTable(data):
    """
    DEBUG!!!!!!!!!!!!!!!!!!!
    """
    for i in range(0,len(data["connections"])):
        stationFrom = data["connections"][i]["from"]["station"]["name"]
        stationTo = data["connections"][i]["to"]["station"]["name"]

        departureTimeTemp = data["connections"][i]["from"]["departure"]
        departureTime, departureDate = getDateAntTimeSplit(departureTimeTemp)


        arrivalTimeTemp = data["connections"][i]["to"]["arrival"]
        arrivalTime, arrivalDate = getDateAntTimeSplit(arrivalTimeTemp)


        departurePlatform = data["connections"][i]["from"]["platform"]
        arrivalPlatform = data["connections"][i]["to"]["platform"]


        transfersTag = ""
        try:
            newData = data["connections"][i]["sections"]
            print("Amount of connections: ",len(newData))
            for connection in range(0,len(newData)):
                print("Processing connection ",connection)
                if connection == 0:
                    # we only need the arrival
                    intermediateArrivalName = newData[connection]["arrival"]['station']["name"]
                    intermediateArrivalTime, intermediateArrivalDate = getDateAntTimeSplit(newData[connection]['arrival']["arrival"])
                    intermediateArrivalPlatform = newData[connection]["arrival"]['platform']

                    templateLoader = jinja2.FileSystemLoader( searchpath="/" )
                    #Get the current path of this file. From here, put togehter the path of the template file
                    basePath = os.path.dirname(os.path.abspath(__file__))
                    # An environment provides the data necessary to read and
                    #   parse our templates.  We pass in the loader object here.
                    templateEnv = jinja2.Environment( loader=templateLoader )

                    # This constant string specifies the template file we will use.
                    #TEMPLATE_FILE = basePath + "/JinjaTemplates/table.jinja"
                    TEMPLATE_FILE = basePath + "/JinjaTemplates/transfersTemplateArrival.jinja"
                    # Read the template file using the environment object.
                    # This also constructs our Template object.
                    template = templateEnv.get_template( TEMPLATE_FILE )

                    # Specify any input variables to the template as a dictionary.
                    templateVars = { "intermediateStationArrival" : intermediateArrivalName,
                                     "arrivalTimeStep":intermediateArrivalTime,
                                     "arrivalPlatform":intermediateArrivalPlatform
                                     }

                    # Finally, process the template to produce our final text.
                    outputText = template.render( templateVars )




                elif connection == len(newData)-1:
                    #We only need the departure
                    intermediateDepartureName = newData[connection]["departure"]['station']["name"]
                    intermediateDepartureTime, intermediateDepartureDate = getDateAntTimeSplit(newData[connection]['departure']["departure"])
                    intermediateDeparturePlatform = newData[connection]["departure"]['platform']

                    templateLoader = jinja2.FileSystemLoader( searchpath="/" )
                    #Get the current path of this file. From here, put togehter the path of the template file
                    basePath = os.path.dirname(os.path.abspath(__file__))
                    # An environment provides the data necessary to read and
                    #   parse our templates.  We pass in the loader object here.
                    templateEnv = jinja2.Environment( loader=templateLoader )

                    # This constant string specifies the template file we will use.
                    #TEMPLATE_FILE = basePath + "/JinjaTemplates/table.jinja"
                    TEMPLATE_FILE = basePath + "/JinjaTemplates/transfersTemplateDeparture.jinja"
                    # Read the template file using the environment object.
                    # This also constructs our Template object.
                    template = templateEnv.get_template( TEMPLATE_FILE )

                    # Specify any input variables to the template as a dictionary.
                    templateVars = { "intermediateStationDeparture" : intermediateDepartureName,
                                     "departureTimeStep":intermediateDepartureTime,
                                     "departurePlatform":intermediateDeparturePlatform
                                     }

                    # Finally, process the template to produce our final text.
                    outputText = template.render( templateVars )

                else:
                    intermediateArrivalName = newData[connection]["arrival"]['station']["name"]
                    intermediateArrivalTime, intermediateArrivalDate = getDateAntTimeSplit(newData[connection]['arrival']["arrival"])
                    intermediateArrivalPlatform = newData[connection]["arrival"]['platform']
                    intermediateDepartureName = newData[connection]["departure"]['station']["name"]
                    intermediateDepartureTime, intermediateDepartureDate = getDateAntTimeSplit(newData[connection]['departure']["departure"])
                    intermediateDeparturePlatform = newData[connection]["departure"]['platform']

                    templateLoader = jinja2.FileSystemLoader( searchpath="/" )
                    #Get the current path of this file. From here, put togehter the path of the template file
                    basePath = os.path.dirname(os.path.abspath(__file__))
                    # An environment provides the data necessary to read and
                    #   parse our templates.  We pass in the loader object here.
                    templateEnv = jinja2.Environment( loader=templateLoader )

                    # This constant string specifies the template file we will use.
                    #TEMPLATE_FILE = basePath + "/JinjaTemplates/table.jinja"
                    TEMPLATE_FILE = basePath + "/JinjaTemplates/transfersTemplateCombined.jinja"
                    # Read the template file using the environment object.
                    # This also constructs our Template object.
                    template = templateEnv.get_template( TEMPLATE_FILE )

                    # Specify any input variables to the template as a dictionary.
                    templateVars = { "intermediateStationArrival" : intermediateArrivalName,
                                     "arrivalTimeStep":intermediateArrivalTime,
                                     "arrivalPlatform":intermediateArrivalPlatform,
                                     "intermediateStationDeparture" : intermediateDepartureName,
                                     "departureTimeStep":intermediateDepartureTime,
                                     "departurePlatform":intermediateDeparturePlatform
                                     }

                    # Finally, process the template to produce our final text.
                    outputText = template.render( templateVars )

                transfersTag += outputText

        except:
            print("No Connections")








        templateLoader = jinja2.FileSystemLoader( searchpath="/" )
        #Get the current path of this file. From here, put togehter the path of the template file
        basePath = os.path.dirname(os.path.abspath(__file__))
        # An environment provides the data necessary to read and
        #   parse our templates.  We pass in the loader object here.
        templateEnv = jinja2.Environment( loader=templateLoader )

        # This constant string specifies the template file we will use.
        #TEMPLATE_FILE = basePath + "/JinjaTemplates/table.jinja"
        TEMPLATE_FILE = basePath + "/JinjaTemplates/resultsTemplate.jinja"
        # Read the template file using the environment object.
        # This also constructs our Template object.
        template = templateEnv.get_template( TEMPLATE_FILE )

        # Specify any input variables to the template as a dictionary.
        templateVars = { "stationFrom" : stationFrom,
                         "transfers" : transfersTag,
                         "stationTo" : stationTo,
                        "departureTime" : departureTime,
                        "departureDate" : departureDate,
                        "arrivalTime" : arrivalTime,
                        "departurePlatform":departurePlatform,
                        "arrivalPlatform":arrivalPlatform}

        # Finally, process the template to produce our final text.
        outputText = template.render( templateVars )


        if i==0:
            fullPageHTML = outputText
        else:
            fullPageHTML += outputText


    templateLoader = jinja2.FileSystemLoader( searchpath="/" )
    #Get the current path of this file. From here, put togehter the path of the template file
    basePath = os.path.dirname(os.path.abspath(__file__))
    # An environment provides the data necessary to read and
    #   parse our templates.  We pass in the loader object here.
    templateEnv = jinja2.Environment( loader=templateLoader )

    # This constant string specifies the template file we will use.
    TEMPLATE_FILE = basePath + "/JinjaTemplates/mainPage.jinja"

    # Read the template file using the environment object.
    # This also constructs our Template object.
    template = templateEnv.get_template( TEMPLATE_FILE )

    # Specify any input variables to the template as a dictionary.
    templateVars = { "title" : stationFrom + " to " + stationTo,
                     "description" : "Some description",
                    "textOfWebPage" : fullPageHTML}

    # Finally, process the template to produce our final text.
    outputText = template.render( templateVars )


    #print("Output text: ", outputText)


    return outputText



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

    urlForRequest = common.apiURL + "connections"
    # Get all input elements
    inputElements = locals()
    # Transform in a list
    inputElementsKeys = list(inputElements.keys())
    inputElementsValues = list(inputElements.values())

    # Holds the final input Values
    finalValues = []
    print(finalValues)
    # Add all items that are not the restricted ones, as well as are not 'None'
    for i in range(0,len(inputElementsKeys)):
        if inputElementsKeys[i] != "stationFrom" and inputElementsKeys[i] != "stationTo" and inputElementsKeys[i] != "urlForRequest" and inputElementsValues[i] != None:
            finalValues.append([inputElementsKeys[i],inputElementsValues[i]])

    # DEBUG: Display final values
    print(finalValues)

    # We start by adding the departure station and the destination
    urlForRequest += "?from=" + common.getCorrectLocationURLFormatted(stationFrom) + "&to=" + common.getCorrectLocationURLFormatted(stationTo)

    for i in range(0,len(finalValues)):
        if finalValues[i][0] == "via":
            urlForRequest += "&" + str(finalValues[i][0]) + "=" + common.getCorrectLocationURLFormatted(str(finalValues[i][1]))
        else:
            urlForRequest += "&" + str(finalValues[i][0]) + "=" + str(finalValues[i][1])

    print(urlForRequest)

    # HTTP Request with the data needed
    rawJSON = common.doRequest(urlForRequest)





    return returnHTMLTable(rawJSON)
