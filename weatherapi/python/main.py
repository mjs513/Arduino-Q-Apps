from arduino.app_bricks.streamlit_ui import st
from arduino.app_utils import *

import urllib.request
import urllib.error
import urllib.parse
import pandas as pd
import streamlit as st
from io import StringIO

# Constants
API_KEY = 'PDPQPL3X6BUCGHR76HQW2CT9F'
BASE_URL = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/'

# Function to fetch weather data
def get_weather_data(location):
    encoded_location = urllib.parse.quote(location)
    query_parameters = {
        'unitGroup': 'us',
        'contentType': 'csv',
        'include': 'days',
        'key': API_KEY
    }
    query_url = f"{BASE_URL}{encoded_location}/next7days?"
    query_url += '&'.join([f"{key}={value}" for key, value in query_parameters.items()])
    try:
        response = urllib.request.urlopen(query_url)
        csv_data = response.read().decode('utf-8')
        df = pd.read_csv(StringIO(csv_data))
        return df, None
    except urllib.error.HTTPError as e:
        return None, f"HTTP Error {e.code}: {e.read().decode()}"
    except urllib.error.URLError as e:
        return None, f"URL Error: {e.reason}"
    except Exception as e:
        return None, f"Unexpected error: {e}"

def main():
    # Streamlit UI
    st.title("7-Day Weather Forecast")
    
    location = st.text_input("Enter location (e.g., New York,NY)", "New York,NY")
    refresh = st.button("Refresh Data")
    
    if location and refresh:
        df, error = get_weather_data(location)
        if error:
            st.error(error)
        elif df is not None:
            st.subheader("Raw Forecast Data")
            st.dataframe(df)
    
            st.subheader("Select Data to Plot")
            options = {
                "Maximum Temperature (°F)": "tempmax",
                "Minimum Temperature (°F)": "tempmin",
                "Humidity (%)": "humidity",
                "Wind Speed (mph)": "windspeed",
                "Precipitation (in)": "precip"
            }
    
            selected_columns = [col for label, col in options.items() if st.checkbox(label, value=(col in ["tempmax", "tempmin"]))]
    
            if selected_columns:
                st.subheader("Weather Trends")
                st.line_chart(df.set_index('datetime')[selected_columns])
            else:
                st.info("Please select at least one data element to visualize.")


if __name__ == "__main__":
    main()
