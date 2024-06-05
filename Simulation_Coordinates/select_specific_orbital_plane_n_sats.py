import numpy as np
from math import radians, sin, cos, sqrt, atan2

# Haversine function to calculate surface distance
def haversine(coord1, coord2):
    R = 6371.0  # Earth radius in kilometers
    lat1, lon1 = radians(coord1[0]), radians(coord1[1])
    lat2, lon2 = radians(coord2[0]), radians(coord2[1])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

# Coordinates of the satellites (latitude, longitude, altitude)
satellite_coords = [
    (21.1117, -68.6274, 539633.3643),
    (22.6876, -69.6045, 547383.9135),
    (14.5233, -76.633, 529571.5646),
    (-43.8941, 135.0381, 555414.1922),
    # (47.9881, -30.1253, 500936.9828),
    (-52.0145, 168.5322, 571056.6174),
    (37.0698, -53.4182, 549164.2787),
    (-49.7403, 156.079, 557836.64),
    # (46.3675, 42.9695, 526714.9723),
    (39.0812, -48.1739, 542741.8925),
    # (-9.2814, 100.6512, 503860.5065),
    (22.213, 77.0078, 540217.7929),
    (-15.7274, 101.5155, 544387.4366),
    (25.1349, -64.8374, 540251.1958),
    # (-36.495, -119.4908, 511212.3482),
    # (29.7296, 69.092, 442303.6204),
    (53.0263, 8.6921, 552843.729),
    # (-10.1097, 99.9716, 487704.6206),
    # (9.9685, -78.5017, 499708.9707),
    (24.5067, 72.2375, 547597.1669),
    # (14.944, 82.924, 509638.717),
    (-53.3227, -172.2302, 559158.361),
    (-48.3533, 149.4275, 564735.6571),
    (-39.2682, 132.1211, 553717.035),
    (-9.0636, -94.6767, 550004.3765),
    (-47.4294, 149.0814, 557063.4593),
    # (13.327, 84.2241, 509819.2732),
    # (39.4734, -47.4544, 511702.4063),
    (-24.6719, -107.9181, 554849.6504),
    (-11.6829, 100.2829, 550613.0446),
    (-51.8513, 167.4315, 571752.7437),
    # (-48.4555, -145.0613, 478734.922),
    (6.9571, -82.5895, 547210.3266),
    # (40.9521, -45.7082, 504885.6918)
]


# Function to select the next satellite based on surface distance
def select_next(selected, remaining, coords):
    max_min_dist = -1
    next_sat = None
    for i in remaining:
        min_dist = min(haversine(coords[i], coords[j]) for j in selected)
        if min_dist > max_min_dist:
            max_min_dist = min_dist
            next_sat = i
    return next_sat

# Initialize the selection with the first satellite
selected = [18] #Change to get maximum spread out 
remaining = list(range(1, len(satellite_coords)))

# Select the remaining 4 satellites
for _ in range(3):
    next_sat = select_next(selected, remaining, satellite_coords)
    selected.append(next_sat)
    remaining.remove(next_sat)

# Get the selected satellites' coordinates
selected_coords = [satellite_coords[i] for i in selected]

# Print the selected coordinates
for i, coord in enumerate(selected_coords):
    print(f"Satellite {i+1}: {coord}")

# Optionally, save the selected coordinates to a file
with open('selected_satellites.txt', 'w') as f:
    for coord in selected_coords:
        f.write(f"{coord}\n")
