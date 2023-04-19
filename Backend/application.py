from flask import Flask,request,Response,json
import joblib
import json
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import hstack
def load_vectorizer(file_path):
    with open(file_path, 'r') as f:
        params = json.load(f)
    vectorizer = TfidfVectorizer(vocabulary=params['vocabulary'])
    vectorizer.idf_ = np.asarray(params['idf'])
    return vectorizer


pickle_in = open("Classifiers.pkl","rb")
classifiers=joblib.load(pickle_in)
char_vectorizer = load_vectorizer('CharVectorizer.json')
pickle_in = open("WordVectorizer.pkl","rb")
word_vectorizer=joblib.load(pickle_in)

application = Flask(__name__)

@application.route("/",methods=["GET"])
def home():
    return "Toxicity Detector API"

@application.route("/predict",methods=["POST"])
def predict():
    payload = request.get_json()
    test_text = payload["text"].strip()
    test_text = pd.Series([test_text])
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