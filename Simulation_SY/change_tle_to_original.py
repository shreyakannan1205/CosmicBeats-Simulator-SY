import sys

def erase_last_three_lines(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Check if there are more than three lines to remove the last three
    if len(lines) > 3:
        lines = lines[:-3]
    else:
        lines = []  # If less than three lines, the result is an empty file

    with open(file_path, 'w') as file:
        file.writelines(lines)

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <filename>")
        return

    file_path = sys.argv[1]
    erase_last_three_lines(file_path)
    print(f"Processed file: {file_path}")

if __name__ == "__main__":
    main()
