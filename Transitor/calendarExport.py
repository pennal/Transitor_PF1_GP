from icalendar import Calendar, Event
from datetime import datetime
import pytz
import  os
from bs4 import BeautifulSoup  # Pretty self explanatory...
import urllib



def downloadEventForCalendar(htmlPage):
    htmlPage = urllib.parse.unquote(urllib.parse.unquote(htmlPage))

    # DEBUG
    #htmlPage = open("/Users/Lucas/Desktop/resultHTMLBF.html").read()

    mainDiv = BeautifulSoup(htmlPage)

    entries = mainDiv.find_all('tr')[1:]
    print(len(entries), entries)
    # Get the names of departure and arrival station
    stationFrom,stationTo = entries[0].text.replace("to","").split(" ")
    stationFrom = stationFrom[1:]
    stationTo = stationTo[:-1]

    # Get the departure time
    depTime = entries[1].find_all('td')[1].text
    depPlatform = entries[1].find_all('td')[3].text
    arrivalTime = entries[4].find_all('td')[1].text


    depDate = entries[2].find_all('td')[1].text
    durationOfTrip = entries[2].find_all('td')[3].text[:-4]

    


    cal = Calendar()
    cal.add('prodid', 'Transitor')
    cal.add('version', '2.0')
    event = Event()

    summaryString = "Trip from " + stationFrom + " to " + stationTo

    splitDate = depDate.split("/")
    splitDate[0],splitDate[1],splitDate[2] = int(splitDate[0]),int(splitDate[1]),int(splitDate[2])

    # TODO: Time difference for different regions !!!!
    splitTime = depTime.split(":")
    splitTime[0],splitTime[1] = int(splitTime[0]), int(splitTime[1])


    splitArrivalTime = arrivalTime.split(":")
    splitArrivalTime[0],splitArrivalTime[1] = int(splitArrivalTime[0]), int(splitArrivalTime[1])


    event.add('summary', summaryString)
    event.add('dtstart', datetime(splitDate[2],splitDate[1],splitDate[0],splitTime[0],splitTime[1],0))
    event.add('dtend', datetime(splitDate[2],splitDate[1],splitDate[0],splitArrivalTime[0],splitArrivalTime[1],0))
    event['uid'] = datetime.now().strftime('%s')
    event.add('priority', 5)
    cal.add_component(event)


    return cal.to_ical()

