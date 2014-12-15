import common
import datetime
import countriesDict

baseURL = 'http://api.openweathermap.org/data/2.5/forecast/daily?'
weatherAPIKey = '970f1415d7c8305f158b25b13c3f1c24'

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

    for i in range(0,len(data)):
        dayName, dayNumber = datetime.datetime.fromtimestamp(int(data[i]["dt"])).strftime('%A %d').split(" ")
        dictOfValues = {
            "resultsNumber" : i + 1,
            "dayName" : dayName,
            "dayNumber" : dayNumber,
            "forecastCode" : data[i]["forecastId"],
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
        "weatherResults" : insideContent,
        "location" : data[0]["locationOfWeather"]
    }

    return common.jinjaSubstitution(lastDict,"weatherMain.jinja")


def getForecast(location):
    currentWeatherURL = baseURL + "q=" + location + "&units=metric&cnt=6"
    print(currentWeatherURL)
    data = common.doRequest(currentWeatherURL)
    forecast = []
    locationOfWeather = data["city"]["name"] + ", " + countriesDict.getExtendedCountryName(data["city"]["country"])
    for i in range(0,len(data["list"])):
        weatherId = str(data["list"][i]["weather"][0]["id"])
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
            "forecastId" : forecastDict[weatherId],
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
            "currentSituation" : currentSituation,
            "locationOfWeather" : locationOfWeather
        })
    return prepareHTMLContent(forecast)