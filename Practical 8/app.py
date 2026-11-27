
from flask import Flask, render_template, request
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

app = Flask(__name__)

# Sample training data
texts = [
    "I love this product",
    "This is amazing",
    "I am very happy",
    "Excellent experience",
    "I really enjoyed it",
    "This is wonderful",
    "I hate this product",
    "This is terrible",
    "I am very disappointed",
    "Worst experience ever",
    "I dislike this",
    "This is horrible",
    "The product is okay",
    "It is average",
    "Nothing special",
    "The experience was normal",
    "It is neither good nor bad",
    "The product is acceptable"
]

labels = [
    "Positive", "Positive", "Positive",
    "Positive", "Positive", "Positive",
    "Negative", "Negative", "Negative",
    "Negative", "Negative", "Negative",
    "Neutral", "Neutral", "Neutral",
    "Neutral", "Neutral", "Neutral"
]

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(texts)

model = MultinomialNB()
model.fit(X, labels)


@app.route("/", methods=["GET", "POST"])
def index():
    sentiment = None
    confidence = None
    user_text = ""

    if request.method == "POST":
        user_text = request.form.get("text", "").strip()

        if user_text:
            transformed_text = vectorizer.transform([user_text])
            sentiment = model.predict(transformed_text)[0]

            probabilities = model.predict_proba(transformed_text)[0]
            confidence = round(max(probabilities) * 100, 2)
        else:
            sentiment = "Please enter some text."

    return render_template(
        "index.html",
        sentiment=sentiment,
        confidence=confidence,
        user_text=user_text
    )


if __name__ == "__main__":
    app.run(debug=True)
