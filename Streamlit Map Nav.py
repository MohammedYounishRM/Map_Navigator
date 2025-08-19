import os
import streamlit as st
from streamlit_folium import st_folium
import folium
import openrouteservice

st.set_page_config(page_title="Route Map Generator", layout="centered")
st.title("🗺️ Route Map Generator")
st.markdown("Enter your origin and destination to find the route.")

# inputs
origin = st.text_input("From:")
destination = st.text_input("To:")

# API key
api_key = st.secrets.get("ORS_API_KEY", os.getenv("ORS_API_KEY", ""))
client = openrouteservice.Client(key=api_key) if api_key else None

# store map in session state
if "map_obj" not in st.session_state:
    st.session_state["map_obj"] = None

if st.button("Generate Map"):
    if not origin or not destination:
        st.error("Please enter both origin and destination.")
    elif not client:
        st.error("Missing ORS_API_KEY in Streamlit Secrets.")
    else:
        try:
            # geocode
            o_res = client.pelias_search(text=origin)
            d_res = client.pelias_search(text=destination)
            o = o_res["features"][0]["geometry"]["coordinates"]  # [lon, lat]
            d = d_res["features"][0]["geometry"]["coordinates"]

            # route
            route = client.directions(
                coordinates=[o, d],
                profile="driving-car",
                format="geojson"
            )

            distance_m = route["features"][0]["properties"]["segments"][0]["distance"]
            st.success(f"Distance: {round(distance_m/1000, 2)} km")

            # map
            center = [(o[1]+d[1])/2, (o[0]+d[0])/2]
            m = folium.Map(location=center, zoom_start=8)
            folium.GeoJson(route).add_to(m)
            folium.Marker([o[1], o[0]], tooltip="Origin").add_to(m)
            folium.Marker([d[1], d[0]], tooltip="Destination").add_to(m)

            # save map to session
            st.session_state["map_obj"] = m

        except Exception as e:
            st.error(f"Could not compute route: {e}")

# show map if exists
if st.session_state["map_obj"]:
    st_folium(st.session_state["map_obj"], width=800, height=500)
