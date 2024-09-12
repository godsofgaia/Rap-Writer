from textblob import TextBlob


def analyze_sentiment(text):
    """Analyzes the sentiment of the provided text."""
    if not text:
        raise ValueError("Input text cannot be empty.")
    sentiment = TextBlob(text).sentiment
    return {
        'polarity': sentiment.polarity,
        'subjectivity': sentiment.subjectivity
    }


def analyze_sentiments(texts):
    """Analyzes the sentiment of a list of texts."""
    return {text: analyze_sentiment(text) for text in texts}
