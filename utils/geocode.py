from geopy.geocoders import Nominatim
from geopy.exc import GeocoderUnavailable, GeocoderTimedOut

geolocator = Nominatim(user_agent="smartserve_app", timeout=10)

def get_coordinates(location):
    try:
        result = geolocator.geocode(location)
        if result:
            return result.latitude, result.longitude
        return None, None
    except (GeocoderUnavailable, GeocoderTimedOut):
        return None, None
    except Exception:
        return None, None
