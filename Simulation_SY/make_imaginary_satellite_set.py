def calculate_checksum(tle_line):
    checksum = 0
    for char in tle_line:
        if char.isdigit():
            checksum += int(char)
        elif char == '-':
            checksum += 1
    return checksum % 10

# Base TLE values
base_tle_1 = "1 {catalog_number:05d}U 22175S   24100.52217282  .00001245  00000+0  96324-4 0  {tle_number}"
base_tle_2 = "2 {catalog_number:05d}  53.2156 287.4860 0001364  80.1829  {mean_anomaly:8.4f} 15.08840119 72428{checksum_digit}"

# Initial Mean Anomaly
initial_mean_anomaly = 279.9317
final_mean_anomaly = 294.9317

# Number of satellites
num_satellites = 14

# Generate TLEs
tles = []

for i in range(1, num_satellites + 1):
    mean_anomaly = (initial_mean_anomaly + i) % 360
    catalog_number = 54775 + i 
    
    tle_1 = base_tle_1.format(catalog_number=catalog_number, tle_number=2 + i)
    tle_2 = base_tle_2.format(catalog_number=catalog_number, mean_anomaly=mean_anomaly, checksum_digit=6 + i)

    checksum_1 = calculate_checksum(tle_1)
    checksum_2 = calculate_checksum(tle_2)
    
    tle_1 += str(checksum_1)
    tle_2 += str(checksum_2)
    
    tles.append((f"Imaginary_{i}", tle_1, tle_2))

with open('imaginary_24.tle', 'w') as file:
    for tle in tles:
        file.write(tle[0] + '\n')
        file.write(tle[1] + '\n')
        file.write(tle[2] + '\n')

print("TLEs have been saved to imaginary_24.tle")
