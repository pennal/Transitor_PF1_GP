import common

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

def durationOfTrip(originalDuration):
    numberOfDays = originalDuration[:2]
    hours,minutes = originalDuration[3:-3].split(":")
    stringToReturn = ""
    if int(numberOfDays) > 0:
        if int(numberOfDays) < 10:
            stringToReturn += numberOfDays[1:] + "d "
        else:
            stringToReturn += numberOfDays + "d "

    if int(hours) > 0:
        if int(hours) < 10:
            stringToReturn += hours[1:] + "h "
        else:
            stringToReturn += hours + "h "

    if int(minutes) > 0:
        if int(minutes) < 10:
            stringToReturn += minutes[1:] + "m"
        else:
            stringToReturn += minutes + "m"

    return stringToReturn

def returnHTMLTable(data):
    for i in range(0,len(data["connections"])):
        stationFrom = data["connections"][i]["from"]["station"]["name"]
        stationTo = data["connections"][i]["to"]["station"]["name"]

        departureTimeTemp = data["connections"][i]["from"]["departure"]
        departureTime, departureDate = getDateAntTimeSplit(departureTimeTemp)


        arrivalTimeTemp = data["connections"][i]["to"]["arrival"]
        arrivalTime, arrivalDate = getDateAntTimeSplit(arrivalTimeTemp)

        duration = durationOfTrip(data["connections"][i]["duration"])
        departurePlatform = data["connections"][i]["from"]["platform"]
        arrivalPlatform = data["connections"][i]["to"]["platform"]

        hiddenIntermediateStops = ""

        transfersTag = ""
        if len(data["connections"][i]["sections"]) != 1:
            try:
                newData = data["connections"][i]["sections"]



                for connection in range(0,len(newData)):
                    if connection == 0:
                        # we only need the arrival
                        intermediateArrivalName = newData[connection]["arrival"]['station']["name"]
                        intermediateArrivalTime, intermediateArrivalDate = getDateAntTimeSplit(newData[connection]['arrival']["arrival"])
                        intermediateArrivalPlatform = newData[connection]["arrival"]['platform']
                        # 20:11: Lugano (3)
                        hiddenIntermediateStops += intermediateArrivalTime + ": " + intermediateArrivalName + " (" + intermediateArrivalPlatform + ")<<"
                        templateVars = { "intermediateStationArrival" : intermediateArrivalName,
                                         "arrivalTimeStep":intermediateArrivalTime,
                                         "arrivalPlatform":intermediateArrivalPlatform
                                         }

                        # Finally, process the template to produce our final text.
                        outputText = common.jinjaSubstitution(templateVars,"transfersTemplateArrival.jinja")




                    elif connection == len(newData)-1:
                        #We only need the departure
                        intermediateDepartureName = newData[connection]["departure"]['station']["name"]
                        intermediateDepartureTime, intermediateDepartureDate = getDateAntTimeSplit(newData[connection]['departure']["departure"])
                        intermediateDeparturePlatform = newData[connection]["departure"]['platform']

                        # Specify any input variables to the template as a dictionary.
                        templateVars = { "intermediateStationDeparture" : intermediateDepartureName,
                                         "departureTimeStep":intermediateDepartureTime,
                                         "departurePlatform":intermediateDeparturePlatform
                                         }
                        hiddenIntermediateStops += intermediateDepartureTime + ": " + intermediateDepartureName + " (" + intermediateDeparturePlatform + ")"
                        outputText = common.jinjaSubstitution(templateVars,"transfersTemplateDeparture.jinja")

                    else:
                        intermediateArrivalName = newData[connection]["arrival"]['station']["name"]
                        intermediateArrivalTime, intermediateArrivalDate = getDateAntTimeSplit(newData[connection]['arrival']["arrival"])
                        intermediateArrivalPlatform = newData[connection]["arrival"]['platform']
                        intermediateDepartureName = newData[connection]["departure"]['station']["name"]
                        intermediateDepartureTime, intermediateDepartureDate = getDateAntTimeSplit(newData[connection]['departure']["departure"])
                        intermediateDeparturePlatform = newData[connection]["departure"]['platform']


                        # Specify any input variables to the template as a dictionary.
                        templateVars = { "intermediateStationArrival" : intermediateArrivalName,
                                         "arrivalTimeStep":intermediateArrivalTime,
                                         "arrivalPlatform":intermediateArrivalPlatform,
                                         "intermediateStationDeparture" : intermediateDepartureName,
                                         "departureTimeStep":intermediateDepartureTime,
                                         "departurePlatform":intermediateDeparturePlatform
                                         }
                        hiddenIntermediateStops += intermediateDepartureTime + ": " + intermediateDepartureName + " (" + intermediateDeparturePlatform + ") <" + intermediateArrivalTime + ": " + intermediateArrivalName + " (" + intermediateArrivalPlatform + ")<<"
                        outputText = common.jinjaSubstitution(templateVars,"transfersTemplateCombined.jinja")

                    transfersTag += outputText

            except Exception as e:
                print("No Connections: ", e)


        print(hiddenIntermediateStops)

        # Specify any input variables to the template as a dictionary.
        templateVars = {
            "stationFrom" : stationFrom,
             "transfers" : transfersTag,
             "stationTo" : stationTo,
             "departureTime" : departureTime,
             "departureDate" : departureDate,
             "arrivalTime" : arrivalTime,
             "arrivalDate" : arrivalDate,
             "departurePlatform":departurePlatform,
             "arrivalPlatform":arrivalPlatform,
             "duration": duration,
             "intermediateStops" : hiddenIntermediateStops
        }


        outputText = common.jinjaSubstitution(templateVars,"resultsTemplate.jinja")

        if i==0:
            fullPageHTML = outputText
        else:
            fullPageHTML += outputText


    # Specify any input variables to the template as a dictionary.
    templateVars = {"textOfWebPage" : fullPageHTML}


    outputText = common.jinjaSubstitution(templateVars,"mainPage.jinja")



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


    #Prepare the transportations options
    if len(transportations) != 10:
        transportationOptions = ""
        for typeOfTransportation in range(0,len(transportations)):

            transportationOptions += "transportations[]=" + transportations[typeOfTransportation]
            if typeOfTransportation != len(transportations) - 1:
                transportationOptions += "&"

    else:
        transportationOptions = None

    for i in range(0,len(inputElementsKeys)):
        if inputElementsKeys[i] == "transportations":
            inputElementsValues[i] = transportationOptions





    print("trans opt:",transportations)
    # Add all items that are not the restricted ones, as well as are not 'None'
    for i in range(0,len(inputElementsKeys)):
        if inputElementsKeys[i] != "stationFrom" and inputElementsKeys[i] != "stationTo" and inputElementsKeys[i] != "urlForRequest" and inputElementsValues[i] != None:
            finalValues.append([inputElementsKeys[i],inputElementsValues[i]])

    # DEBUG: Display final values
    print("Final Values: ", finalValues)

    # We start by adding the departure station and the destination
    urlForRequest += "?from=" + common.getCorrectLocationURLFormatted(stationFrom) + "&to=" + common.getCorrectLocationURLFormatted(stationTo)







    for i in range(0,len(finalValues)):
        if finalValues[i][0] == "via":
            urlForRequest += "&" + str(finalValues[i][0]) + "=" + common.getCorrectLocationURLFormatted(str(finalValues[i][1]))
        elif finalValues[i][0] == "transportations":
            urlForRequest += "&" + str(finalValues[i][1])
        else:
            urlForRequest += "&" + str(finalValues[i][0]) + "=" + str(finalValues[i][1])

    print("Final URL for request: " + urlForRequest)

    # HTTP Request with the data needed
    rawJSON = common.doRequest(urlForRequest)





    return returnHTMLTable(rawJSON)
