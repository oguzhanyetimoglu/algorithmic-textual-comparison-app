import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from scipy.cluster.hierarchy import dendrogram, linkage
import numpy as np

def visualize_with_pca(embeddings, num_components=2):
    """
    Visualize embeddings using PCA and Plotly.

    This function reduces the dimensionality of embeddings using PCA and visualizes 
    the results using Plotly's scatter plot.

    Parameters:
        embeddings (numpy.array): The input high-dimensional embeddings.
        num_components (int, optional): The number of principal components for PCA. 
                                      Default is 2.

    Returns:
        fig (plotly.graph_objs._figure.Figure): A Plotly figure object representing the scatter plot.
    """
    pca = PCA(n_components=num_components)
    reduced_embeddings = pca.fit_transform(embeddings)

    df = pd.DataFrame(reduced_embeddings, columns=[
                      f"PC{i+1}" for i in range(num_components)])
    fig = px.scatter(df, x="PC1", y="PC2")
    
    return fig


def visualize_with_tsne(data, labels=None, perplexity=30, learning_rate=200, n_iter=1000):
    """
    Visualize high-dimensional data using t-SNE.

    Parameters:
        data (numpy.array): High-dimensional data matrix.
        labels (list or numpy.array, optional): Labels for each data point for coloring. Default is None.
        perplexity (float): The perplexity is related to the number of nearest neighbors that are used in learning algorithms. Consider selecting a value between 5-50.
        learning_rate (float): Learning rate for t-SNE. Usually in the range [10.0, 1000.0].
        n_iter (int): Number of iterations for optimization.

    Returns:
    numpy.array: 2D array representing data in 2D space.
    """

    tsne = TSNE(perplexity=perplexity, n_components=2,
                learning_rate=learning_rate, n_iter=n_iter, random_state=42)
    data = np.array(data)
    tsne_results = tsne.fit_transform(data)
    # Plotting the results
    plt.figure(figsize=(10, 6))

    if labels is not None:
        plt.scatter(tsne_results[:, 0],
                    tsne_results[:, 1], c=labels, cmap='viridis')
        plt.colorbar()
    else:
        plt.scatter(tsne_results[:, 0], tsne_results[:, 1])

    plt.title('t-SNE visualization')
    plt.xlabel('Dimension 1')
    plt.ylabel('Dimension 2')
    plt.grid(True)
    plt.show()

    return tsne_results


def plot_dendrogram(model, **kwargs):
    """
    Create linkage matrix and then plot the dendrogram.

    Parameters:
        model (AgglomerativeClustering): Instance of AgglomerativeClustering.

    Returns:
        None
    """
    # Create the counts of samples under each node
    counts = np.zeros(np.array(model["children_"]).shape[0])
    n_samples = len(model["labels_"])
    for i, merge in enumerate(model["children_"]):
        current_count = 0
        for child_idx in merge:
            if child_idx < n_samples:
                current_count += 1  # leaf node
            else:
                current_count += counts[child_idx - n_samples]
        counts[i] = current_count

    linkage_matrix = np.column_stack([model["children_"], model["distances_"],
                                      counts]).astype(float)
    print(linkage_matrix)
    # Plot the dendrogram
    plt.figure(figsize=(10, 7))
    dendrogram(linkage_matrix)
    plt.title('Hierarchical Clustering Dendrogram')
    plt.xlabel('sample index')
    plt.ylabel('distance')
    plt.show()