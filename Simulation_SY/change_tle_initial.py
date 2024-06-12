import random
import sys

def extract_and_save_remaining_segments(input_file_path, extracted_output_path, remaining_output_path, number_of_segments_to_extract):
    with open(input_file_path, 'r') as file:
        lines = file.readlines()

    segments = [lines[i:i + 3] for i in range(0, len(lines), 3)]

    selected_segments = random.sample(segments, k=number_of_segments_to_extract)

    with open(extracted_output_path, 'w') as file:
        for segment in selected_segments:
            file.writelines(segment)

    remaining_segments = [segment for segment in segments if segment not in selected_segments]

    remaining_lines = [line for segment in remaining_segments for line in segment]

    with open(remaining_output_path, 'w') as file:
        file.writelines(remaining_lines)

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python3 change_tle_initial.py input_file_path extracted_output_path remaining_output_path number_of_segments_to_extract")
        sys.exit(1)

    input_file_path = sys.argv[1]
    extracted_output_path = sys.argv[2]
    remaining_output_path = sys.argv[3]
    try:
        number_of_segments_to_extract = int(sys.argv[4])
    except ValueError:
        print("Please ensure 'number_of_segments_to_extract' is an integer.")
        sys.exit(1)

    extract_and_save_remaining_segments(input_file_path, extracted_output_path, remaining_output_path, number_of_segments_to_extract)
