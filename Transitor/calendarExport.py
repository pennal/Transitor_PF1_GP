from icalendar import Calendar, Event
from datetime import datetime
from bs4 import BeautifulSoup  # Pretty self explanatory...
import urllib





def prettyPrintInformation(listOfEntries):
    stringToReturn = ""

    for i in range(0,len(listOfEntries)):
        if listOfEntries[i][2] == "":
            stringToReturn += listOfEntries[i][1] + ": " + listOfEntries[i][0] + "\n"
        else:
            stringToReturn += listOfEntries[i][1] + ": " + listOfEntries[i][0] + " (" + listOfEntries[i][2] + ")\n"
        if i%2 == 1:
            stringToReturn += '\n'

    # col_width = max(len(word) for row in listOfEntries for word in row) + 2
    # rowCounter = 0
    # for row in listOfEntries:
    #     rowCounter += 1
    #     for word in row:
    #         for i in range(0,col_width-len(word)):
    #             word += "."#"\u00A0"
    #         stringToReturn += word
    #
    #     stringToReturn += '\n'
    #     if rowCounter%2 == 0:
    #         for _ in range(0,2*col_width+2):
    #             stringToReturn += '-'
    #         stringToReturn += '\n'
    return stringToReturn

def downloadEventForCalendar(htmlPage):
    htmlPage = urllib.parse.unquote(urllib.parse.unquote(htmlPage))

    print(htmlPage)

    # DEBUG
    #htmlPage = open("/Users/Lucas/Desktop/resultHTMLBF.html").read()

    soup = BeautifulSoup(htmlPage)

    # Get the contents of the hidden tag
    hiddenInformation = soup.find_all('td')

    listOfData = []

    for i in range(0,len(hiddenInformation)):
        listOfData.append(hiddenInformation[i].text.split("|"))

    print(listOfData)

    stationFrom = listOfData[0][1]
    stationTo = listOfData[1][1]
    departureTime = listOfData[2][1]
    departureDate = listOfData[3][1]
    arrivalTime = listOfData[4][1]
    arrivalDate = listOfData[5][1]
    departurePlatform = listOfData[6][1]
    arrivalPlatform = listOfData[7][1]

    intermediateStops = listOfData[8][1].replace("\t","")

    intermediateStops = intermediateStops.replace("<","\n")
    intermediateStops = intermediateStops.replace("()","")

    if departurePlatform != "":
        stringForDepPlatform = "(" + departurePlatform + ")"
    else:
        stringForDepPlatform = ""

    if arrivalPlatform != "":
        stringForArrPlatform = "(" + arrivalPlatform + ")"
    else:
        stringForArrPlatform = ""

    intermediateStops = departureTime + ": " + stationFrom + " " + stringForDepPlatform + "\n" + intermediateStops

    intermediateStops += arrivalTime + ": " + stationTo + " " + stringForArrPlatform + ""
    print(intermediateStops)




    cal = Calendar()
    cal.add('prodid', 'Transitor')
    cal.add('version', '2.0')
    event = Event()

    summaryString = "Trip from " + stationFrom + " to " + stationTo

    splitDate = departureDate.split("/")
    splitDate[0],splitDate[1],splitDate[2] = int(splitDate[0]),int(splitDate[1]),int(splitDate[2])


    splitTime = departureTime.split(":")
    splitTime[0],splitTime[1] = int(splitTime[0]), int(splitTime[1])


    splitArrivalDate = arrivalDate.split("/")
    splitArrivalDate[0],splitArrivalDate[1],splitArrivalDate[2] = int(splitArrivalDate[0]),int(splitArrivalDate[1]),int(splitArrivalDate[2])

    splitArrivalTime = arrivalTime.split(":")
    splitArrivalTime[0],splitArrivalTime[1] = int(splitArrivalTime[0]), int(splitArrivalTime[1])


    event.add('summary', summaryString)
    event.add('dtstart', datetime(splitDate[2],splitDate[1],splitDate[0],splitTime[0],splitTime[1],0))
    event.add('dtend', datetime(splitArrivalDate[2],splitArrivalDate[1],splitArrivalDate[0],splitArrivalTime[0],splitArrivalTime[1],0))
    event.add('description', intermediateStops)
    event['uid'] = datetime.now().strftime('%s')
    event.add('priority', 5)
    cal.add_component(event)


    return cal.to_ical()