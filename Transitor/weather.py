import common
import json

baseURL = 'http://api.openweathermap.org/data/2.5/forecast?units=metric&'
weatherAPIKey = '970f1415d7c8305f158b25b13c3f1c24'

def getForecast(location,numberOfDays = 5):
    currentWeatherURL = baseURL + "q=" + location + "&cnt=" + str(numberOfDays)
    print(currentWeatherURL)
    data = common.doRequest(currentWeatherURL)
    forecast = []
    for i in range(0,len(data["list"])):
        clouds = data["list"][i]["clouds"]
        humidity = data["list"][i]["main"]["humidity"]
        windSpeed = data["list"][i]["wind"]["speed"]
        temperature = {
            "mainTemp" : data["list"][i]["main"]["temp"],
            "maxTemp" : data["list"][i]["main"]["temp_max"],
            "minTemp" : data["list"][i]["main"]["temp_min"]
        }
        currentSituation = data["list"][i]["weather"][0]["main"]

        forecast.append({
            "clouds" : clouds,
            "humidity" : humidity,
            "windSpeed" : windSpeed,
            "temperature" : temperature,
            "currentSituation" : currentSituation
        })


getForecast("Lugano",10)