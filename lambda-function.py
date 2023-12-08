# this for lambda AWS
import json
import pandas as pd
import os
from functions import getForecastFiveDays, bringMeTheArrivals, getMeFewAirports


def lambda_handler(event, context):
    # This is a nice way to get your credentials from environment
    con = os.environ["con"]
    weather_api = os.environ["weather"]
    cities_df = pd.read_sql("cities", con) 
    cities_to_work = cities_df["city"].to_numpy()
    forecast = getForecastFiveDays(cities_to_work, weather_api)
    forecast.merge(cities_df, how="left", on="city")[["id_city", "date_forecast", "main_temp", "rain_percent", "wind_speed", "description"]].to_sql('forecasts',
              if_exists='append',
              con=con,
              index=False)
    airports_df = pd.read_sql("airports", con)
    icaos = cities_df.merge(airports_df, how="left", on="city")["icao"].to_numpy()
    arrivals = getMeFewAirports(icaos)
    arrivals.to_sql("arrivals",con, index=False, if_exists="append")
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
