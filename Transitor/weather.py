import common
import datetime
import countriesDict
from pygeocoder import Geocoder

baseURL = 'https://api.forecast.io/forecast/e59201f23f3889e65c456b9903db3309/'

forecastDict = {
    "200":"<ul><li class=\"basethundercloud\"></li><li class=\"icon-thunder\"></li></ul>",
    "300":"<ul><li class=\"basecloud\"></li><li class=\"icon-drizzle\"></li></ul>",
    "301":"<ul><li class=\"basecloud\"></li><li class=\"icon-drizzle\"></li></ul>",
    "302":"<ul><li class=\"basecloud\"></li><li class=\"icon-drizzle\"></li></ul>",
    "310":"<ul><li class=\"basecloud\"></li><li class=\"icon-drizzle\"></li></ul>",
    "312":"<ul><li class=\"basecloud\"></li><li class=\"icon-drizzle\"></li></ul>",
    "313":"<ul><li class=\"basecloud\"></li><li class=\"icon-drizzle\"></li></ul>",
    "314":"<ul><li class=\"basecloud\"></li><li class=\"icon-drizzle\"></li></ul>",
    "321":"<ul><li class=\"basecloud\"></li><li class=\"icon-drizzle\"></li></ul>",
    "500":"<ul><li class=\"basecloud\"></li><li class=\"icon-rainy\"></li></ul>",
    "501":"<ul><li class=\"basecloud\"></li><li class=\"icon-rainy\"></li></ul>",
    "502":"<ul><li class=\"basecloud\"></li><li class=\"icon-rainy\"></li></ul>",
    "503":"<ul><li class=\"basecloud\"></li><li class=\"icon-rainy\"></li></ul>",
    "504":"<ul><li class=\"basecloud\"></li><li class=\"icon-rainy\"></li></ul>",
    "511":"<ul><li class=\"basecloud\"></li><li class=\"icon-sleet\"></li></ul>",
    "520":"<ul><li class=\"basecloud\"></li><li class=\"icon-drizzle\"></li></ul>",
    "521":"<ul><li class=\"basecloud\"></li><li class=\"icon-showers\"></li></ul>",
    "522":"<ul><li class=\"basecloud\"></li><li class=\"icon-showers\"></li></ul>",
    "531":"<ul><li class=\"basecloud\"></li><li class=\"icon-rainy\"></li></ul>",
    "600":"<ul><li class=\"basecloud\"></li><li class=\"icon-snowy\"></li></ul>",
    "601":"<ul><li class=\"basecloud\"></li><li class=\"icon-snowy\"></li></ul>",
    "602":"<ul><li class=\"basecloud\"></li><li class=\"icon-frosty\"></li></ul>",
    "611":"<ul><li class=\"basecloud\"></li><li class=\"icon-snowy\"></li></ul>",
    "612":"<ul><li class=\"basecloud\"></li><li class=\"icon-snowy\"></li></ul>",
    "615":"<ul><li class=\"basecloud\"></li><li class=\"icon-sleet\"></li></ul>",
    "616":"<ul><li class=\"basecloud\"></li><li class=\"icon-snowy\"></li></ul>",
    "620":"<ul><li class=\"basecloud\"></li><li class=\"icon-snowy\"></li></ul>",
    "621":"<ul><li class=\"basecloud\"></li><li class=\"icon-snowy\"></li></ul>",
    "622":"<ul><li class=\"basecloud\"></li><li class=\"icon-snowy\"></li></ul>",
    "701":"<ul><li class=\"icon-mist\"></li></ul>",
    "711":"<ul><li class=\"icon-mist\"></li></ul>",
    "721":"<ul><li class=\"icon-mist\"></li></ul>",
    "731":"<ul><li class=\"icon-mist\"></li></ul>",
    "741":"<ul><li class=\"icon-mist\"></li></ul>",
    "751":"<ul><li class=\"icon-mist\"></li></ul>",
    "761":"<ul><li class=\"icon-mist\"></li></ul>",
    "762":"<ul><li class=\"icon-mist\"></li></ul>",
    "771":"<ul><li class=\"icon-mist\"></li></ul>",
    "781":"<ul><li class=\"icon-mist\"></li></ul>",
    "800":"<ul><li class=\"icon-sun\"></ul>",
    "801":"<ul><li class=\"basecloud\"></li><li class=\"icon-sunny\"></li></ul>",
    "802":"<ul><li class=\"icon-cloud\"></li></ul>",
    "803":"<ul><li class=\"icon-cloud\"></li></ul>",
    "804":"<ul><li class=\"icon-cloud\"></li></ul>",
    "900":"<ul></ul>", 
    "901":"<ul></ul>",
    "902":"<ul></ul>",
    "903":"<ul></ul>",
    "904":"<ul></ul>",
    "905":"<ul></ul>",
    "906":"<ul></ul>",
    "951":"<ul><li class=\"basecloud\"></li><li class=\"icon-windy\"></li></ul>",
    "952":"<ul><li class=\"basecloud\"></li><li class=\"icon-windy\"></li></ul>",
    "953":"<ul><li class=\"basecloud\"></li><li class=\"icon-windy\"></li></ul>",
    "954":"<ul><li class=\"basecloud\"></li><li class=\"icon-windy\"></li></ul>",
    "955":"<ul><li class=\"windysnowcloud\"></li><li class=\"icon-windysnow\"></li></ul>",
    "956":"<ul><li class=\"windysnowcloud\"></li><li class=\"icon-windysnow\"></li></ul>",
    "957":"<ul><li class=\"windysnowcloud\"></li><li class=\"icon-windysnow\"></li></ul>",
    "958":"<ul></ul>",
    "959":"<ul></ul>",
    "960":"<ul></ul>",
    "961":"<ul></ul>",
    "962":"<ul></ul>",
}

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
            "forecastCode" : data[i]["forecastId"],
            "mainTemp" : getFormattedTemperature((float(data[i]["maxTemperature"]) + float(data[i]["minTemperature"]))/2),
            "humidity" : str(int(float(data[i]["humidity"])*100)),
            "pressure" : data[i]["pressure"],
            "windSpeed" : data[i]["windSpeed"],
            "apparentTemperatureMax" : data[i]["apparentTemperatureMax"],
            "apparentTemperatureMin" : data[i]["apparentTemperatureMin"],
            "maxTemp" : data[i]["maxTemperature"],
            "minTemp" : data[i]["minTemperature"],
            "precipitationProbability" : data[i]["precipitationProbability"],
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
    locationOfWeather = results.formatted_address.split(",")[0] + "," + countriesDict.getExtendedCountryName(results.formatted_address.split(",")[1])

    for i in range(0,len(data["daily"]["data"])):
        currentSituation = data["daily"]["data"][i]["icon"]
        weatherId = currentSituation
        #weatherId = str(data["list"][i]["weather"][0]["id"]) # WUT?
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
            "forecastId" : forecastDict["802"],
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
            "currentSituation" : currentSituation,
            "locationOfWeather" : locationOfWeather
        })
    return prepareHTMLContent(forecast)


#print(getForecast("Lugano"))