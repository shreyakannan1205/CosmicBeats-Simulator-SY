import re
import argparse

def correct_lines(input_output_file):
    with open(input_output_file, 'r') as file:
        lines = file.readlines()
    
    corrected_lines = []
    for line in lines:
        # Remove blank lines
        if line.strip():
            # Detect concatenated lines using a regular expression pattern
            corrected_line = re.sub(r"(\d+\.\d+)(Pass\. nodeID:)", r"\1\n\2", line)
            corrected_lines.append(corrected_line)
    
    with open(input_output_file, 'w') as file:
        file.writelines(corrected_lines)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Correct lines in a text file by inserting missing newlines and removing blank lines.")
    parser.add_argument("input_output_file", help="The input and output text file")
    args = parser.parse_args()
    
    correct_lines(args.input_output_file)
