import common
import datetime
import countriesDict
from pygeocoder import Geocoder

baseURL = 'https://api.forecast.io/forecast/e59201f23f3889e65c456b9903db3309/'

forecastDict = {
    "clear-day":"<ul><li class=\"icon-sun\"></li></ul>",
    "clear-night":"<ul><li class=\"icon-sun\"></li></ul>",
    "rain":"<ul><li class=\"basecloud\"></li><li class=\"icon-drizzle\"></li></ul>",
    "snow":"<ul><li class=\"basecloud\"></li><li class=\"icon-snowy\"></li></ul>",
    "sleet":"<ul><li class=\"basecloud\"></li><li class=\"icon-sleet\"></li></ul>",
    "wind":"<ul><li class=\"basecloud\"></li><li class=\"icon-windy\"></ul>",
    "fog":"<ul><li class=\"icon-mist\"></li></ul>",
    "cloudy":"<ul><li class=\"icon-cloud\"></li></ul>",
    "partly-cloudy-day":"<ul><li class=\"basecloud\"></li><li class=\"icon-rainy icon-sunny\"></ul>",
    "partly-cloudy-night":"<ul><li class=\"basecloud\"></li><li class=\"icon-rainy icon-sunny\"></ul>",
    "hail":"<ul><li class=\"basecloud\"></li><li class=\"icon-hail\"></ul>",
    "thunderstorm":"<ul><li class=\"basethundercloud\"></li><li class=\"icon-thunder\"></ul>",
    "tornado":"<ul><li class=\"windyraincloud\"></li><li class=\"icon-windyrain\"></li></ul>",
}

def getCorrectIconForForecast(iconName):
    try:
        return forecastDict[iconName]
    except:
        return ""

def getFormattedTemperature(temperature):
    temperature = str(temperature)
    if "." in temperature:
        intPart,decimalPart = temperature.split(".")
        intPart = int(intPart)
        decimalPart = int(decimalPart)

        if int(decimalPart) > 1 and int(decimalPart) <= 25:
            decimalPart = 0
        elif int(decimalPart) > 25 and int(decimalPart) <= 75:
            decimalPart = 5
        elif int(decimalPart) > 75 and int(decimalPart) <= 99:
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

    for i in range(0,6):
        dayName, dayNumber = datetime.datetime.fromtimestamp(data[i]["dt"]).strftime('%A %d').split(" ")

        dictOfValues = {
            "resultsNumber" : i + 1,
            "dayName" : dayName,
            "dayNumber" : dayNumber,
            "forecastCode" : getCorrectIconForForecast(data[i]["forecastId"]),
            "mainTemp" : getFormattedTemperature((float(data[i]["maxTemperature"]) + float(data[i]["minTemperature"]))/2),
            "humidity" : str(int(float(data[i]["humidity"])*100)),
            "pressure" : data[i]["pressure"],
            "windSpeed" : data[i]["windSpeed"],
            "apparentTemperatureMax" : data[i]["apparentTemperatureMax"],
            "apparentTemperatureMin" : data[i]["apparentTemperatureMin"],
            "maxTemp" : data[i]["maxTemperature"],
            "minTemp" : data[i]["minTemperature"],
            "precipitationProbability" : str(int(float(data[i]["precipitationProbability"]*100))),
            "precipitationIntensity" : "{0:.2f}".format(float(data[i]["precipitationIntensity"]))
        }
        insideContent += common.jinjaSubstitution(dictOfValues,"weatherResults.jinja")
    lastDict = {
        "weatherResults" : insideContent,
        "location" : data[0]["locationOfWeather"]
    }

    return common.jinjaSubstitution(lastDict,"weatherMain.jinja")


def getForecast(location):


    results = Geocoder.geocode(location)
    print(results[0].coordinates)

    currentWeatherURL = baseURL + str(results[0].coordinates[0]) + "," + str(results[0].coordinates[1]) + "?units=si"

    data = common.doRequest(currentWeatherURL)
    forecast = []
    locationOfWeather = results.formatted_address.split(",")[0] + ", " + countriesDict.getExtendedCountryName(results.formatted_address.split(",")[1])

    for i in range(0,len(data["daily"]["data"])):
        currentSituation = data["daily"]["data"][i]["icon"]
        weatherId = data["daily"]["data"][i]["icon"]

        clouds = data["daily"]["data"][i]["cloudCover"]
        dt = data["daily"]["data"][i]["time"]
        humidity = data["daily"]["data"][i]["humidity"]
        pressure = data["daily"]["data"][i]["pressure"]
        windSpeed = data["daily"]["data"][i]["windSpeed"]
        apparentTemperatureMax = getFormattedTemperature(data["daily"]["data"][i]["apparentTemperatureMax"])
        apparentTemperatureMin = getFormattedTemperature(data["daily"]["data"][i]["apparentTemperatureMin"])
        maxTemperature = getFormattedTemperature(data["daily"]["data"][i]["temperatureMax"])
        minTemperature = getFormattedTemperature(data["daily"]["data"][i]["temperatureMin"])

        precipitationProbability = data["daily"]["data"][i]["precipProbability"]
        precipitationIntensity = data["daily"]["data"][i]["precipIntensity"]
        forecast.append({
        "forecastId" : weatherId,
        "clouds" : clouds,
        "dt": dt,
        "humidity" : humidity,
        "pressure" : pressure,
        "windSpeed" : windSpeed,
        "apparentTemperatureMax" : apparentTemperatureMax,
        "apparentTemperatureMin" : apparentTemperatureMin,
        "maxTemperature" : maxTemperature,
        "minTemperature" : minTemperature,
        "precipitationProbability" : precipitationProbability,
        "precipitationIntensity" : precipitationIntensity,
        "locationOfWeather" : locationOfWeather,
        "currentSituation" : currentSituation
    })
    return prepareHTMLContent(forecast)


    #print(getForecast("Lugano"))
