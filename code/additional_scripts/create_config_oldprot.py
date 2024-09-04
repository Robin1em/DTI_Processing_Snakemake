import os
import argparse
from glob import glob
from helper_functions import generate_config_oldprot

conf = generate_config_oldprot()


### index.txt ###
# Function for counting all 0s in bval file and writing the index numbers into "index-txt" (one line per index nr)
def process_file_block1(bvalfile):
    with open(bvalfile, 'r') as bval_file:
        counter = 1
        with open(index_file_path, 'w') as index_file:
            for line in bval_file:
                numbers = line.split()
                for number in numbers:
                    if number == '0':
                        index_file.write(str(counter) + '\n')
                        counter += 1

# Function for second part of "index.txt"; keep index number for every non-0 until a new 0 comes up
def process_file_block2(bvalfile):
    with open(bvalfile, 'r') as bval_file, open(index_file_path, 'a') as index_file:
        counter = 0
        for line in bval_file:
            numbers = line.split()
            for number in numbers:
                if number == '0':
                    counter += 1
                #   index_file.write(str(counter) + '\n')
                else:
                    index_file.write(str(counter) + '\n')


### acqparams.txt ###
# Function to extract the numbers from lines in json file
# that start with ""PhaseEncodingSteps"" or ""DerivedVendorReportedEchoSpacing""
def extract_values(json_data, key1, key2):
    values = {key1: None, key2: None}
    for line in json_data:
        if f'"{key1}"' in line:  # fstring because of quotes in the file
            _, value = line.replace(',', '').strip().split(":")
            values[key1] = float(value)
        elif f'"{key2}"' in line:
            _, value = line.replace(',', '').strip().split(":")
            values[key2] = float(value)

    return values

# Function to extract number of 0s, non-os and total number of values from bval file
def count_numbers(bval_file):
    with open(bval_file, 'r') as file:
        content = file.read()

    # Split content into a list of integers
    numbers = list(map(int, content.split()))

    # Count occurrences of each number
    counts = {}
    for num in numbers:
        counts[num] = counts.get(num, 0) + 1

    # Count the number of "0"s and non-"0"s
    zero_count = counts.get(0, 0)
    non_zero_count = len(numbers) - zero_count

    return counts, zero_count, non_zero_count

def number_of_volumes(niftifile):
    with open(niftifile, 'r') as file:
        content = file.read()

    # Split content into a list of integers
    numbers = list(map(int, content.split()))

    # Count occurrences of each number
    counts = {}
    for num in numbers:
        counts[num] = counts.get(num, 0) + 1

    # Count the number of "0"s and non-"0"s
    zero_count = counts.get(0, 0)
    non_zero_count = len(numbers) - zero_count

    return counts, zero_count, non_zero_count


### Argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process files.')
    parser.add_argument('--bval', help='Path to bval file')
    parser.add_argument('--json', help='Path to json file')
    parser.add_argument('--nii', help='Path to nifti file')
    parser.add_argument('--output_dir', help='Directory for output files', default='.')
    args = parser.parse_args()

    bvalfile = args.bval
    jsonfile = args.json
    niftifile = args.nii
    output_dir = args.output_dir

    index_file_path = os.path.join(output_dir, 'index.txt')
    acqparams_file_path = os.path.join(output_dir, 'acqparams.txt')

    process_file_block1(bvalfile)
    process_file_block2(bvalfile)

    with open(jsonfile, 'r') as file:
        data = file.readlines()

    key1 = 'PhaseEncodingSteps'
    key2 = 'DerivedVendorReportedEchoSpacing'
    result = extract_values(data, key1, key2)

    if result[key1] is not None and result[key2] is not None:
        expression_result = round(result[key2] * (result[key1] - 1), 3)
    else:
        print("One or both keys for column 4 not found")

    _, zero_count, _ = count_numbers(bvalfile)

    positive_line = f'0 1 0 {expression_result}\n'
    negative_line = f'0 -1 0 {expression_result}\n'

with open(acqparams_file_path, 'w') as params_file:
    for i in range(zero_count):
        params_file.write(positive_line)
    for i in range(zero_count):
        params_file.write(negative_line)


### in case there are more b-values than one and therefore a combined bval file -> adjust index.txt ###
# get biggest value from index.txt
def get_maximum_index():
    with open('index.txt', 'r') as file:
        # initialize maximum number to a very small number
        max_number = float('-inf')
        # iterate through each line
        for line in file:
            # convert the line to an integer
            number = int(line.strip())
            # update the maximum number if current number is bigger
            if number > max_number:
                max_number = number
        return max_number

max_index = get_maximum_index()

# add biggest value from index.txt to every line in index_new.txt
def extend_index():
    if len(conf["bvecs"]) > 1:
        with open("index.txt", 'r') as file:
            with open("index_new.txt", 'w') as output_file:
                for line in file:
                    line = line.strip()
                    number = int(line)
                    updated_number = number + max_index
                    output_file.write(str(updated_number) + '\n')

        # combine index and index_new
        with open('index.txt', 'r') as file1, open('index_new.txt', 'r') as file2:
            content1 = file1.read()
            content2 = file2.read()
            os.remove('index.txt')
            os.remove('index_new.txt')
        with open('index.txt', 'w') as comb_index:
            comb_index.write(content1 + content2)

extend_index()