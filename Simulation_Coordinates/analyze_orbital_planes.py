import sys
from collections import defaultdict

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
        satellites.append((name, inclination, raan))
    return satellites

def group_by_orbital_plane(satellites, inclination_tolerance=1, raan_tolerance=2):
    orbital_planes = defaultdict(list)
    for sat in satellites:
        name, inclination, raan = sat
        # Apply different tolerances for inclination and RAAN
        orbital_plane_key = (round(inclination / inclination_tolerance) * inclination_tolerance,
                             round(raan / raan_tolerance) * raan_tolerance)
        orbital_planes[orbital_plane_key].append(sat)
    return orbital_planes

def sort_orbital_planes_by_satellites(orbital_planes):
    sorted_planes = sorted(orbital_planes.items(), key=lambda x: len(x[1]), reverse=True)
    return sorted_planes

def save_analysis_results(filename, total_satellites, total_planes, sorted_planes):
    with open(filename, 'w') as file:
        file.write(f"Total number of satellites: {total_satellites}\n")
        file.write(f"Total number of distinct orbital planes: {total_planes}\n")
        for plane, sats in sorted_planes:
            file.write(f"Orbital Plane {plane}: {len(sats)} satellites\n")

def main(tle_filename, output_filename):
    lines = read_tle_file(tle_filename)
    satellites = parse_tle(lines)
    orbital_planes = group_by_orbital_plane(satellites)
    sorted_planes = sort_orbital_planes_by_satellites(orbital_planes)
    
    total_satellites = len(satellites)
    total_planes = len(orbital_planes)
    
    save_analysis_results(output_filename, total_satellites, total_planes, sorted_planes)
    
    print(f"Total number of satellites: {total_satellites}")
    print(f"Total number of distinct orbital planes: {total_planes}")
    for plane, sats in sorted_planes:
        print(f"Orbital Plane {plane}: {len(sats)} satellites")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 analyze_orbital_planes.py <tle_file> <output_file>")
    else:
        main(sys.argv[1], sys.argv[2])
