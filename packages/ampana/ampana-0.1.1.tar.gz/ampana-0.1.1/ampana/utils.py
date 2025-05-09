import requests

def detect_city_from_ip():
    """Try to detect user's city based on their IP address."""
    try:
        response = requests.get("http://ip-api.com/json/").json()
        return response.get("city")
    except Exception:
        return None
