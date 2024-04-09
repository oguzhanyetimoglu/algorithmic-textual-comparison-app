from flask import Flask, jsonify, request
from algorithms.clustering import knn_clustering, agglomerative_clustering
from algorithms.similarity import calculate_cosine_similarity
from algorithms.text_processing import preprocess_text
from algorithms.vectorization import tfidf_vectorization
from algorithms.visualization import visualize_with_pca, visualize_with_tsne, plot_dendrogram
from algorithms.word_embedding import word2vec_embedding, get_embedding_from_pretrained

app = Flask(__name__)


def validate_json(data, *required_fields):
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing '{field}' field in the request.")


@app.route('/preprocess', methods=['POST'])
def preprocess_endpoint():
    try:
        data = request.get_json()
        validate_json(data, 'text')
        processed_text = preprocess_text(data['text'])
        return jsonify({'processed_text': processed_text})

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/tfidf', methods=['POST'])
def tfidf_endpoint():
    try:
        data = request.get_json()
        validate_json(data, 'corpus')
        tfidf_matrix, _ = tfidf_vectorization(data['corpus'])
        return jsonify({'tfidf_matrix': tfidf_matrix.toarray().tolist()})

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/word2vec-embedding', methods=['POST'])
def word2vec_embedding_endpoint():
    try:
        data = request.get_json()
        validate_json(data, 'sentences')
        embedding_model = word2vec_embedding(data['sentences'])
        # Additional processing or response as needed
        return jsonify({'message': 'Word2Vec embedding generated successfully'})

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/pretrained-embedding', methods=['POST'])
def pretrained_embedding_endpoint():
    try:
        data = request.get_json()
        validate_json(data, 'text')
        embeddings = get_embedding_from_pretrained(data['text'])
        return jsonify({'embeddings': embeddings.tolist()})

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/cosine-similarity', methods=['POST'])
def cosine_similarity_endpoint():
    try:
        data = request.get_json()
        validate_json(data, 'matrix1', 'matrix2')
        similarity = calculate_cosine_similarity(
            data['matrix1'], data['matrix2'])
        return jsonify({'cosine_similarity': similarity.tolist()})

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/knn-clustering', methods=['POST'])
def knn_clustering_endpoint():
    try:
        data = request.get_json()
        validate_json(data, 'matrix', 'n_neighbors')
        knn_model = knn_clustering(data['matrix'], data['n_neighbors'])
        # Additional processing or response as needed
        return jsonify({'message': 'kNN clustering model fitted successfully'})

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/agglomerative-clustering', methods=['POST'])
def agglomerative_clustering_endpoint():
    try:
        data = request.get_json()
        validate_json(data, 'input_data', 'n_clusters')
        # Default to 'ward' if not provided
        linkage = data.get('linkage', 'ward')
        cluster_labels = agglomerative_clustering(
            data['input_data'], data['n_clusters'], linkage)
        return jsonify({'cluster_labels': cluster_labels.tolist()})

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/visualize-pca', methods=['POST'])
def visualize_pca_endpoint():
    try:
        data = request.get_json()
        validate_json(data, 'embeddings')
        num_components = data.get('num_components', 2)
        fig = visualize_with_pca(data['embeddings'], num_components)
        # Additional processing or response as needed
        return jsonify({'message': 'PCA visualization generated successfully'})

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/visualize-tsne', methods=['POST'])
def visualize_tsne_endpoint():
    try:
        data = request.get_json()
        validate_json(data, 'high_dimensional_data')
        labels = data.get('labels')  # Optional
        perplexity = data.get('perplexity')
        learning_rate = data.get('learning_rate')
        n_iter = data.get('n_iter')
        tsne_results = visualize_with_tsne(
            data=data['high_dimensional_data'], labels=labels, perplexity=perplexity, learning_rate=learning_rate, n_iter=n_iter)
        # Additional processing or response as needed
        return jsonify({'message': 't-SNE visualization generated successfully'})

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/plot-dendrogram', methods=['POST'])
def plot_dendrogram_endpoint():
    try:
        data = request.get_json()
        validate_json(data, 'model')
        print(data['model'])
        plot_dendrogram(data['model'])
        # Additional processing or response as needed
        return jsonify({'message': 'Dendrogram plot generated successfully'})

    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)
