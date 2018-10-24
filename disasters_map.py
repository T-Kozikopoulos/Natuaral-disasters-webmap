import pandas as pd
import folium
from folium.plugins import FloatImage


# Import the datasets and set up column variables.
vol_data = pd.read_csv('volcanoes.csv')
vol_lat = list(vol_data['Latitude'])
vol_lon = list(vol_data['Longitude'])
vol_name = list(vol_data['Volcano Name'])
vol_elev = list(vol_data['Elev'])
vol_er = list(vol_data['Last Known Eruption'])

quake_data = pd.read_csv('earthquakes.csv')
quake_lat = list(quake_data['Latitude'])
quake_lon = list(quake_data['Longitude'])
quake_mag = list(quake_data['Magnitude'])
quake_date = list(quake_data['Date'])

tsu_data = pd.read_csv('tsunamis.csv')
tsu_lat = list(tsu_data['LATITUDE'])
tsu_lon = list(tsu_data['LONGITUDE'])
tsu_dc = list(tsu_data['DEATHS'])
tsu_max = list(tsu_data['MAXIMUM_WATER_HEIGHT'])
tsu_date = list(tsu_data['YEAR'])


# Center the map.
map = folium.Map(location=[25.5, -32.5], zoom_start=3, tiles='Mapbox Control Room')

# Create the layer groups.
fg_vol = folium.FeatureGroup(name='Volcanoes')
fg_quake = folium.FeatureGroup(name='Earthquakes (6+)')
fg_tsu = folium.FeatureGroup(name='Tsunamis')


# Use location data to set up markers on the map, add some useful info to them.
def vol_popup(na, el, er):
    return folium.Popup('<{}>, Height: {}m, Last eruption: {}'.format(na, str(el)[:2], er),
                        parse_html=True)


for lt, ln, na, el, er in zip(vol_lat, vol_lon, vol_name, vol_elev, vol_er):
    fg_vol.add_child(folium.RegularPolygonMarker(location=[lt, ln],
                                                 popup=vol_popup(na, el, er),
                                                 color='black', fill_color='red',
                                                 radius=8, fill_opacity=.65))


# Do the same the volcano data, but use different colors.
def quake_popup(mgn, da):
    return folium.Popup('Magnitude: {} <br> {}'.format(mgn, da))


for lt, ln, mgn, da in zip(quake_lat, quake_lon, quake_mag, quake_date):
    fg_quake.add_child(folium.RegularPolygonMarker(location=[lt, ln],
                                                   popup=quake_popup(mgn, da),
                                                   color='black', fill_color='darkgreen',
                                                   radius=8, fill_opacity=.65))


# Same as above.
def tsu_popup(dc, max, da):
    return folium.Popup('Height: {}m, Deaths: {}, Year: {}'.format(str(max), str(dc), str(int(da))),
                        parse_html=True)


for lt, ln, dc, max, da in zip(tsu_lat, tsu_lon, tsu_dc, tsu_max, tsu_date):
    fg_tsu.add_child(folium.RegularPolygonMarker(location=[lt, ln],
                                                 popup=tsu_popup(dc, max, da),
                                                 color='black', fill_color='blue',
                                                 radius=8, fill_opacity=.65))

# Add the layers to the map and allow users to toggle them on/off.
map.add_child(fg_vol)
map.add_child(fg_tsu)
map.add_child(fg_quake)
map.add_child(folium.LayerControl())

# Finally, add the legend.
legend = 'legend.png'
FloatImage(legend, bottom=2, left=2).add_to(map)

# All done!
map.save('map.html')
