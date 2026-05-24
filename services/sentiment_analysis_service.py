from collections import Counter
import re

from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def extract_keywords(texts, top_n=10):
    """
    Extract top keywords from a list of texts.
    """

    words = []

    for text in texts:

        text_words = re.findall(
            r"\b[a-zA-Z]+\b",
            text.lower(),
        )

        words.extend(
            [
                word
                for word in text_words
                if word not in ENGLISH_STOP_WORDS
                and len(word) > 2
            ]
        )

    return [
        word
        for word, _ in Counter(words).most_common(top_n)
    ]


def analyze_reviews(reviews):
    """
    Analyze review sentiments and extract keywords.
    """

    analyzer = SentimentIntensityAnalyzer()

    positive_review_texts = []
    negative_review_texts = []

    positive_count = 0
    negative_count = 0
    neutral_count = 0

    for review in reviews:

        score = analyzer.polarity_scores(
            review.review_text
        )

        compound = score["compound"]

        if compound >= 0.05:
            sentiment = "positive"
            positive_count += 1

            positive_review_texts.append(
                review.review_text
            )

        elif compound <= -0.05:
            sentiment = "negative"
            negative_count += 1

            negative_review_texts.append(
                review.review_text
            )

        else:
            sentiment = "neutral"
            neutral_count += 1

        review.sentiment = sentiment
        review.confidence = abs(compound)

    return {
        "positive_count": positive_count,
        "negative_count": negative_count,
        "neutral_count": neutral_count,
        "top_positive_keywords": extract_keywords(
            positive_review_texts
        ),
        "top_negative_keywords": extract_keywords(
            negative_review_texts
        ),
    }