import common
import json
import datetime

baseURL = 'http://api.openweathermap.org/data/2.5/forecast/daily?'

weatherAPIKey = '970f1415d7c8305f158b25b13c3f1c24'

def getFormattedTemperature(temperature):
    temperature = str(temperature)
    if "." in temperature:
        intPart,decimalPart = temperature.split(".")
        intPart = int(intPart)
        decimalPart = int(decimalPart)

        if int(decimalPart) > 1 and int(decimalPart) <= 25:
            decimalPart = 0
        elif int(decimalPart) > 26 and int(decimalPart) <= 75:
            decimalPart = 5
        elif int(decimalPart) > 76 and int(decimalPart) <= 99:
            intPart += 1
            decimalPart = 0
        if decimalPart != 0:
            correctTemperature = str(intPart) + "." + str(decimalPart)
        else:
            correctTemperature = str(intPart)
    else:
        correctTemperature = temperature

    return correctTemperature


def prepareHTMLContent(data):
    insideContent = ""

    #DEBUG: Encoded weather icon
    forecastCode = "<ul><li class=\"icon-sun\"></li></ul>"



    for i in range(0,len(data)):
        dayName, dayNumber = datetime.datetime.fromtimestamp(int(data[i]["dt"])).strftime('%A %d').split(" ")
        dictOfValues = {
            "resultsNumber" : i + 1,
            "dayName" : dayName,
            "dayNumber" : dayNumber,
            "forecastCode" : forecastCode,
            "mainTemp" : data[i]["dayTemperature"],
            "humidity" : data[i]["humidity"],
            "pressure" : data[i]["pressure"],
            "windSpeed" : data[i]["windSpeed"],
            "dayTemp" : data[i]["dayTemperature"],
            "eveningTemp" : data[i]["eveningTemperature"],
            "Sunrise" : "REMOVE",
            "Sunset" : "REMOVE",
            "maxTemp" : data[i]["maxTemperature"],
            "minTemp" : data[i]["minTemperature"],
            "morningTemp" : data[i]["morningTemperature"],
            "nightTemp" : data[i]["nightTemperature"]
        }
        insideContent += common.jinjaSubstitution(dictOfValues,"weatherResults.jinja")
    lastDict = {
        "weatherResults" : insideContent
    }

    return common.jinjaSubstitution(lastDict,"weatherMain.jinja")


def getForecast(location):
    currentWeatherURL = baseURL + "q=" + location + "&units=metric&cnt=6"
    print(currentWeatherURL)
    data = common.doRequest(currentWeatherURL)
    forecast = []
    for i in range(0,len(data["list"])):
        clouds = data["list"][i]["clouds"]
        dt = data["list"][i]["dt"]
        humidity = data["list"][i]["humidity"]
        pressure = data["list"][i]["pressure"]
        windSpeed = data["list"][i]["speed"]
        dayTemperature = getFormattedTemperature(data["list"][i]["temp"]["day"])
        eveningTemperature = getFormattedTemperature(data["list"][i]["temp"]["eve"])
        maxTemperature = getFormattedTemperature(data["list"][i]["temp"]["max"])
        minTemperature = getFormattedTemperature(data["list"][i]["temp"]["min"])
        morningTemperature = getFormattedTemperature(data["list"][i]["temp"]["morn"])
        nightTemperature = getFormattedTemperature(data["list"][i]["temp"]["night"])

        currentSituation = data["list"][i]["weather"][0]["main"]

        forecast.append({
            "clouds" : clouds,
            "dt": dt,
            "humidity" : humidity,
            "pressure" : pressure,
            "windSpeed" : windSpeed,
            "dayTemperature" : dayTemperature,
            "eveningTemperature" : eveningTemperature,
            "maxTemperature" : maxTemperature,
            "minTemperature" : minTemperature,
            "morningTemperature" : morningTemperature,
            "nightTemperature" : nightTemperature,
            "currentSituation" : currentSituation
        })

    return prepareHTMLContent(forecast)