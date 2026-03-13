import folium
import geopandas as gpd

# 1. Load map data directly from a URL to avoid the deprecation error
world_url = "https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson"
print("Downloading map data...")
world = gpd.read_file(world_url)

# 2. Extract Iran's geometry
# Some datasets use 'name', others use 'ADMIN'. Adjusting for compatibility:
iran = world[world['ADMIN'] == 'Iran'] if 'ADMIN' in world.columns else world[world['name'] == 'Iran']
iran_geom = iran.geometry.iloc[0]

# 3. Create a 2500km buffer
# We project to World Azimuthal Equidistant (ESRI:54032) to do math in meters
iran_projected = iran.to_crs("ESRI:54032")
buffer_projected = iran_projected.buffer(2500000) 
buffer_wgs84 = buffer_projected.to_crs("EPSG:4326")

# 4. Initialize Folium Map (OpenStreetMap)
m = folium.Map(location=[35, 20], zoom_start=3)

# 5. Add Iran (Red)
folium.GeoJson(
    iran_geom,
    style_function=lambda x: {'fillColor': 'red', 'color': 'red', 'weight': 2}
).add_to(m)

# 6. Add the 2000km Buffer (Shaded Red/Orange)
folium.GeoJson(
    buffer_wgs84,
    name="2000km Border Range",
    style_function=lambda x: {
        'fillColor': '#ff4b4b',
        'color': '#ff4b4b',
        'weight': 1,
        'fillOpacity': 0.3
    }
).add_to(m)

# 7. Add California Marker for scale
folium.Marker(
    [34.0522, -118.2437], 
    popup="California (USA)",
    icon=folium.Icon(color='blue', icon='cloud')
).add_to(m)

# 8. Save and finish
m.save('iran_range_map.html')
print("Success! Open iran_range_map.html in your browser to see the results.")