# combine the content of two bval files

import argparse
from glob import glob

def generate_config():
    niftis = glob("origs/*AP*.nii*")
    b_niftis = [x.replace("origs/", "").replace("_AP", "").replace("_iso", ""). replace(".nii", "").replace(".gz", "").replace("_2.2", "") for x in niftis if not "_b0_" in x]
    sample_ids = [x.split("_DTI_")[0] for x in b_niftis]
    b_values = [x.split("_DTI_")[1] for x in b_niftis]
    shortbvals = glob("bvecs_bvals/*short.bval")
    PA_niftis = glob("origs/*PA*nii*")
    PA_names = [x.replace ("origs/", "").replace(".nii", "").replace(".gz", "").replace("_iso", "") for x in PA_niftis]
    jsons = glob("origs/*AP*json")
    bvecs = glob("origs/*.bvec")
    AP_b0s = [f for f in glob("*b0*.nii.gz") if not "PA" in f]
    return {"sample_ids": sample_ids, "b_values": b_values, "niftis": niftis, "shortbvals": shortbvals, "PA_niftis": PA_niftis, "PA_names": PA_names, "jsons": jsons, "bvecs": bvecs, "AP_b0s": AP_b0s}
config = generate_config()

# create parser
parser = argparse.ArgumentParser(description='Combine content of two bvals.')

# add arguments
parser.add_argument('bval1', type=str, help='The first bval to read.')
parser.add_argument('bval2', type=str, nargs='?', default=None, help='The second bvec to read.')

# parse the arguments
args = parser.parse_args()

# Check the length of config["niftis"]
if len(config["niftis"]) > 1:
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