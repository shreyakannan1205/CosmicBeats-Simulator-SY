input_file = "distance.txt"  # Replace with your input file name
output_file = "distance_fixed.txt"  # Replace with your desired output file name

with open(input_file, 'r') as file:
    lines = file.readlines()

distances = []
for line in lines:
    if 'km' in line:  # Ensure 'km' is in the line
        parts = line.split()
        # Extract the number before "km" and convert to float
        try:
            distance = float(parts[-2])  # parts[-2] should contain the distance
            distances.append(distance)
        except ValueError:
            print(f"Could not convert to float: {parts[-2]}")

with open(output_file, 'w') as file:
    for distance in distances:
        file.write(f"{distance}\n")