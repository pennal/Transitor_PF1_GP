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

    return result

def returnHTMLBoard(data):
    for i in range(0, len(data)):
        numberLine = data[i]["numberLine"]

        templateLoader = jinja2.FileSystemLoader( searchpath="/" )
        #Get the current path of this file. From here, put togehter the path of the template file
        basePath = os.path.dirname(os.path.abspath(__file__))
        # An environment provides the data necessary to read and
        #   parse our templates.  We pass in the loader object here.
        templateEnv = jinja2.Environment( loader=templateLoader )

        # This constant string specifies the template file we will use.
        #TEMPLATE_FILE = basePath + "/JinjaTemplates/table.jinja"
        TEMPLATE_FILE = basePath + "/JinjaTemplates/arrivalBoardTable.jinja"
        # Read the template file using the environment object.
        # This also constructs our Template object.
        template = templateEnv.get_template( TEMPLATE_FILE )

        # Specify any input variables to the template as a dictionary.
        templateVars = { "stationFrom" : stationFrom,
                         "stationTo" : stationTo,
                        "departureTime" : departureTime,
                        "arrivalTime" : arrivalTime,
                        "departurePlatform":departurePlatform,
                        "arrivalPlatform":arrivalPlatform}