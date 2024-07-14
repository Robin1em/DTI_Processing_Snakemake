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