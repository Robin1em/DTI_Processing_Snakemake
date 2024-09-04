# combine the content of two bval files

import argparse
from glob import glob
from helper_functions import generate_config_oldprot

conf = generate_config_oldprot()

# create parser
parser = argparse.ArgumentParser(description='Combine content of two bvals.')

# add arguments
parser.add_argument('bval1', type=str, help='The first bval to read.')
parser.add_argument('bval2', type=str, nargs='?', default=None, help='The second bvec to read.')

# parse the arguments
args = parser.parse_args()

# Check the length of config["niftis"]
if len(conf["niftis"]) > 1:
    # use the arguments to open the files
    with open(args.bval1, 'r') as bval1, open(args.bval2, 'r') as bval2:
        # Read the content of each file
        content1 = bval1.read().splitlines()
        content2 = bval2.read().splitlines()

    # make both contents strings (otherwise next step doesn't work)
    if isinstance(content1, list):
        content1 = ' '.join(content1)
    if isinstance(content2, list):
        content2 = ' '.join(content2)

    # combine contents with a single space as separator
    combined_content = content1 + ' ' + content2

    # write combined content to a new file
    with open('sorted_bvals_combined.bval', 'w') as combined_file:
        combined_file.write(combined_content)
else:
    # If the length of config["niftis"] is not more than 1, just write the content of bvec1
    with open(args.bval1, 'r') as bval1:
        content1 = bval1.read()

    with open('sorted_bvals_combined.bval', 'w') as combined_file:
        combined_file.write(content1)