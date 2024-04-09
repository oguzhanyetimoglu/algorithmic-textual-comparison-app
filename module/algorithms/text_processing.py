import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('punkt')

def preprocess_text(text):
    """ 
    Preprocess the input text.

    Parameters:
        text (str): Raw input text.

    Returns:
        str: Processed text after tokenization, stopwords removal, and lemmatization.
    """

    # Tokenization
    tokens = nltk.word_tokenize(text)

    # Stopwords removal
    stop_words = set(stopwords.words('english'))
    tokens = [i for i in tokens if not i in stop_words]

    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(i) for i in tokens]

    return ' '.join(tokens)
