from sklearn.metrics.pairwise import cosine_similarity, linear_kernel


def calculate_cosine_similarity(matrix1, matrix2, pd="c"):
    """
    Calculate cosine similarity between two matrices.

    NOTE: Notice both linear_kernel and cosine_similarity produced the same result. When you're 
        working with a very large amount of data and your vectors are in the tf-idf representation, 
        it is good practice to default to linear_kernel to improve performance.

    Parameters:
        matrix1 (numpy.array or sparse matrix): First matrix.
        matrix2 (numpy.array or sparse matrix): Second matrix.
        pd (str): Option for linear_kernel and cosine_similarity.

    Returns:
        numpy.array: Cosine similarity scores between matrix1 and matrix2.
    """
    if pd == "c":
        return cosine_similarity(matrix1, matrix1)
    else:
        return linear_kernel(matrix1, matrix2)
