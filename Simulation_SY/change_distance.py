input_file = "distance.txt"  
output_file = "distance_fixed.txt"  

with open(input_file, 'r') as file:
    lines = file.readlines()

distances = []
for line in lines:
    if 'km' in line:  
        parts = line.split()
        try:
            distance = float(parts[-2]) 
            distances.append(distance)
        except ValueError:
            print(f"Could not convert to float: {parts[-2]}")

with open(output_file, 'w') as file:
    for distance in distances:
        file.write(f"{distance}\n")