from sklearn.cluster import AgglomerativeClustering
from sklearn.neighbors import NearestNeighbors


def knn_clustering(matrix, n_neighbors=5):
    """
    Fit a kNN model on the input matrix for clustering.

    Parameters:
        matrix (numpy.array or sparse matrix): Matrix to cluster.
        n_neighbors (int): Number of neighbors to use.

    Returns:
        model_knn (NearestNeighbors): Fitted kNN model.
    """
    model_knn = NearestNeighbors(
        metric='cosine', algorithm='brute', n_neighbors=n_neighbors, n_jobs=-1)
    model_knn.fit(matrix)
    return model_knn


def agglomerative_clustering(data, n_clusters=5, linkage='ward'):
    """
    Perform agglomerative clustering on the data.

    Parameters:
        data (array-like of shape (n_samples, n_features)): Input data.
        n_clusters (int): Desired number of clusters.
        linkage (str, optional): Which linkage criterion to use. 
        Options are 'ward', 'complete', 'average', 'single'. Defaults to 'ward'.

    Returns:
        array: Cluster labels for each data point.
    """
    clustering = AgglomerativeClustering(
        n_clusters=n_clusters, linkage=linkage)
    cluster_labels = clustering.fit_predict(data)
    return cluster_labels
