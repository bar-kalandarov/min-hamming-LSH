from min_hamming_LSH import calculate_hamming_distance


def find_min_hamming_distance(vectors: list[list[int]]) -> tuple[int, tuple[list[int], list[int]] | None]:
    """
    Finds the pair of vectors with the minimum Hamming distance.

    Args:
        vectors (list[list[int]]): A list of binary vectors of equal length.

    Returns:
        tuple[int, tuple[list[int], list[int]] | None]:
            - The minimum Hamming distance found.
            - The pair of vectors with the minimum distance, or None if no valid pair was found.
    """
    min_distance = len(vectors[0]) + 1
    min_pair = None

    for i in range(len(vectors)):
        for j in range(i + 1, len(vectors)):
            dist = calculate_hamming_distance(vectors[i], vectors[j])
            if dist < min_distance:
                min_distance = dist
                min_pair = (vectors[i], vectors[j])

    return min_distance, min_pair

