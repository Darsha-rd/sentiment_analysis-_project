from flask import Flask, render_template,request, redirect
from helper import preprocessing, vectorizer, get_prediction

app = Flask(__name__)

data = dict()
reviews = []
positive = 0
negative = 0

from flask import Flask, render_template, request, redirect
from helper import preprocessing, vectorizer, get_prediction

app = Flask(__name__)

data = dict()
reviews = []
positive = 0
negative = 0

brand_keywords = {
    'Apple': ['appl', 'iphon', 'io'],
    'Samsung': ['samsung', 'galaxi', 'note'],
    'Sony': ['sony', 'xperia'],
    'Nokia': ['nokia', 'lumia'],
    'Huawei': ['huawei', 'honor']
}

brand_sentiments = {brand: {'positive': 0, 'negative': 0} for brand in brand_keywords}

def detect_brands(text):
    text = text.lower()
    detected = []
    for brand, keywords in brand_keywords.items():
        if any(keyword in text for keyword in keywords):
            detected.append(brand)
    return detected

@app.route("/")
def index():
    data['reviews'] = reviews
    data['positive'] = positive
    data['negative'] = negative
    data['brand_sentiments'] = brand_sentiments
    return render_template('index.html', data=data)

@app.route("/", methods=['POST'])
def my_post():
    global positive, negative

    text = request.form['text']
    preprocessed_txt = preprocessing(text)
    vectorized_txt = vectorizer(preprocessed_txt)
    prediction = get_prediction(vectorized_txt)

    if prediction == 'negative':
        negative += 1
    else:
        positive += 1

    # Detect brands in the tweet
    brands = detect_brands(text)
    for brand in brands:
        if prediction in ['positive', 'negative']:
            brand_sentiments[brand][prediction] += 1

    reviews.insert(0, text)
    return redirect(request.url)

if __name__ == "__main__":
    app.run()
