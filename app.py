import streamlit as st
import openrouteservice
import folium
from streamlit_folium import st_folium

# OpenRouteService API Key
API_key = st.secrets["ORS_API_KEY"]  # use Streamlit secrets instead of hardcoding
client = openrouteservice.Client(key=API_key)

st.set_page_config(page_title="Route Map Generator", layout="centered")
st.title("🗺️🗺 Route Map Generator")
st.markdown("Enter your origin and destination to find the route.")

origin = st.text_input("From:")
destination = st.text_input("To:")

# Store map in session state
if "map_obj" not in st.session_state:
    st.session_state.map_obj = None

if st.button("Generate Map") and origin and destination:
    try:
        origin_result = client.pelias_search(text=origin)
        origin_coords = origin_result['features'][0]['geometry']['coordinates']

        destination_result = client.pelias_search(text=destination)
        destination_coords = destination_result['features'][0]['geometry']['coordinates']

        route = client.directions(
            coordinates=[origin_coords, destination_coords],
            profile='driving-car',
            format='geojson'
        )

        distance_meters = route['features'][0]['properties']['segments'][0]['distance']
        distance_km = round(distance_meters / 1000, 2)
        map_route = folium.Map(location=[origin_coords[1], origin_coords[0]], zoom_start=10)

        folium.GeoJson(route).add_to(map_route)
        folium.Marker([origin_coords[1], origin_coords[0]], tooltip="Origin", icon=folium.Icon(color='green')).add_to(map_route)
        folium.Marker([destination_coords[1], destination_coords[0]], tooltip="Destination", icon=folium.Icon(color='red')).add_to(map_route)

        steps = route['features'][0]['properties']['segments'][0]['steps']
        for idx, step in enumerate(steps):
            lat, lon = step['way_points'][0], step['way_points'][-1]
            coord = route['features'][0]['geometry']['coordinates'][lat]
            folium.Marker(
                    location=[coord[1], coord[0]],
                    icon=folium.Icon(color='green', icon='info-sign'),
                    tooltip=f"{idx + 1}. {step['instruction']}"
                ).add_to(map_route)

        # Save map to session state
        st.session_state.map_obj = map_route

        st.success(f"Distance: {distance_km} km")

    except Exception as e:
        st.error(f"Error: {e}")

# Always display stored map if available
if st.session_state.map_obj:
    st_folium(st.session_state.map_obj, width=700, height=500)
