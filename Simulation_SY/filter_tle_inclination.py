import sys

def filter_satellites_by_inclination(source_file, target_file, desired_inclination):
    try:
        desired_inclination = int(desired_inclination)
    except ValueError:
        print("The provided inclination must be an integer.")
        return

    with open(source_file, 'r') as infile:
        lines = infile.readlines()

    if not lines:
        print("The source file is empty or not correctly read.")
        return

    filtered_satellites = []
    inclinations = []

    for i in range(2, len(lines), 3):
        line = lines[i].strip()
        if line.startswith('2'):
            inclination = float(line.split()[2])
            rounded_inclination = round(inclination)
            inclinations.append(rounded_inclination)
            if rounded_inclination == desired_inclination:
                filtered_satellites.extend(lines[i-2:i+1])

    if not filtered_satellites:
        print(f"No satellites found with an inclination rounding to {desired_inclination}.")
        return

    # # Debug output for tracking the inclinations found
    # print("Inclinations and their rounded values found:")
    # for incl in set(inclinations):
    #     print(f"{incl} found.")

    # Write filtered satellites' data to the target file
    with open(target_file, 'w') as outfile:
        outfile.writelines(filtered_satellites)

    # print(f"Filtered satellites with an inclination of approximately {desired_inclination} degrees have been written to {target_file}.")

# Main execution block to get command-line argument and call function
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 filter_tle.py <Desired Rounded Inclination>")
    else:
        filter_satellites_by_inclination('starlink_original.tle', 'starlink.tle', sys.argv[1])
