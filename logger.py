import csv
import os

# Define the path to the log file
LOG_FILE = "data/user_logs.csv"

def log_user_input(input_type, distance, elevation, surface, matched_route, username="anonymous"):
    """
    Logs a user's input and matched route to a CSV file.

    Parameters:
        input_type (str): 'gpx' or 'manual'
        distance (float or int): Route distance in km
        elevation (float or int): Elevation gain in meters
        surface (str): Surface type ('Paved', 'Gravel', etc.)
        matched_route (str): Name of the matched route or 'Uploaded GPX File'
        username (str): Username of the user (default: 'anonymous')
    """
    # Check if the file already exists
    log_exists = os.path.isfile(LOG_FILE)

    # Ensure the data folder exists
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    # Open the file in append mode
    with open(LOG_FILE, mode="a", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Write headers if this is the first time writing to the file
        if not log_exists:
            writer.writerow(["username", "input_type", "distance", "elevation", "surface", "matched_route"])

        # Write the actual log entry
        writer.writerow([username, input_type, distance, elevation, surface, matched_route])
