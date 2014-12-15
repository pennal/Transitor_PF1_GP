import common
import datetime

def deltaTime(timeOfDeparture):
    """
    :param timeOfDeparture: Time at which the bus is supposed to depart
    :return:(int)time left until departure
    """

    a = datetime.datetime.now()
    c = timeOfDeparture - a
    res = divmod(c.days * 86400 + c.seconds, 60)
    if res[0] > 59: #More than an hour
            return str(res[0]//60) + 'h'
    else: #If time left is less than an hour
        return str(res[0]+1) +'\''

def getDateAndTime(inputString):
    departureTimeTemp = inputString.split("T")
    departureDate = departureTimeTemp[0]
    departureTime = departureTimeTemp[1].split("+")[0]#Remove the greenwich delta
    newTimeLeftAsString = deltaTime(datetime.datetime.strptime(departureTime + " " + departureDate,"%H:%M:%S %Y-%m-%d"))
    return newTimeLeftAsString

def getTableBoard(station):
    """
    :param station: [MANDATORY] Station to check table-board.             {string}
    :return: list
    """
    urlForRequest = common.apiURL + "stationboard"
    urlForRequest += "?station=" + common.getCorrectLocationURLFormatted(station) + "&limit=10"
    dic = common.doRequest(urlForRequest)
    result = [dic["stationboard"][0]["stop"]["station"]["name"]]

    for i in range(0, len(dic["stationboard"])):
        result.append([dic["stationboard"][i]["to"],dic["stationboard"][i]["number"],getDateAndTime(dic["stationboard"][i]["stop"]["departure"])])

    return returnHTMLBoard(result)

def returnHTMLBoard(data):
    contentPage = ""
    for i in range(1, len(data)):
        time = data[i][2]
        if time != "0'":
            templateVars = {"lineNumber" : data[i][1],
                            "arrivalName" : data[i][0],
                            "departureName" : data[0],
                            "time" : time}

            outputText = common.jinjaSubstitution(templateVars,"departureBoardTemplate.jinja")
            contentPage += outputText

    fullPageHTML = common.jinjaSubstitution({"variabile" : contentPage},"initDepartureBoardTemplate.jinja")

    return fullPageHTML