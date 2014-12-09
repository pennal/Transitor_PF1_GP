import common
import datetime
import time

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

def getTimeDifference(time1, date1, time2, date2):
    print("Time1 :", time1)
    print("Date1 :", date1)
    print("Time2 :", time2)
    print("Date2 :", date2)

    #If the dates share the same date
    if date1 == date2:
        hours1 = time1.split(":")[0]
        hours2 = time2.split(":")[0]
        minutes1 = time1.split(":")[1]
        minutes2 = time2.split(":")[1]

        # print("\nhours1 :", hours1, end="  ")
        # print("\nminutes1 :", minutes1)
        # print("\nhours2 :", hours2, end="  ")
        # print("\nminutes2 :", minutes2, end="\n\n")

        deltaMinutes = int(minutes2) - int(minutes1)
        deltaHours = int(hours2) - int(hours1)

        print("result :", deltaMinutes + deltaHours * 60)
        return deltaMinutes + deltaHours * 60
    else:
        print("Different Date!")

def getCurrentDateAndTime():
    return time.strftime("%H:%M"), time.strftime("%d/%m/%Y")

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

    currentTime, currentDate = getCurrentDateAndTime()
    getDateAntTimeSplit("2014-12-09T15:35:00+0100")

    contentPage = ""
    for i in range(0, len(data)):

        arrivalTime, arrivalDate = getDateAntTimeSplit(data[i]["intermediateStops"][0]["arrivalHour"])
        time = getTimeDifference(currentTime, currentDate, arrivalTime, arrivalDate)

        templateVars = {"arrivalName" : data[i]["intermediateStops"][len(data[i]["intermediateStops"])-1]["nameStop"],
                        "departureName" : data[i]["intermediateStops"][0]["nameStop"],
                        "time" : time}

        outputText = common.jinjaSubstitution(templateVars,"departureBoardTemplate.jinja")
        contentPage += outputText

    fullPageHTML = common.jinjaSubstitution({"variabile" : contentPage},"initDepartureBoardTemplate.jinja")

    return fullPageHTML
