import os
from arduino.app_bricks.streamlit_ui import st
from arduino.app_utils import *

import pandas as pd
import openmeteo_requests
import requests_cache
from retry_requests import retry

def fetch_weather_data():
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 40.7654,
        "longitude": -73.8174,
        "hourly": ["temperature_2m", "pressure_msl", "surface_pressure"],
    }
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]

    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_pressure_msl = hourly.Variables(1).ValuesAsNumpy()
    hourly_surface_pressure = hourly.Variables(2).ValuesAsNumpy()

    hourly_data = {
        "date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left"
        ),
        "temperature_2m": hourly_temperature_2m,
        "pressure_msl": hourly_pressure_msl,
        "surface_pressure": hourly_surface_pressure
    }

    return pd.DataFrame(hourly_data)


def main():
    st.arduino_header("This is a test")
    st.title("📈 Open-Meteo Hourly Weather Visualization")
    st.write("Hello World")
    if st.button('Refresh Data'):
      df = fetch_weather_data()
      print(df)

if __name__ == "__main__":
    main()
