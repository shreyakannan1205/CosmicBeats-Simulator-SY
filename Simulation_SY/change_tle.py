import random
import sys


def extract_random_segments(input_file_path, output_file_path, number_of_segments_to_extract):
    with open(input_file_path, 'r') as file:
        lines = file.readlines()

    segments = [lines[i:i + 3] for i in range(0, len(lines), 3)]

    selected_segments = random.sample(segments, k=number_of_segments_to_extract)

    with open(output_file_path, 'w') as file:
        for segment in selected_segments:
            file.writelines(segment)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script_name.py input_file_path output_file_path number_of_segments_to_extract")
        sys.exit(1)

    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]
    try:
        number_of_segments_to_extract = int(sys.argv[3])
    except ValueError:
        print("Please ensure 'number_of_segments_to_extract' is an integer.")
        sys.exit(1)

    extract_random_segments(input_file_path, output_file_path, number_of_segments_to_extract)
