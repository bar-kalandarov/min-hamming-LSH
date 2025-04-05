"""
Project: Minimum Hamming Distance Estimation using LSH

Description:
This script estimates the minimum Hamming distance between binary vectors using Locality-Sensitive Hashing (LSH).

Problem Statement:
Hamming distance measures the number of differing bits between two binary vectors. Calculating the exact
minimum Hamming distance for large datasets is computationally expensive. Instead, LSH can be used to
efficiently approximate the solution by reducing the number of comparisons.

Solution:
1. **LSH-based grouping:** Vectors are first divided into groups based on randomly selected bit positions.
2. **Filtered distance computation:** Within each group, additional bit positions are randomly chosen, and
   Hamming distance is computed only for vector pairs that match in these positions.
3. **Multiple runs for evaluation:** The algorithm is executed multiple times to assess the consistency and
    accuracy of the approximation.
4. This approach reduces the number of pairwise comparisons while still approximating the true minimum
   Hamming distance.

Example Usage:
-----------------
Run the script with command-line arguments:
    python min_hamming_LSH.py --vectors 1000 --length 32 --iterations 10

This will:
- Generate 1000 binary vectors of length 32.
- Estimate the minimum Hamming distance using LSH-based filtering.
- Repeat the process internally for evaluation according to the given number of iterations.

"""

import numpy as np
from collections import defaultdict
import math
import argparse


def calculate_hamming_distance(vec1: list[int], vec2: list[int]) -> int:
    """
    Calculates the Hamming distance between two binary vectors.

    The Hamming distance is the number of positions where the corresponding elements of two vectors differ.

    Args:
        vec1 (list[int]): The first binary vector.
        vec2 (list[int]): The second binary vector.

    Returns:
        int: The Hamming distance between the two vectors.

    Raises:
        ValueError: If the input vectors have different lengths.
    """

    if len(vec1) != len(vec2):
        raise ValueError("Input vectors must have the same length.")

    return sum(b1 != b2 for b1, b2 in zip(vec1, vec2))


def classify_vectors_by_random_bits(vectors: list[list[int]], num_of_bits: int) -> list[list[list[int]]]:
    """
    Classifies vectors into groups based on randomly selected bit positions.

    Each vector is assigned to a group determined by the values at randomly chosen indices.
    The function assumes that all vectors have the same length.

    Args:
        vectors (list[list[int]]): A list of binary vectors of equal length.
        num_of_bits (int): The number of random bit positions to use for classification.

    Returns:
        list[list[list[int]]]: A list of groups, where each group contains vectors
        that share the same values at the selected bit positions.
    """

    if not vectors:
        return []

    vector_length = len(vectors[0])
    indices = np.random.choice(vector_length, num_of_bits, replace=False)
    groups = defaultdict(list)

    for vec in vectors:
        key = tuple(vec[i] for i in indices)
        groups[key].append(vec)

    return list(groups.values())


def find_min_hamming_distance_in_group(vectors: list[list[int]], indices: list[int]) -> tuple[
                                int, tuple[list[int], list[int]] | None]:
    """
    Finds the pair of vectors with the minimum Hamming distance among those that match at specified indices.

    Args:
        vectors (list[list[int]]): A list of binary vectors of equal length.
        indices (list[int]): A list of indices that must match between the vector pairs.

    Returns:
        tuple[int, tuple[list[int], list[int]] | None]:
            - The minimum Hamming distance found.
            - The pair of vectors with the minimum distance, or None if no valid pair was found.
    """
    min_distance = len(vectors[0]) + 1
    min_pair = None

    for i in range(len(vectors)):
        for j in range(i + 1, len(vectors)):
            if all(vectors[i][idx] == vectors[j][idx] for idx in indices):
                dist = calculate_hamming_distance(vectors[i], vectors[j])
                if dist < min_distance:
                    min_distance = dist
                    min_pair = (vectors[i], vectors[j])

    return min_distance, min_pair


def find_min_hamming_distance_across_groups(groups: list[list[list[int]]], vector_length: int, num_of_sample_bits: int) -> tuple[int, tuple[list[int], list[int]]]:
    """
    Finds the minimum Hamming distance across multiple groups of vectors.

    This function randomly selects bit positions filter vector pairs within each group.
    The Hamming distance is then calculated for pairs that match at the selected bit positions.
    It returns the smallest Hamming distance and the pair of vectors with the minimum distance.

    Args:
        groups (list[list[list[int]]]): A list of groups, where each group is a list of binary vectors.
        vector_length (int): The length of each binary vector.
        num_of_sample_bits (int): The number of bit positions to randomly sample for filtering.

    Returns:
        tuple: A tuple containing:
            - int: The minimum Hamming distance found across all groups.
            - tuple[list[int], list[int]]: The pair of vectors that have the minimum Hamming distance.
              If no such pair is found, the second element will be None.
    """
    min_values = []

    # Randomly select bit positions to filter vector pairs
    sample_bits = np.random.choice(vector_length, num_of_sample_bits, replace=False)

    # Compute the minimum Hamming distance in each group
    for group in groups:
        min_values.append(find_min_hamming_distance_in_group(group, sample_bits))

    # Return the smallest minimum Hamming distance and the corresponding vector pair
    return min(min_values)


def find_min_hamming_using_LSH(vectors, iterations):
    # Set the number of indices to use in the LSH hash function to log(m/log(m))
    num_of_lsh_bits = round(math.log2(len(vectors) / math.log2(len(vectors))))

    # Calculates log(n) which is used to randomly select bits for filtering vectors in each group.
    log_n = round(math.log2(len(vectors[0])))

    results = []

    for _ in range(iterations):
        vectors_groups = classify_vectors_by_random_bits(vectors, num_of_lsh_bits)
        iter_result = find_min_hamming_distance_across_groups(vectors_groups, len(vectors[0]), log_n)
        results.append(iter_result)

    return min(results)


def main():
    """
    Main function that generates binary vectors, computes the minimum
    Hamming distance between them using Locality Sensitive Hashing (LSH),
    and prints the result.

    The function:
    - Generates a set of binary vectors with specified length.
    - Computes the minimum Hamming distance using LSH.
    - Prints the minimum Hamming distance and the two vectors that have the minimum distance.

    Command line arguments:
        --vectors: The number of binary vectors to generate.
        --length: The length of each binary vector.
        --iterations: The number of LSH iterations to perform.
    """

    # Parse command line arguments to allow users to customize parameters
    parser = argparse.ArgumentParser(description="Find minimum Hamming distance using LSH.")
    parser.add_argument("--vectors", type=int, required=True, help="Number of binary vectors")
    parser.add_argument("--length", type=int, required=True, help="Length of each binary vector")
    parser.add_argument("--iterations", type=int, required=True, help="Number of LSH iterations")
    args = parser.parse_args()

    # Generate the binary vectors
    binary_vectors = [np.random.randint(0, 2, args.length).tolist() for _ in range(args.vectors)]

    # Find the minimum Hamming distance using LSH
    result = find_min_hamming_using_LSH(binary_vectors, args.iterations)

    print("Minimum Hamming distance is", result[0])
    print("V1: ", result[1][0])
    print("V2: ", result[1][1])


if __name__ == "__main__":
    main()

