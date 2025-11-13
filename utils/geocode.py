from geopy.geocoders import Nominatim
import time

geolocator = Nominatim(user_agent="smartserve")

def get_coordinates(location: str):
    """
    Converts a text location (e.g., 'Kempton Park')
    into (latitude, longitude)
    """
    if not location:
        return None, None

    try:
        # delay helps prevent server rate limit issues
        time.sleep(1)
        place = geolocator.geocode(location)
        if place:
            print(f"✅ Geocoded {location}: ({place.latitude}, {place.longitude})")
            return place.latitude, place.longitude
        else:
            print(f"⚠️ No match found for: {location}")
            return None, None
    except Exception as e:
        print(f"❌ Geocoding error: {e}")
        return None, None
