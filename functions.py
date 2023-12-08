# this is for lambda AWS
import requests
from datetime import datetime
import sqlalchemy as sa
import time
import pandas as pd

def getForecastFiveDays(cities, open_weather_api):
    res = []
    for city in cities:
        geo_query = "http://api.openweathermap.org/geo/1.0/direct?q=" + city + "&limit=1&appid="+open_weather_api
        geo_pos = requests.get(geo_query)
        geo_json = geo_pos.json()
        five_forecast = "http://api.openweathermap.org/data/2.5/forecast?units=metric&lat=" + str(geo_json[0]["lat"]) + "&lon=" + str(geo_json[0]["lon"]) + "&appid="+open_weather_api
        five_re = requests.get(five_forecast)
        five_json = five_re.json()
        weather = five_json["list"][8]
        temp_res = {
            "city" : city,
            "date_forecast": weather["dt_txt"],
            "main_temp": weather["main"]["temp"],
            "rain_percent": weather["pop"]*100,
            "wind_speed": weather["wind"]["speed"],
            "description": weather["weather"][0]["description"]
        }
        res.append(temp_res)
    res_df = pd.DataFrame(res)
    res_df["date_forecast"] = pd.to_datetime(res_df["date_forecast"])
    return res_df
    
def bringMeTheArrivals(icao):
    # bring up the initials
    purified_arrivals = []
    direct_url = "http://api.flightradar24.com/common/v1/airport.json"
    ppp = {"code":icao, "page":1}
    day24 = datetime.timestamp(datetime.now())+24*60*60
    
    # without headers you will get acquainted with 451 error
    headers={"User-Agent":"PostmanRuntime/7.35.0"}
    
    # getting first response to analyse the amount of work
    first_response = requests.get(direct_url, params=ppp, headers=headers)
    if first_response.status_code != 200:
        print("Something went wrong")
        return -1
    dir_json = first_response.json()
    
    # getting the amount of all pages
    pages = dir_json["result"]["response"]["airport"]['pluginData']['schedule']["arrivals"]["page"]["total"]
    page = 1
    total = dir_json["result"]["response"]["airport"]['pluginData']['schedule']["arrivals"]["item"]["total"]
    if total > 0:
        # now bringing all to the cycle - we will fetch first page, look for the others, repeat until we will
        # reach the end
        while True:
            try:
                arrivals = dir_json["result"]["response"]["airport"]["pluginData"]["schedule"]["arrivals"]["data"]
                for arrival in arrivals:
                    temp = arrival["flight"]
                    dt_object = datetime.utcfromtimestamp(temp["time"]["scheduled"]["arrival"])
                    if "Scheduled" in temp["status"]["text"] and temp["time"]["scheduled"]["arrival"] < day24:
                        temp_res ={
                            "id":temp["identification"]["row"],
                            "identification":temp["identification"]["number"]["default"],
                            "arrivalAirport":icao,
                            "departureAirport":temp["airport"]["origin"]["code"]["icao"],
                            "landing_time": dt_object.strftime('%Y-%m-%d %H:%M:%S')
                        }
                        purified_arrivals.append(temp_res)

                # checking if it is the last page or not
                if page == pages:
                    break
                page += 1
                ppp = {"code":icao, "page":page}
                response = requests.get(direct_url, params=ppp, headers=headers)
                dir_json = response.json()
                time.sleep(2)
            except:
                break

        # creating DataFrame, making datetime and returning
        arrivals_df = pd.DataFrame(purified_arrivals)
        arrivals_df.landing_time = pd.to_datetime(arrivals_df["landing_time"])
        return arrivals_df


def getMeFewAirports(icaos):
    result = pd.DataFrame()
    for icao in icaos:
        result = pd.concat([result, bringMeTheArrivals(icao)])
    return result