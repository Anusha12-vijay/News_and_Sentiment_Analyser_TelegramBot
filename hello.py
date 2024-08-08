import streamlit as st
import joblib
import pandas as pd
import re
from nltk.stem import PorterStemmer

# Load the model and vectorizer
model = joblib.load('model.pkl')
vectorizer = joblib.load('vectorizer.pkl')

# Initialize the stemmer
stemmer = PorterStemmer()

def preprocess_tweet(tweet):
    def remove_pattern(input_text, pattern):
        r = re.findall(pattern, input_text)
        for word in r:
            input_text = re.sub(word, "", input_text)
        return input_text

    tweet = remove_pattern(tweet, "@[\w]*")
    tweet = re.sub("[^a-zA-Z#]", " ", tweet)
    tweet = " ".join([w for w in tweet.split() if len(w) > 3])
    tweet = " ".join([stemmer.stem(word) for word in tweet.split()])
    return tweet

def predict_sentiment(tweet):
    cleaned_tweet = preprocess_tweet(tweet)
    bow = vectorizer.transform([cleaned_tweet])
    prediction = model.predict(bow)
    return "Positive sentiment" if prediction == 0 else "Negative sentiment"

st.title("Twitter Sentiment Analysis")
st.write("Enter a tweet to analyze its sentiment:")

tweet = st.text_area("Tweet", "")
if st.button("Analyze Sentiment"):
    if tweet:
        sentiment = predict_sentiment(tweet)
        st.write(f"Sentiment: {sentiment}")
    else:
        st.write("Please enter a tweet to analyze.")
