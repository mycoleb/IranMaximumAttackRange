#Yes I made this.
import folium
import geopandas as gpd


# Load map data directly 
world_url = "https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson"
print("Downloading map data...")
world = gpd.read_file(world_url)


# Extract Iran's geometry


iran = world[world['ADMIN'] == 'Iran'] if 'ADMIN' in world.columns else world[world['name'] == 'Iran']
iran_geom = iran.geometry.iloc[0]


# Create a 2500km buffer


iran_projected = iran.to_crs("ESRI:54032")
buffer_projected = iran_projected.buffer(2500000) 
buffer_wgs84 = buffer_projected.to_crs("EPSG:4326")


#  Initialize Folium
m = folium.Map(location=[35, 20], zoom_start=3)



folium.GeoJson(
    iran_geom,
    style_function=lambda x: {'fillColor': 'red', 'color': 'red', 'weight': 2}
).add_to(m)


#  Add the 2500km Buffer 
folium.GeoJson(
    buffer_wgs84,
    name="2500km Border Range",
    style_function=lambda x: {
        'fillColor': '#ff4b4b',
        'color': '#ff4b4b',
        'weight': 1,
        'fillOpacity': 0.3
    }
).add_to(m)


#  Add California Marker 
folium.Marker(
    #optional Swidnica, Poland 50.8498° N, 16.4757° E
    #Los Angeles coordinates
    [34.0549, -118.2426], 
    popup="California (USA)",
    icon=folium.Icon(color='blue', icon='cloud')
).add_to(m)


#  Save and finish
m.save('iran_range_map.html')
print("Success! Open iran_range_map.html in your browser to see the results. Thank you for visiting my github github.com/mycoleb")
