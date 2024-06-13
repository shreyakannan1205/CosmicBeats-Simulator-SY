# Define a function to calculate the checksum of a TLE line
def calculate_checksum(tle_line):
    checksum = 0
    for char in tle_line:
        if char.isdigit():
            checksum += int(char)
        elif char == '-':
            checksum += 1
    return checksum % 10

# Generate the TLEs
def generate_tles():
    mean_anomaly_start = 279.9317
    tles = []

    for i in range(1, 89):
        mean_anomaly = (mean_anomaly_start + i) % 360
        catalog_number = 54778 + i
        
        sat_name = f"Imaginary_{i}"
        tle_1 = f"1 {catalog_number:05d}U 22175W   24100.52217282  .00001245  00000+0  96324-4 0  "
        tle_2 = f"2 {catalog_number:05d}  53.2156 287.4860 0001364  80.1829  {mean_anomaly:8.4f} 15.08840119 72428"

        # Calculate checksums
        checksum_1 = calculate_checksum(tle_1)
        checksum_2 = calculate_checksum(tle_2)

        tle_1 += str(checksum_1)
        tle_2 += str(checksum_2)

        tles.append((sat_name, tle_1, tle_2))

    return tles

# Generate the TLEs
tles = generate_tles()

# Save the TLEs to a file with the specified format
with open('5th_sat.tle', 'w') as file:
    for tle in tles:
        file.write(tle[0] + '\n' + tle[1] + '\n' + tle[2] + '\n')

print("TLEs have been saved to 5th_sat.tle")
