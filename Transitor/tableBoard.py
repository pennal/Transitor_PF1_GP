import common


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

    # #DEBUG
    # #Visualize ris
    # for i in result:
    #     print("numberLine :", i["numberLine"])
    #     print("IntermediateStops : ")
    #     for j in i["intermediateStops"]:
    #         print("\t\tnameStop :", j["nameStop"])
    #         print("\t\tarrivalHour :", j["arrivalHour"], end="\n\n")

    return returnHTMLBoard(result)

def returnHTMLBoard(data):

    contentPage = ""
    for i in range(0, len(data)):

        templateVars = {"arrivalName" : data[i]["intermediateStops"][len(data[i]["intermediateStops"])-1]["nameStop"],
                        "departureName" : data[i]["intermediateStops"][0]["nameStop"],
                        "time" : "Some"}

        outputText = common.jinjaSubstitution(templateVars,"departureBoardTemplate.jinja")
        contentPage += outputText

    fullPageHTML = common.jinjiaSubstitution({"variabile" : contentPage},"initDepartureBoardTemplate.jinja")

    return fullPageHTML
