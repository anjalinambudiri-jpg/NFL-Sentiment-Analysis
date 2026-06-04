from sklearn.preprocessing import MinMaxScaler, LabelEncoder

def label(df, cols):
    '''
    Args:
    df: Pandas dataframe
    cols: list of strings
    
    Returns:
    df: updated Pandas dataframe with adjusted columns
    
    Takes selected columns from the dataframe and uses scikit library's LabelEncoder to change categorical columns to numeric values
    
    '''
    
    for each in cols: # Cycle through each column name in the list
        
        label_encoder = LabelEncoder() #Initialze encoder
        
        df[each] = label_encoder.fit_transform(df[each]) #Apply to df column
        
    return df


import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('punkt_tab')
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

def lemmatize(text):
    ''' 
    Args:
    text: str

    Returns:
    str

    Transforms a string into lemmatized version: lowercase, same words of different tenses collapsed (eg. 'runs', 'ran' to 'run'), sourcing from nltk word dictionaries

    '''
    
    lemmatizer = WordNetLemmatizer() # Initialize the lemmatizer
    
    text = str(text).lower() # Make all characters lowercase
    
    words = word_tokenize(text) # Split text into tokens (separated by individual words)
    
    lemmatized_words = [lemmatizer.lemmatize(word) for word in words]  # Lemmatize every word, pulling from nltk dictionary
    
    return " ".join(lemmatized_words)  # Join separate words back together into paragraph structure




from sklearn.model_selection import train_test_split
from sklearn.base import clone
import numpy as np


def train(pipeline, X, Y, trials=5):
    '''
    Args:
    pipeline: Scikit Pipeline
    X: Pandas Series
    Y: Pandas Series
    trials: int

    Returns:
    float

    Trains a scikit pipeline for a set number of trials, then outputs average accuracy across all trials

    '''
    accuracy = [] #To store accuracy from each trial
    
    for i in range(trials):
        X_train, X_test, y_train, y_test = train_test_split(X,Y,test_size=0.2, random_state=i) # Split data
        
        fresh_pipeline = clone(pipeline) # Create new pipeline of same type by cloning previous, ensures each trial is fresh
        
        fresh_pipeline.fit(X_train, y_train) # Fit on training data
        
        score = fresh_pipeline.score(X_test, y_test)  # Evaluate on test data 


        print(f"Logistic Regression Accuracy Trial {i+1}:", score) #Output individual trial accuracy
       
        accuracy.append(score) # Accumulate accuracy from each trial

    array = np.array(accuracy) # Turn array into numpy array, so that mean can be computed easily

    return array.mean()



import vaderSentiment
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def find_sentiment_dict(text):
    ''' 
    Args: 
    text: str
    
    Returns:
    scores: dictionary

    Uses Vader library's SentimentIntensityAnalyzer to compute a sentiment score for a section of text, broken into a negative, neutral, and positive components as well as a compound score. 
    
    '''
    analyzer = SentimentIntensityAnalyzer() # Initialize the analyzer
    
    text = str(text) #Ensure input is in string form
    
    scores = analyzer.polarity_scores(text) #Calculate sentiment scores
    
    return scores







