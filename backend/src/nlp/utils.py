import json
import numpy as np
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from gensim.models import Word2Vec
from sentence_transformers import SentenceTransformer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from gensim.models import Word2Vec
from nltk.tokenize import word_tokenize
from sentence_transformers import SentenceTransformer, util
from sklearn.neighbors import NearestNeighbors
import random
import matplotlib.pyplot as plt

def downloads():
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')

def preprocess_text(text):
    downloads()
    # Tokenization
    tokens = word_tokenize(text)
    # Convert to lower case
    tokens = [word.lower() for word in tokens]
    # Remove punctuation
    tokens = [word for word in tokens if word.isalpha()]
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if not word in stop_words]
    # Stemming
    porter = PorterStemmer()
    tokens = [porter.stem(word) for word in tokens]
    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]

    return tokens


def find_most_similar_sentences(entry_list_with_ids,
                                text_query,
                                embedding_type,
                                num_similar=10,
                                preprocessing=False,
                                similarity_technique="cosine"):
    result_list = []

    entry_list = [e[1] for e in entry_list_with_ids]
    # Preprocessing
    print("find_most_similar_sentences")
    if preprocessing:
        preprocessed_entry_list = [" ".join(preprocess_text(sentence)) for sentence in entry_list]
        preprocessed_text_query = " ".join(preprocess_text(text_query))
    else:
        preprocessed_entry_list = entry_list
        preprocessed_text_query = text_query

    # Vectorization and similarity calculation
    if embedding_type == "tfidf":
        all_sentences = [preprocessed_text_query] + preprocessed_entry_list
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(all_sentences)

        # Cosine similarity calculation
        if similarity_technique == "cosine":
            cosine_similarities = cosine_similarity(tfidf_matrix[0],
                                                    tfidf_matrix[1:])[0]
        else:
            print("similarity_technique method not supported")
            return None

    # Word2Vec vectorization and similarity calculation
    elif embedding_type == "word2vec":
        # Tokenize sentences and query string
        tokenized_sentences = [
            word_tokenize(sentence) for sentence in preprocessed_entry_list
        ]
        tokenized_query = word_tokenize(preprocessed_text_query)
        # Create Word2Vec model
        model = Word2Vec(tokenized_sentences + [tokenized_query],
                         window=5,
                         min_count=1,
                         workers=4)
        model.train(tokenized_sentences,
                    total_examples=len(tokenized_sentences),
                    epochs=10)
        # Get word embeddings for sentences and query string
        sentence_vectors = [
            model.wv[sentence].mean(axis=0) for sentence in tokenized_sentences
        ]
        query_vector = model.wv[tokenized_query].mean(axis=0)
        # Calculate cosine similarity between query string and sentences
        if similarity_technique == "cosine":
            cosine_similarities = cosine_similarity(
                [query_vector], sentence_vectors).flatten()
        else:
            print("Similarity method not supported")
            return None

    # BERT sentence embeddings and similarity calculation
    elif embedding_type == "bert":
        tokenized_sentences = [
            word_tokenize(sentence) for sentence in preprocessed_entry_list
        ]
        tokenized_query = word_tokenize(preprocessed_text_query)
        # Convert the tokenized sentences and query string to strings
        sentence_strings = [' '.join(tokens) for tokens in tokenized_sentences]
        query_string = ' '.join(tokenized_query)

        # Load pre-trained BERT model for sentence embeddings
        model = SentenceTransformer('bert-base-nli-mean-tokens')

        # Encode sentences and query string to obtain embeddings
        sentence_embeddings = model.encode(sentence_strings,
                                           convert_to_tensor=True)
        query_embedding = model.encode(query_string, convert_to_tensor=True)

        if similarity_technique == "cosine":
            cosine_similarities = util.pytorch_cos_sim(
                query_embedding, sentence_embeddings).cpu().numpy().flatten()

    # Find the indices of the most similar sentences
    top_indices = cosine_similarities.argsort()[-num_similar:][::-1]

    for index in top_indices:
        result_dict = {
            'id': entry_list_with_ids[index][0],
            'similarity': float(cosine_similarities[index])
        }
        result_list.append(result_dict)
        # print(
        #     f"Similarity: {cosine_similarities[index]:.4f} - Sentence: {entry_list[index]}"
        # )
    # print("result_list")
    return result_list


