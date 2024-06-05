import math

# Constants
MU = 398600.4418  # Earth's gravitational parameter, km^3/s^2
R_EARTH = 6371.0  # Earth's radius, km

def read_tle_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    return lines

def parse_tle(lines):
    satellites = []
    for i in range(0, len(lines), 3):
        name = lines[i].strip()
        line1 = lines[i + 1].strip()
        line2 = lines[i + 2].strip()
        satellites.append((name, line1, line2))
    return satellites

def calculate_altitude(tle_line2):
    mean_motion = float(tle_line2[52:63])  # Extract Mean Motion
    mean_motion_rev_per_day = mean_motion
    mean_motion_rad_per_sec = mean_motion_rev_per_day * 2 * math.pi / 86400.0  # Convert to radians per second
    
    # Calculate the semi-major axis (a)
    semi_major_axis = (MU / (mean_motion_rad_per_sec ** 2)) ** (1/3)
    
    # Calculate the altitude (h)
    altitude = semi_major_axis - R_EARTH
    return altitude

def process_tle_file(input_filename, output_filename):
    lines = read_tle_file(input_filename)
    satellites = parse_tle(lines)
    
    results = []
    for sat in satellites:
        name, line1, line2 = sat
        altitude = calculate_altitude(line2)
        results.append((name, altitude))
    
    with open(output_filename, 'w') as f:
        for result in results:
            f.write(f"{result[0]}: Altitude = {result[1]:.2f} km\n")
    
    print(f"Processed {len(results)} satellites. Results saved to {output_filename}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python calculate_altitudes.py <input_tle_file> <output_file>")
    else:
        input_filename = sys.argv[1]
        output_filename = sys.argv[2]
        process_tle_file(input_filename, output_filename)
