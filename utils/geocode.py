import requests

def get_coordinates(location: str):
    if not location or location.strip() == "":
        return None, None

    try:
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": location,
            "format": "json",
            "limit": 1
        }

        headers = {
            "User-Agent": "SmartServeGIS/1.0 (contact: admin@smartserve)"
        }

        response = requests.get(url, params=params, headers=headers, timeout=10)

        if response.status_code != 200:
            return None, None

        data = response.json()

        if not data:
            return None, None

        return float(data[0]["lat"]), float(data[0]["lon"])

    except Exception:
        return None, None
