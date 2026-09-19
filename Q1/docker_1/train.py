import pandas as pd
import numpy as np
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

df = pd.read_csv("spam_dataset.csv")

pipeline = Pipeline([("tfidf", TfidfVectorizer()), ("classifier", MultinomialNB())])
pipeline.fit(df["text"], df["label"])
joblib.dump(pipeline, "spam_predictor.joblib")
