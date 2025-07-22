import streamlit as st
from streamlit_folium import folium_static
import folium
import plotly.graph_objects as go

from matcher import match_route
from ors_utils import get_route, plot_route_on_map, generate_round_trip
from utils.gpx_utils import parse_gpx_file
from logger import log_user_input

st.set_page_config(page_title="Route Finder", layout="wide")
st.title("🚴 Route Finder (Europe)")

# Ask for username once at the top for personalization
username = st.text_input("Enter your name (for personalization):", "")
if not username:
    st.warning("Please enter your name to continue.")
    st.stop()

option = st.radio("Choose input method:", ["Upload GPX File", "Manual Entry"])

# --- Manual Entry Section ---
if option == "Manual Entry":
    distance = st.number_input("Distance (km)", min_value=1.0, step=0.5)
    elevation = st.number_input("Elevation Gain (m)", min_value=0.0, step=10.0)
    surface = st.selectbox("Surface Type", ["Any", "Paved", "Gravel", "Mixed"])

    st.subheader("🔎 Find a Similar Route")
    if st.button("Find Match from Local GPX Files"):
        result = match_route(distance, elevation, surface)
        st.info(result)
        log_user_input(username, "manual", distance, elevation, surface, result)

    st.subheader("🌐 Get Live Route (via OpenRouteService)")
    start = st.text_input("Start location (lon,lat)", "13.388860,52.517037")
    end = st.text_input("End location (lon,lat)", "13.427555,52.504049")

    if st.button("Get Route from ORS"):
        try:
            start_coords = list(map(float, start.split(",")))
            end_coords = list(map(float, end.split(",")))
            route = get_route([start_coords, end_coords])
            if route:
                st.success("Route fetched from ORS!")
                map_ = plot_route_on_map(route, center=[
                    (start_coords[1] + end_coords[1]) / 2,
                    (start_coords[0] + end_coords[0]) / 2
                ])
                folium_static(map_)
                log_user_input(username, "manual", distance, elevation, surface, "ORS Route")
            else:
                st.error("No route returned.")
        except:
            st.error("Invalid coordinates format. Use 'lon,lat'")

    st.subheader("🔁 Generate Similar Route via ORS (Manual Entry)")
    manual_midpoint = st.text_input("Enter city center or midpoint coordinates (lon,lat)", "13.4050,52.5200")  # Berlin default

    if st.button("Generate ORS Round Trip"):
        try:
            center_coords = list(map(float, manual_midpoint.split(",")))  # [lon, lat]
            route = generate_round_trip(center_coords, distance)

            if route:
                st.success("Similar route generated using ORS!")
                sim_map = plot_route_on_map(route, center=[center_coords[1], center_coords[0]])  # [lat, lon]
                folium_static(sim_map)
                log_user_input(username, "manual", distance, elevation, surface, "ORS RoundTrip Manual")
            else:
                st.error("ORS failed to generate a route. Try adjusting coordinates or distance.")
        except:
            st.error("Invalid format. Use 'lon,lat'")

# --- GPX Upload Section ---
else:
    uploaded_file = st.file_uploader("Upload your GPX file", type="gpx")
    if uploaded_file:
        st.success("GPX uploaded successfully!")

        parsed = parse_gpx_file(uploaded_file)

        st.subheader("📊 Route Summary")
        st.write(f"**Distance:** {parsed['distance']:.2f} km")
        st.write(f"**Elevation Gain:** {parsed['elevation_gain']} m")

        # Elevation Profile
        st.subheader("📈 Elevation Profile")
        distances, elevations = zip(*parsed["elevation_profile"])
        fig = go.Figure(data=go.Scatter(x=distances, y=elevations, mode='lines', line=dict(color='green')))
        fig.update_layout(title="Elevation vs Distance", xaxis_title="Distance (km)", yaxis_title="Elevation (m)")
        st.plotly_chart(fig, use_container_width=True)

        # Route Map
        st.subheader("🗺️ Route Map")
        coords = parsed.get("coordinates", [])
        if coords:
            midpoint = coords[len(coords) // 2]
            map_ = folium.Map(location=midpoint, zoom_start=13)
            folium.PolyLine(coords, color="blue", weight=4).add_to(map_)
            folium_static(map_)
        else:
            st.warning("No coordinates available for visualization.")

        # Suggest Similar Route via ORS
        st.subheader("🔁 Suggest Similar Route via ORS")
        if st.button("Generate Similar Route"):
            midpoint = parsed["coordinates"][len(parsed["coordinates"]) // 2]  # [lat, lon]
            center = [midpoint[1], midpoint[0]]  # Convert to [lon, lat] for ORS
            distance_km = parsed["distance"]
            route = generate_round_trip(center, distance_km)

            if route:
                st.success("Similar route fetched using ORS!")
                sim_map = plot_route_on_map(route, center=[midpoint[0], midpoint[1]])
                folium_static(sim_map)
                log_user_input(username, "gpx", distance_km, parsed["elevation_gain"], "From GPX", "ORS RoundTrip")
            else:
                st.error("ORS could not generate a similar route.")
