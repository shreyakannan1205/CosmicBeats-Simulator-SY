import numpy as np
import plotly.graph_objects as go
from math import radians, sin, cos, sqrt, atan2

# Example satellite coordinates (latitude, longitude)
satellite_coords = [

(21.1117, -68.6274),
(22.6876, -69.6045),
(14.5233, -76.633),
(-43.8941, 135.0381),
(47.9881, -30.1253),
(-52.0145, 168.5322),
(37.0698, -53.4182),
(-49.7403, 156.079),
(46.3675, 42.9695),
(39.0812, -48.1739),
(-9.2814, 100.6512),
(22.213, 77.0078),
(-15.7274, 101.5155),
(25.1349, -64.8374),
(-36.495, -119.4908),
(29.7296, 69.092),
(53.0263, 8.6921),
(-10.1097, 99.9716),
(9.9685, -78.5017),
(24.5067, 72.2375),
(14.944, 82.924),
(-53.3227, -172.2302),
(-48.3533, 149.4275),
(-39.2682, 132.1211),
(-9.0636, -94.6767),
(-47.4294, 149.0814),
(13.327, 84.2241),
(39.4734, -47.4544),
(-24.6719, -107.9181),
(-11.6829, 100.2829),
(-51.8513, 167.4315),
(-48.4555, -145.0613),
(6.9571, -82.5895),
(40.9521, -45.7082),


]

# Satellite 1 and Satellite 3: 10060.59 km
# Satellite 1 and Satellite 4: 9418.87 km
# Satellite 2 and Satellite 3: 9930.31 km
# Satellite 2 and Satellite 4: 10620.40 km

# (-24.6719, -107.9181), 
# (24.5067, 72.2375),
# (-43.8941, 135.0381),
# (39.0812, -48.1739)

# 29 (alone), 20 (almost alone - close to 16 and 12), 4 (almost alone - close to 24), 10 (close to 28)
# 28: (39.4734, -47.4544, 511702.4063) -> STARLINK-30404 (diffheight) Altitude = 516.47 km
# 24: (-39.2682, 132.1211, 553717.035) Height similar to original 
# 16: (29.7296, 69.092, 442303.6204) -> STARLINK-1421 Altitude = 441.72 km
# 12: (22.213, 77.0078, 540217.7929) -> Height similar to original 

# Radius of Earth in kilometers
R = 6371.0

# Function to calculate the great-circle distance between two points
def haversine(coord1, coord2):
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    
    lat1, lon1 = radians(lat1), radians(lon1)
    lat2, lon2 = radians(lat2), radians(lon2)
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    distance = R * c
    return distance

# Calculate distances between each pair of satellites
distances = {}
for i in range(len(satellite_coords)):
    for j in range(i + 1, len(satellite_coords)):
        dist = haversine(satellite_coords[i], satellite_coords[j])
        distances[(i + 1, j + 1)] = dist

# Print distances
print("Great-circle distances between satellites (in km):")
for pair, distance in distances.items():
    print(f"Satellite {pair[0]} and Satellite {pair[1]}: {distance:.2f} km")

# Extract latitudes and longitudes
lats = [coord[0] for coord in satellite_coords]
lons = [coord[1] for coord in satellite_coords]

# Convert lat/lon to radians
lats_rad = np.radians(lats)
lons_rad = np.radians(lons)

# Convert spherical coordinates to Cartesian coordinates (on the Earth's surface)
x = R * np.cos(lats_rad) * np.cos(lons_rad)
y = R * np.cos(lats_rad) * np.sin(lons_rad)
z = R * np.sin(lats_rad)

# Generate a sphere to represent Earth
u, v = np.mgrid[0:2*np.pi:100j, 0:np.pi:50j]
earth_x = R * np.cos(u) * np.sin(v)
earth_y = R * np.sin(u) * np.sin(v)
earth_z = R * np.cos(v)

# Create a 3D scatter plot
fig = go.Figure()

# Plot Earth as a surface
fig.add_trace(go.Surface(
    x=earth_x,
    y=earth_y,
    z=earth_z,
    colorscale='Blues',
    opacity=0.7,
    showscale=False,
    name='Earth'
))

# Plot satellites
fig.add_trace(go.Scatter3d(
    x=x, y=y, z=z,
    mode='markers+text',
    marker=dict(size=5, color='red'),
    text=[f'Satellite {i+1}' for i in range(len(satellite_coords))],
    name='Satellites'
))

# Add layout details
fig.update_layout(
    title='3D Visualization of Satellites Projected on Earth',
    scene=dict(
        xaxis=dict(title='X (km)'),
        yaxis=dict(title='Y (km)'),
        zaxis=dict(title='Z (km)'),
        aspectratio=dict(x=1, y=1, z=1),
        camera_eye=dict(x=1.5, y=1.5, z=1.5)
    )
)

fig.show()
