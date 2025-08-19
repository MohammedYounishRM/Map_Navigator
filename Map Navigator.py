#File Importing Required Files
import openrouteservice
import folium
import tkinter as tk
from tkinter import simpledialog

#Getting The Input Field
root = tk.Tk()
root.withdraw()

#Getting API Key
Key = 'eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6IjVjNzRiYmJlOGQ4YzRkYTdiNmFkYmQxNGU2NTk4NjEyIiwiaCI6Im11cm11cjY0In0='

#Client Creation
client = openrouteservice.Client(Key)

#User Inupts
start = simpledialog.askstring("Start Location", "Enter Your Starting Place:")
end = simpledialog.askstring("Destination", "Enter Your Destination:")

#Getting Code For Start
start_place = client.pelias_search(start)
start_coords = start_place['features'][0]['geometry']['coordinates']
start_lat = start_coords[1]
start_lon = start_coords[0]

#Getting Code For End
end_place = client.pelias_search(end)
end_coords = end_place['features'][0]['geometry']['coordinates']
end_lat = end_coords[1]
end_lon = end_coords[0]

#Routes
route = client.directions(
    coordinates = [start_coords, end_coords], profile = 'driving-car', format='geojson')

#Distance Calculation
dist_m = route['features'][0]['properties']['segments'][0]['distance']
dist_km = round(dist_m/1000, 2)

#Map Gen
map_cre = folium.Map(location=[start_lat, start_lon], zoom_start = 10)

#Route Draw
folium.GeoJson(route).add_to(map_cre)

#save
map_cre.save("Map_Create.html")

print("Map Created Succesfully!")
print(f"Starting Place:{start}")
print(f"Destination:{end}")
print(f" Total Distance Is {dist_km} km")
