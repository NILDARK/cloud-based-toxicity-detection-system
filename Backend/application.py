from flask import Flask,request,Response,json
import pickle as pkl
import pandas as pd
import joblib
from scipy.sparse import hstack
pickle_in = open("Classifiers.pkl","rb")
classifiers=joblib.load(pickle_in)

pickle_in = open("CharVectorizer.pkl","rb")
char_vectorizer=joblib.load(pickle_in)

pickle_in = open("WordVectorizer.pkl","rb")
word_vectorizer=joblib.load(pickle_in)

application = Flask(__name__)
@application.route("/",methods=["GET"])
def home():
    return "Hello Its running mf..."
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
    # application.run(host="127.0.0.1",port=5000,debug=True)
    application.run(debug=True)