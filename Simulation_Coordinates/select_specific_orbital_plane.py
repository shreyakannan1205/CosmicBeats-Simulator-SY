import sys

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
        inclination = float(line2[8:16])
        raan = float(line2[17:25])
        satellites.append((name, inclination, raan, line1, line2))
    return satellites

def filter_orbital_plane(satellites, target_inclination, target_raan, tolerance=1):
    filtered_satellites = []
    for sat in satellites:
        name, inclination, raan, line1, line2 = sat
        if abs(inclination - target_inclination) <= tolerance and abs(raan - target_raan) <= tolerance:
            filtered_satellites.append((name, line1, line2))
    return filtered_satellites

def save_filtered_satellites(filename, satellites):
    with open(filename, 'w') as file:
        for sat in satellites:
            name, line1, line2 = sat
            file.write(f"{name}\n{line1}\n{line2}\n")

def main(tle_filename, output_filename, target_inclination, target_raan):
    lines = read_tle_file(tle_filename)
    satellites = parse_tle(lines)
    filtered_satellites = filter_orbital_plane(satellites, target_inclination, target_raan)
    
    save_filtered_satellites(output_filename, filtered_satellites)
    
    print(f"Filtered {len(filtered_satellites)} satellites to {output_filename}")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python3 select_specific_orbital_plane.py <tle_file> <output_file> <target_inclination> <target_raan>")
    else:
        tle_filename = sys.argv[1]
        output_filename = sys.argv[2]
        target_inclination = float(sys.argv[3])
        target_raan = float(sys.argv[4])
        main(tle_filename, output_filename, target_inclination, target_raan)
