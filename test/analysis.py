import pandas as pd
import plotly_express as px
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from textblob import TextBlob
import pandas as pd

def get_df(path):
    return pd.read_csv(path,index_col=0)

def get_sentiment_data(sentence):
    if isinstance(sentence,str):
        blob= TextBlob(sentence)
        p = [sentence.polarity for sentence in blob.sentences] 
        return p
    else:
        return np.nan
def get_review_sentiment(sentence):
    if isinstance(sentence,str):
        blob= TextBlob(sentence)
        p = [sentence.polarity for sentence in blob.sentences] 
        pavg = sum(p)/len(p)
        return pavg
    else:
        return np.nan
def get_review_subjectivity(sentence):
    if isinstance(sentence,str):
        blob= TextBlob(sentence)
        s = [sentence.subjectivity for sentence in blob.sentences] 
        savg = sum(s)/len(s)
        return savg
    else:
        return np.nan

def get_review_sentence_count(sentence):
    if isinstance(sentence,str):
        return len(sentence.split())
    return 0

def get_sentiment(value):
    if value > 0:
        return "positive"
    elif value < 0:
        return "negative"
    else:
        return "nuetral" 
