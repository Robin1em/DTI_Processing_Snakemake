import argparse

def sort_bvals(input_file, output_file):
    # function to sort "0" before other values
    def custom_sort(item):
        if item == "0":
            return 0
        elif item != "0":
            return 1

    # read the file line by line
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # process each line
    sorted_lines = []
    for line in lines:
        content = line.split()
        sorted_content = sorted(content, key=custom_sort)
        sorted_lines.append(' '.join(sorted_content))

    # write to a new file
    with open(output_file, 'w') as file:
        file.write('\n'.join(sorted_lines))

# create parser
parser = argparse.ArgumentParser(description='Sort content of bvals')
parser.add_argument('input', help='Path to the input file')
parser.add_argument('output', help='Path to the output file')

# parse arguments
args = parser.parse_args()

# call the function with parsed arguments
sort_bvals(args.input, args.output)
