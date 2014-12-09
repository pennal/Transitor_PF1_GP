# -*- coding: utf-8 -*-
import pointToPoint
import tableBoard
from flask import request
from flask import Flask #Flask is the base server. use 'sudo pip3 install Flask' to install

app = Flask(__name__,static_url_path='') 

@app.route("/")
def mainPage():
    return app.send_static_file('index.html')


# ACTUAL CALL!!
# Example URL: http://127.0.0.1:5000/pointToPoint/doRequest?from=Lugano&to=Zug

@app.route("/api/ptp")
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

    return pointToPoint.getConnectionsPointToPoint(stationFrom,stationTo,via,time,date,isArrivalTime,transportations,limit,direct,sleeper,couchette,bike)

@app.route("/api/tb")
def doTBRequest():
    stationFrom = request.args.get('station')

    return tableBoard.getTableBoard(stationFrom)




if __name__ == "__main__":
    app.debug = True
    app.run()

#print(json.dumps(pointToPoint.getConnectionsPointToPoint("Lugano","Zürich HB"),indent=4))