def knn_clustering(sentences, n_neighbors=5):
    """
    Fit a kNN model on the input sentences for semantic clustering.

    Parameters:
        sentences (list): List of sentences to cluster.
        n_neighbors (int): Number of neighbors to use.

    Returns:
        result_json (str): JSON string containing clustering results.
    """
    # Convert sentences to TF-IDF features
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(sentences)

    # Fit kNN model
    model_knn = NearestNeighbors(metric='cosine',
                                 algorithm='brute',
                                 n_neighbors=n_neighbors,
                                 n_jobs=-1)
    model_knn.fit(X)

    # Find distances and indices of the k-neighbors for each sentence
    distances, indices = model_knn.kneighbors(X)

    # Create a dictionary to store the results
    results = {"sentences": []}

    # Populate the dictionary with sentences, distances, indices, and neighbors
    for i, (dist, ind) in enumerate(zip(distances, indices)):
        result_entry = {
            "index":
            int(i),
            "sentence":
            sentences[i],
            "neighbors": [{
                "index": int(j),
                "sentence": sentences[j],
                "distance": dist[n]
            } for n, j in enumerate(ind) if n < len(sentences)]
        }
        results["sentences"].append(result_entry)

    # Convert the dictionary to a JSON string
    result_json = json.dumps(results, indent=2)

    return result_json


def validate_json(data, *required_fields):
    # TODO remove
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing '{field}' field in the request.")

def clustering_(entry_list_with_ids, embedding_type, clustering_technique, dim_reduction_technique, n_clusters=10, preprocessing=False):
    entry_list = [e[1] for e in entry_list_with_ids]

    # Preprocessing
    if preprocessing:
        preprocessed_entry_list = [" ".join(preprocess_text(sentence)) for sentence in entry_list]
    else:
        preprocessed_entry_list = entry_list

    # Embedding
    if embedding_type == 'tfidf':
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(preprocessed_entry_list)
        X = X.toarray()
    elif embedding_type == 'bert':
        model = SentenceTransformer('bert-base-nli-mean-tokens')
        X = model.encode(preprocessed_entry_list)
    elif embedding_type == 'word2vec':
        model = Word2Vec(preprocessed_entry_list, min_count=1)
        X = np.array([np.mean([model.wv[word] for word in doc if word in model.wv], axis=0) for doc in preprocessed_entry_list])

    else:
        raise ValueError('Invalid embedding_type')

    # Dimensionality Reduction
    if dim_reduction_technique == 'tsne':
        X = TSNE(n_components=2).fit_transform(X)
    elif dim_reduction_technique == 'pca':
        X = PCA(n_components=2).fit_transform(X)
    else:
        raise ValueError('Invalid dim_reduction_technique')

    # Clustering
    if clustering_technique == 'kmeans':
        model = KMeans(n_clusters=n_clusters)
    elif clustering_technique == 'agglomerative':
        model = AgglomerativeClustering(n_clusters=n_clusters)
    else:
        raise ValueError('Invalid clustering_technique')

    labels = model.fit_predict(X)
    # Group points by label
    clusters = {}
    for i, (label, point) in enumerate(zip(labels, X)):
        if label not in clusters:
            clusters[label] = []
        clusters[label].append({'x': point[0], 'y': point[1], "company": entry_list_with_ids[i][2], 'year': entry_list_with_ids[i][3]})
    # Convert clusters to the desired format
    result = [{'label': label, 'data': points} for label, points in clusters.items()]
    return result