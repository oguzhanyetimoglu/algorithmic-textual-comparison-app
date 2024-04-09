from sklearn.feature_extraction.text import TfidfVectorizer


def tfidf_vectorization(corpus):
    """
    Convert the corpus into TF-IDF matrix.

    Parameters:
        corpus (list): List of texts.

    Returns:
        tfidf_matrix (sparse matrix): Matrix of TF-IDF vectors.
        vectorizer (TfidfVectorizer): Fitted TF-IDF vectorizer.
    """
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)
    return tfidf_matrix, vectorizer
