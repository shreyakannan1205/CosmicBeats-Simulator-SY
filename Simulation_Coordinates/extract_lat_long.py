import re

# Read the input file
with open('output_coordinates_2.txt', 'r') as file:
    data = file.read()

# Regular expression to match the latitude and longitude values
pattern = re.compile(r'\((\-?\d+\.\d+), (\-?\d+\.\d+), \-?\d+\.\d+\)')

# Find all matches in the file
matches = pattern.findall(data)

# Convert matches to the desired format
coordinates = [(float(lat), float(long)) for lat, long in matches]

# Save the coordinates to a file
with open('lat_long.txt', 'w') as file:
    file.write(str(coordinates))

print("Coordinates have been saved to output.txt")
