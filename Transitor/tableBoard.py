import common
import datetime
import time

def deltaTime(timeOfDeparture):
    """
    :param timeOfDeparture: Time at which the bus is supposed to depart in datetime format
    :return:(int)time left until departure
    """
    a = datetime.datetime.now()
    a = a.replace(microsecond=0)

    c = timeOfDeparture - a

    #DEBUGGING
    # print("\n" + str(timeOfDeparture))
    # print(a)
    # print("Result :", c.total_seconds())
    # print("Result minutes :", int(c.total_seconds())//60, end="\n\n")

    return (int(c.total_seconds())//60)

def getDateAndTime(inputString):
    splitInputData = inputString.split("T")
    date = splitInputData[0].split("-")

    # date = ""
    # for el in range(0,len(tempData)):
    #     if el != 0:
    #         date += "/"
    #     date += tempData[len(tempData)-el-1]

    time = splitInputData[1][:-8].split(":")

    return datetime.datetime(int(date[0]), int(date[1]), int(date[2]), int(time[0]), int(time[1]))

def getTableBoard(station):
    """

    :param station: [MANDATORY] Station to check table-board.             {string}
    :return: list
    """

    urlForRequest = common.apiURL + "stationboard"
    urlForRequest += "?station=" + common.getCorrectLocationURLFormatted(station) + "&limit=10"

    dic = common.doRequest(urlForRequest)

    result = []

    for i in range(0, len(dic["stationboard"])):
        result.append({"numberLine" : dic["stationboard"][i]["number"],
                    "intermediateStops" : []})
        for j in dic["stationboard"][i]["passList"]:
            result[i]["intermediateStops"].append({"nameStop" : j["location"]["name"],
                                                "arrivalHour" : j["arrival"]})

    #DEBUG
    #Visualize ris
    for i in result:
        print("numberLine :", i["numberLine"])
        print("IntermediateStops : ")
        for j in i["intermediateStops"]:
            print("\t\tnameStop :", j["nameStop"])
            print("\t\tarrivalHour :", j["arrivalHour"], end="\n\n")

    return returnHTMLBoard(result)

def returnHTMLBoard(data):

    contentPage = ""
    for i in range(0, len(data)):

        arrivalTime = getDateAndTime(data[i]["intermediateStops"][0]["arrivalHour"])
        time = deltaTime(arrivalTime)

        templateVars = {"arrivalName" : data[i]["intermediateStops"][len(data[i]["intermediateStops"])-1]["nameStop"],
                        "departureName" : data[i]["intermediateStops"][0]["nameStop"],
                        "time" : time}

        outputText = common.jinjaSubstitution(templateVars,"departureBoardTemplate.jinja")
        contentPage += outputText

    fullPageHTML = common.jinjaSubstitution({"variabile" : contentPage},"initDepartureBoardTemplate.jinja")

    return fullPageHTML
