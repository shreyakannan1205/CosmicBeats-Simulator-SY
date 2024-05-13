import random

input_file_path = 'starlink.tle'
output_file_path = 'imaging.tle'
number_of_segments_to_extract = 100

def extract_random_segments(input_file_path, output_file_path, number_of_segments_to_extract):
    with open(input_file_path, 'r') as file:
        lines = file.readlines()

    # Assuming each segment is exactly 3 lines long
    segments = [lines[i:i + 3] for i in range(0, len(lines), 3)]

    # Select a fixed number of random segments
    selected_segments = random.sample(segments, k=number_of_segments_to_extract)

    # Write the selected segments to a new file
    with open(output_file_path, 'w') as file:
        for segment in selected_segments:
            file.writelines(segment)


# Call the function
extract_random_segments(input_file_path, output_file_path, number_of_segments_to_extract)
