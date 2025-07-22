import gpxpy
import math

def haversine(coord1, coord2):
    # Approximate Earth radius in km
    R = 6371
    lat1, lon1 = map(math.radians, coord1)
    lat2, lon2 = map(math.radians, coord2)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2)
    return 2 * R * math.asin(math.sqrt(a))

def parse_gpx_file(file):
    import gpxpy
    gpx = gpxpy.parse(file)
    total_distance = 0
    total_elevation_gain = 0
    prev_point = None
    prev_elevation = None
    coordinates = []
    elevation_profile = []

    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                coord = (point.latitude, point.longitude)
                coordinates.append(coord)

                if prev_point:
                    distance_delta = haversine(prev_point, coord)
                    total_distance += distance_delta
                else:
                    distance_delta = 0

                if prev_elevation is not None and point.elevation > prev_elevation:
                    total_elevation_gain += point.elevation - prev_elevation

                elevation_profile.append((total_distance, point.elevation))
                prev_point = coord
                prev_elevation = point.elevation

    return {
        "distance": round(total_distance, 2),
        "elevation_gain": round(total_elevation_gain, 2),
        "coordinates": coordinates,
        "elevation_profile": elevation_profile
    }
