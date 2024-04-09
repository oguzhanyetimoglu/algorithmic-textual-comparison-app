import numpy as np
from gensim.models import Word2Vec
from transformers import AutoTokenizer, AutoModel


def word2vec_embedding(sentences, vector_size=100, window=5, min_count=1, workers=4):
    """
    Train a Word2Vec model on the input sentences.

    Parameters:
        sentences (list): List of tokenized sentences.
        vector_size (int): Dimensionality of the word vectors.
        window (int): Maximum distance between current and predicted word within a sentence.
        min_count (int): Ignores all words with total frequency lower than this.
        workers (int): Number of worker threads to train the model.

    Returns:
        model (Word2Vec): Trained Word2Vec model.
    """
    model = Word2Vec(sentences, vector_size=vector_size, window=window,
                     min_count=min_count, workers=workers)
    model.train(sentences, total_examples=len(sentences), epochs=10)
    return model


def get_embedding_from_pretrained(text, model_name="bert-base-uncased"):
    """
    Obtain embeddings for input text using a pre-trained model.

    Parameters:
        text (str): Raw input text.
        model_name (str): Identifier for the pre-trained model.

    Returns:
        embeddings (numpy.array): Embeddings of the input text.
    """
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)
    inputs = tokenizer(text, return_tensors="pt",
                       truncation=True, padding=True, max_length=512)
    outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.mean(dim=1).detach().numpy()
    return embeddings
