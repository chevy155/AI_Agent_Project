# agents/weather_agent.py
# Weather Agent: Fetches and displays weather information for Del Mar, California

import requests
import json
from datetime import datetime

def get_weather_delmar(use_mock=False):
    """
    Fetches current weather data for Del Mar, California.
    Uses wttr.in service which provides free weather data without API key.
    
    Args:
        use_mock: If True, returns mock data (useful for testing without internet)
    
    Returns:
        str: Formatted weather report or error message
    """
    print("--- Running Weather Agent: Del Mar, California ---")
    
    # If mock mode or if we can't connect, use sample data
    if use_mock:
        return get_mock_weather_delmar()
    
    try:
        # Del Mar, California coordinates
        location = "Del+Mar,California"
        
        # Using wttr.in API for weather data (free, no API key needed)
        url = f"https://wttr.in/{location}?format=j1"
        
        print(f"Fetching weather data from: {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        weather_data = response.json()
        
        # Extract current conditions
        current = weather_data.get('current_condition', [{}])[0]
        nearest_area = weather_data.get('nearest_area', [{}])[0]
        
        # Format the weather report
        report = format_weather_report(current, nearest_area, weather_data)
        
        print("Weather data fetched successfully.")
        return report
        
    except requests.exceptions.RequestException as e:
        print(f"Warning: Failed to fetch live weather data: {e}")
        print("Falling back to mock weather data for demonstration...")
        return get_mock_weather_delmar()
    except Exception as e:
        print(f"Warning: Unexpected error occurred: {e}")
        print("Falling back to mock weather data for demonstration...")
        return get_mock_weather_delmar()


def get_mock_weather_delmar():
    """
    Returns mock weather data for Del Mar, California.
    This is used when internet connection is unavailable.
    
    Returns:
        str: Formatted weather report with sample data
    """
    print("Using mock weather data for demonstration purposes...")
    
    # Get today's date
    today = datetime.now().strftime("%A, %B %d, %Y")
    
    # Mock weather data representing typical Del Mar weather
    report = f"""
{'='*60}
WEATHER REPORT FOR DEL MAR, CALIFORNIA
{'='*60}

Location: Del Mar, San Diego County, California, USA
Date: {today}

CURRENT CONDITIONS:
------------------
Weather: Partly cloudy
Temperature: 72°F (22°C)
Feels Like: 70°F (21°C)
Humidity: 65%
Wind: 8 mph from W
UV Index: 6
Visibility: 10 miles
Pressure: 1013 mb
Cloud Cover: 25%

TODAY'S FORECAST:
-----------------
High: 75°F (24°C)
Low: 62°F (17°C)
Average: 68°F (20°C)

HOURLY HIGHLIGHTS:
------------------
9:00 AM: 68°F - Sunny
12:00 PM: 73°F - Partly cloudy
6:00 PM: 70°F - Partly cloudy

{'='*60}

Note: This is demonstration data. Del Mar typically enjoys a mild 
Mediterranean climate with comfortable temperatures year-round, 
coastal breezes, and low rainfall. For live weather data, ensure 
internet connectivity is available.

{'='*60}
"""
    
    return report


def format_weather_report(current, area, full_data):
    """
    Formats weather data into a readable report.
    
    Args:
        current: Current weather conditions
        area: Location information
        full_data: Full weather data including forecast
        
    Returns:
        str: Formatted weather report
    """
    # Extract location info
    area_name = area.get('areaName', [{}])[0].get('value', 'Del Mar')
    region = area.get('region', [{}])[0].get('value', 'California')
    country = area.get('country', [{}])[0].get('value', 'USA')
    
    # Extract current conditions
    temp_f = current.get('temp_F', 'N/A')
    temp_c = current.get('temp_C', 'N/A')
    feels_like_f = current.get('FeelsLikeF', 'N/A')
    feels_like_c = current.get('FeelsLikeC', 'N/A')
    humidity = current.get('humidity', 'N/A')
    weather_desc = current.get('weatherDesc', [{}])[0].get('value', 'N/A')
    wind_speed = current.get('windspeedMiles', 'N/A')
    wind_dir = current.get('winddir16Point', 'N/A')
    uv_index = current.get('uvIndex', 'N/A')
    visibility = current.get('visibilityMiles', 'N/A')
    pressure = current.get('pressure', 'N/A')
    cloud_cover = current.get('cloudcover', 'N/A')
    
    # Get today's date
    today = datetime.now().strftime("%A, %B %d, %Y")
    
    # Build the report
    report = f"""
{'='*60}
WEATHER REPORT FOR DEL MAR, CALIFORNIA
{'='*60}

Location: {area_name}, {region}, {country}
Date: {today}

CURRENT CONDITIONS:
------------------
Weather: {weather_desc}
Temperature: {temp_f}°F ({temp_c}°C)
Feels Like: {feels_like_f}°F ({feels_like_c}°C)
Humidity: {humidity}%
Wind: {wind_speed} mph from {wind_dir}
UV Index: {uv_index}
Visibility: {visibility} miles
Pressure: {pressure} mb
Cloud Cover: {cloud_cover}%

"""
    
    # Add forecast if available
    if 'weather' in full_data and len(full_data['weather']) > 0:
        report += "TODAY'S FORECAST:\n"
        report += "-" * 16 + "\n"
        
        today_forecast = full_data['weather'][0]
        max_temp_f = today_forecast.get('maxtempF', 'N/A')
        max_temp_c = today_forecast.get('maxtempC', 'N/A')
        min_temp_f = today_forecast.get('mintempF', 'N/A')
        min_temp_c = today_forecast.get('mintempC', 'N/A')
        avg_temp_f = today_forecast.get('avgtempF', 'N/A')
        avg_temp_c = today_forecast.get('avgtempC', 'N/A')
        
        report += f"High: {max_temp_f}°F ({max_temp_c}°C)\n"
        report += f"Low: {min_temp_f}°F ({min_temp_c}°C)\n"
        report += f"Average: {avg_temp_f}°F ({avg_temp_c}°C)\n"
        
        # Add hourly breakdown if available
        if 'hourly' in today_forecast and len(today_forecast['hourly']) > 0:
            report += "\nHOURLY HIGHLIGHTS:\n"
            report += "-" * 18 + "\n"
            
            # Show a few key hours (morning, noon, evening)
            hours_to_show = [3, 6, 9]  # indices for 9AM, 12PM, 6PM approximately
            for idx in hours_to_show:
                if idx < len(today_forecast['hourly']):
                    hour_data = today_forecast['hourly'][idx]
                    time = hour_data.get('time', 'N/A')
                    if time != 'N/A' and len(time) >= 2:
                        # Convert time (e.g., "900" to "9:00 AM")
                        hour = int(time[:2]) if len(time) >= 2 else 0
                        period = "AM" if hour < 12 else "PM"
                        display_hour = hour if hour <= 12 else hour - 12
                        if display_hour == 0:
                            display_hour = 12
                        time_str = f"{display_hour}:00 {period}"
                    else:
                        time_str = time
                    
                    h_temp_f = hour_data.get('tempF', 'N/A')
                    h_desc = hour_data.get('weatherDesc', [{}])[0].get('value', 'N/A')
                    h_precip = hour_data.get('precipMM', 'N/A')
                    
                    report += f"{time_str}: {h_temp_f}°F - {h_desc}"
                    if h_precip != 'N/A' and float(h_precip) > 0:
                        report += f" (Precip: {h_precip}mm)"
                    report += "\n"
    
    report += "\n" + "=" * 60 + "\n"
    
    return report


# --- Example Usage ---
if __name__ == '__main__':
    print("Testing Weather Agent for Del Mar, California\n")
    weather_report = get_weather_delmar()
    print(weather_report)

