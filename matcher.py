# matcher.py
import os
from utils.gpx_utils import parse_gpx_file
from pathlib import Path

def load_sample_routes():
    folder = Path("data/sample_routes")
    routes = []

    for file in folder.glob("*.gpx"):
        try:
            data = parse_gpx_file(open(file, 'r'))
            routes.append({
                "name": file.name,
                "distance": data["distance"],
                "elevation": data["elevation_gain"],
                "surface": "Mixed",  # Optional: Improve later
                "file": file
            })
        except Exception as e:
            print(f"Failed to parse {file.name}: {e}")
    
    return routes

def match_route(user_distance, user_elevation, surface=None):
    sample_routes = load_sample_routes()
    
    best_match = None
    best_score = float("inf")

    for route in sample_routes:
        dist_diff = abs(route["distance"] - user_distance)
        elev_diff = abs(route["elevation"] - user_elevation)
        score = dist_diff + (elev_diff / 100)

        if score < best_score:
            best_score = score
            best_match = route

    if best_match:
        return f"Match found: {best_match['name']} ({round(best_match['distance'],1)} km, {round(best_match['elevation'],0)} m)"
    else:
        return "No suitable match found."
