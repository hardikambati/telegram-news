from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def get_sentiment(text) -> str:
    """
    gets the sentiment / prediction of a statement
    returns 'Up', 'Down' or 'Neutral'
    """
    
    analyzer = SentimentIntensityAnalyzer()
    sentiment_score = analyzer.polarity_scores(text)

    positive = sentiment_score['pos']
    negative = sentiment_score['neg']

    if positive > negative:
        sentiment = 'Up \U0001F53A'
    elif positive == negative:
        sentiment = 'Neutral'
    else:
        sentiment = 'Down \U0001F53B'
    
    return sentiment
