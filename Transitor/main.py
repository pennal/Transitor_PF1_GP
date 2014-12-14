# -*- coding: utf-8 -*-
import pointToPoint
import tableBoard
import weather
from flask import request,make_response,abort
from flask import Flask #Flask is the base server. use 'sudo pip3 install Flask' to install
import calendarExport

app = Flask(__name__,static_url_path='') 

@app.route("/")
def mainPage():
    return app.send_static_file('index.html')


# ACTUAL CALL!!
# Example URL: http://127.0.0.1:5000/pointToPoint/doRequest?from=Lugano&to=Zug

@app.route("/api/p2p")
def doPTPRequest():
    stationFrom = request.args.get('from')
    stationTo = request.args.get('to')
    via = request.args.get('via')
    date=request.args.get('date')
    time=request.args.get('time')
    isArrivalTime = request.args.get('isArrivalTime')
    transportations=request.args.get('transportations')
    limit=request.args.get('limit')
    direct=request.args.get('direct')
    sleeper=request.args.get('sleeper')
    couchette=request.args.get('couchette')
    bike=request.args.get('bike')



    possibleParameters = [["stationFrom",stationFrom],["stationTo",stationTo],["via",via],["date",date],["time",time],["isArrivalTime",isArrivalTime],["transportations",transportations], ["limit",limit],["direct",direct],["sleeper",sleeper],["couchette",couchette],["bike",bike]]

    if possibleParameters[0][1] == "" or possibleParameters[1][1] == "":
        print("No departure or arrival given")
        return abort(404)

    for i in range(2,len(possibleParameters)):
        if possibleParameters[i][1] == "" or possibleParameters[i][1] == '0':
            possibleParameters[i][1] = None

    possibleParameters[6][1] = transportations.split(",")
    #Old Method
    #return pointToPoint.getConnectionsPointToPoint(stationFrom,stationTo,via,time,date,isArrivalTime,transportations,limit,direct,sleeper,couchette,bike)

    return pointToPoint.getConnectionsPointToPoint(stationFrom,stationTo,possibleParameters[2][1],possibleParameters[3][1],possibleParameters[4][1],possibleParameters[5][1],possibleParameters[6][1],possibleParameters[7][1],possibleParameters[8][1],possibleParameters[9][1],possibleParameters[10][1],possibleParameters[11][1])

@app.route("/api/tb")
def doTBRequest():
    station = request.args.get('station')

    return tableBoard.getTableBoard(station)

@app.route("/api/weather")
def doWeatherRequest():
    location = request.args.get('location')

    return weather.getForecast(location)




@app.route("/api/calendarExport")
def exportFromCalendar():
    htmlPage = request.args.get('htmlPage')

    calendarString = calendarExport.downloadEventForCalendar(htmlPage)
    response = make_response(calendarString)
    response.headers["Content-Disposition"] = "attachment; filename=calEvent.ics"
    response.headers['Cache-Control'] = 'no-cache'
    response.headers['Content-Type'] = 'application/ics'

    return response



    #return calendarExport.downloadEventForCalendar(htmlPage)

if __name__ == "__main__":
    app.debug = True
    app.run()

#print(json.dumps(pointToPoint.getConnectionsPointToPoint("Lugano","Zürich HB"),indent=4))