import requests
import os
from dotenv import load_dotenv
from ampana.utils import detect_city_from_ip

# Load the .env file for API key
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_weather(city=None):
    """Fetches weather and adds a snarky comment."""
    if not city:
        city = detect_city_from_ip()
    if not city:
        return "Ugh. I couldn't even find where you are. So basic."

    # Fetch weather data from OpenWeather API
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={API_KEY}"
        data = requests.get(url).json()
        temp = data['main']['temp']
        description = data['weather'][0]['description']
        return format_weather(temp, description, city)
    except Exception:
        return "Something went wrong... try again, darling."

def format_weather(temp, description, city):
    """Formats weather information with a sassy comment."""
    if temp > 30:
        sass = "Hotter than your last situation. Hydrate, queen."
    elif temp < 10:
        sass = "Colder than your social media comments."
    elif "rain" in description:
        sass = "Rainy days are for cute umbrellas and wet shoes."
    else:
        sass = f"Mostly {description}. Meh. Whatever"
    return f"It's {temp}°C. {sass}"
