from flask import Flask,request,Response,json
import pickle as pkl
import pandas as pd
import joblib
import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

from scipy.sparse import hstack
pickle_in = open("Classifiers.pkl","rb")
classifiers=joblib.load(pickle_in)

pickle_in = open("CharVectorizer.pkl","rb") 
char_vectorizer=joblib.load(pickle_in)
# pickle_in = open("CharVectorizer.pkl","rb")
# char_vectorizer=joblib.load(pickle_in)

def load_vectorizer(file_path):
    """
    Load a TfidfVectorizer object from a JSON file.
    
    Args:
        file_path (str): The file path to load the JSON file.
    
    Returns:
        TfidfVectorizer: The loaded TfidfVectorizer object.
    """
    # Read the parameters from the JSON file
    with open(file_path, 'r') as f:
        params = json.load(f)
    vectorizer = TfidfVectorizer(vocabulary=params['vocabulary'])
    # Set the idf_ attribute using the loaded values
    vectorizer.idf_ = np.asarray(params['idf'])
    return vectorizer
char_vectorizer = load_vectorizer('CharVectorizer.json')
pickle_in = open("WordVectorizer.pkl","rb")
word_vectorizer=joblib.load(pickle_in)

application = Flask(__name__)
@application.route("/",methods=["GET"])
def home():
    return "Toxicity Detector API"
@application.route("/predict/<text>",methods=["POST"])
def predict(text):
    # payload = request.get_json()
    text = " ".join(text.split("+"))
    test_text = pd.Series([text])
    test_word_features = word_vectorizer.transform(test_text)
    test_char_features = char_vectorizer.transform(test_text)
    test_features = hstack([test_char_features, test_word_features])
    res = {}
    for clf in classifiers:
        x = clf[1].predict_proba(test_features)[:, 1]
        res[clf[0]]=x[0]
    response = Response(json.dumps(res), status=200, mimetype='application/json')
    return response

if __name__=="__main__":
    application.run(debug=True)
    # application.run(debug=True)