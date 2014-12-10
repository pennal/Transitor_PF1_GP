from icalendar import Calendar, Event
from datetime import datetime
import pytz
import  os


def downloadEventForCalendar(htmlPage):
    cal = Calendar()
    cal.add('prodid', 'Transitor')
    cal.add('version', '2.0')
    event = Event()

    #summaryString = stationFrom + " to " + stationTo



    event.add('summary', 'Python meeting about calendaring')
    event.add('dtstart', datetime(2005,4,4,8,0,0,tzinfo=pytz.utc))
    event.add('dtend', datetime(2005,4,4,10,0,0,tzinfo=pytz.utc))
    event.add('dtstamp', datetime(2005,4,4,0,10,0,tzinfo=pytz.utc))
    event['uid'] = '20050115T101010/27346262376@mxm.dk'
    event.add('priority', 5)
    cal.add_component(event)


    return cal.to_ical()

