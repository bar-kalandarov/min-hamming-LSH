from min_hamming_LSH import find_min_hamming_using_LSH
from min_hamming import find_min_hamming_distance

import argparse
import numpy as np


def get_min_hamming_results(num_of_vectors: int, vector_length: int, lsh_iter: int) -> tuple[int, int]:
    """
    Generates a set of binary vectors and computes both the exact and approximate
    minimum Hamming distance.

    The function first generates random binary vectors of the given length.
    Then, it calculates the exact minimum Hamming distance using,
    Additionally, it estimates the minimum Hamming distance using Locality-Sensitive Hashing.

    Args:
        num_of_vectors (int): The number of binary vectors to generate.
        vector_length (int): The length of each binary vector.
        lsh_iter (int): The number of LSH iterations to perform.

    Returns:
        tuple[int, int]: A tuple containing:
            - int: The exact minimum Hamming distance.
            - int: The approximate minimum Hamming distance using LSH.
    """
    # Generate the binary vectors
    binary_vectors = [np.random.randint(0, 2, vector_length).tolist() for _ in range(num_of_vectors)]

    # Calculate exact result
    exact_result = find_min_hamming_distance(binary_vectors)[0]

    # Calculate approximate result using LSH
    approx_result = find_min_hamming_using_LSH(binary_vectors, lsh_iter)[0]

    return exact_result, approx_result


def compare_result(num_of_cmp_iterations: int, num_of_vectors: int, vector_length: int, lsh_iter: int) -> None:
    """
    Evaluates the accuracy of the LSH-based approximation for finding the minimum Hamming distance.

    This function runs `num_of_cmp_iterations` experiments where it generates
    random binary vectors, computes both the exact and approximate minimum
    Hamming distances, and tracks the accuracy of the approximation.

    It calculates:
    - The hit rate: the percentage of times the exact and approximate results match.
    - The average relative error: the mean percentage difference between the approximate and exact results.

     Note:
        Relative error is only computed for experiments where the exact result is not zero
        to avoid division by zero.

    Args:
        num_of_cmp_iterations (int): The number of inputs to check.
        num_of_vectors (int): The number of binary vectors in each experiment.
        vector_length (int): The length of each binary vector.
        lsh_iter (int): The number of LSH iterations for each input.

    Returns:
        None: The function prints the hit rate and average relative error.
    """
    correct_counter = 0
    results = []

    for _ in range(num_of_cmp_iterations):
        exact, approximate = get_min_hamming_results(num_of_vectors, vector_length, lsh_iter)

        correct_counter += exact == approximate
        results.append((exact, approximate))

    percentage_of_hits = correct_counter / num_of_cmp_iterations * 100

    # Filter out cases where the exact result is 0 to avoid division by zero
    valid_results = [(exact, approx) for exact, approx in results if exact != 0]

    if valid_results:
        percentage_of_error = sum((approx - exact) / exact for exact, approx in valid_results) / len(
            valid_results) * 100
    else:
        percentage_of_error = 0.0

    print(f"Hit rate is {percentage_of_hits:.2f}%")
    print(f"Avg. relative error is {percentage_of_error:.2f}%")


def main():
    """
    Runs a comparison of the minimum Hamming distance using both exact and LSH-based methods.

    This function allows users to specify the number of binary vectors,
    their length, and the number of iterations for comparison. It then
    calls `compare_result` with the provided parameters.

    Command-line arguments:
        --vectors (int): The number of binary vectors to generate.
        --length (int): The length of each binary vector.
        --samples (int): The number of different inputs to compare.
        --iterations (int): The number of LSH iterations to perform.

    Returns:
        None: The function parses arguments and calls `compare_result`.
    """

    # Parse command line arguments to allow users to customize parameters
    parser = argparse.ArgumentParser(description="Check the LSH solution quality.")
    parser.add_argument("--vectors", type=int, required=True, help="Number of binary vectors")
    parser.add_argument("--length", type=int, required=True, help="Length of each binary vector")
    parser.add_argument("--samples", type=int, required=True, help="Number of case studies to check")
    parser.add_argument("--iterations", type=int, required=True, help="Number of LSH iterations")
    args = parser.parse_args()

    compare_result(args.samples, args.vectors, args.length, args.iterations)


if __name__ == "__main__":
    main()
