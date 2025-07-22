# ors_utils.py
import openrouteservice
import folium

API_KEY = "5b3ce3597851110001cf6248d71850273ae54679b7651409d492fc8c"  # <-- Replace with your actual ORS API key

client = openrouteservice.Client(key=API_KEY)

def get_route(coords):
    try:
        route = client.directions(
            coordinates=coords,
            profile='cycling-regular',
            format='geojson'
        )
        return route
    except Exception as e:
        print(f"Error fetching route: {e}")
        return None

def generate_round_trip(center_coords, distance_km, seed=1):
    """
    Generate a round-trip cycling route from ORS given a center coordinate and desired distance in km.
    """
    try:
        params = {
            "coordinates": [center_coords],
            "profile": "cycling-regular",
            "format": "geojson",
            "geometry": True,
            "options": {
                "round_trip": {
                    "length": distance_km * 1000,  # ORS expects meters
                    "points": 3,
                    "seed": seed
                }
            }
        }
        return client.directions(**params)
    except Exception as e:
        print(f"[ORS Round Trip Error]: {e}")
        return None

def plot_route_on_map(route, center=[52.52, 13.405]):
    m = folium.Map(location=center, zoom_start=13)
    folium.GeoJson(route, name="route").add_to(m)
    return m
