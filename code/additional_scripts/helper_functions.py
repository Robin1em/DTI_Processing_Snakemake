from glob import glob

def get_similar_vectors(numbers):
    zero_triplets = []
    similar_triplets_lists = []
    current_similar_triplets = []

    for i in range(len(numbers[0])):
        triplet = [numbers[j][i] for j in range(3)]

        # Check if all numbers in triplet are 0
        if all(num == 0 for num in triplet):
            zero_triplets.append(i)
        else:
            # If the current triplet is not all zeros, check if it's similar to the previous one
            if i > 0 and triplet == [numbers[j][i-1] for j in range(3)]:
                # If similar, append to the current list
                current_similar_triplets.append(i)
            else:
                # If not similar, append the current list to similar_triplets_lists and start a new list
                if current_similar_triplets:
                    similar_triplets_lists.append(current_similar_triplets)
                current_similar_triplets = [i] # Start a new list with the current index

    # Append the last list of indices if it's not empty
    if current_similar_triplets:
        similar_triplets_lists.append(current_similar_triplets)

    return zero_triplets, similar_triplets_lists

def generate_config():
    niftis = glob("origs/*DTI*AP*.nii*")
    print(niftis)
    b_niftis = [x.replace("origs/", "").replace("_AP", "").replace("_iso", ""). replace(".nii", "").replace(".gz", "").replace("_2.2", "") for x in niftis if "DTI" in x and not "_b0_" in x]
    sample_ids = [x.split("_DTI_")[0] for x in b_niftis]
    b_values = [x.split("_DTI_")[1] for x in b_niftis]
    shortbvals = glob("bvecs_bvals/*short.bval")
    PA_niftis = glob("origs/*PA*nii*")
    PA_names = [x.replace ("origs/", "").replace(".nii", "").replace(".gz", "").replace("_iso", "").replace("_2.2", "") for x in PA_niftis]
    jsons = glob("origs/*AP*json")
    bvecs = glob("origs/*.bvec")
    AP_b0s = [f for f in glob("*b0*.nii.gz") if not "PA" in f]
    return {"sample_ids": sample_ids, "b_values": b_values, "niftis": niftis, "shortbvals": shortbvals, "PA_niftis": PA_niftis, "PA_names": PA_names, "jsons": jsons, "bvecs": bvecs, "AP_b0s": AP_b0s}

#conf = generate_config()