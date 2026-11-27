
from flask import Flask, render_template, request
from sklearn.naive_bayes import GaussianNB
import numpy as np

app = Flask(__name__)

# Training dataset: [Study Hours, Attendance, Previous Marks]
X = np.array([
    [1, 50, 40],
    [2, 55, 45],
    [3, 60, 50],
    [4, 65, 55],
    [5, 70, 60],
    [6, 75, 65],
    [7, 80, 75],
    [8, 85, 80],
    [9, 90, 85],
    [10, 95, 90]
])

# 0 = Needs Improvement, 1 = Good
y = np.array([0, 0, 0, 0, 1, 1, 1, 1, 1, 1])

model = GaussianNB()
model.fit(X, y)


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    probability = None

    if request.method == "POST":
        try:
            hours = float(request.form["hours"])
            attendance = float(request.form["attendance"])
            marks = float(request.form["marks"])

            if not (0 <= hours <= 24 and
                    0 <= attendance <= 100 and
                    0 <= marks <= 100):
                raise ValueError("Enter valid values within the given ranges.")

            prediction = model.predict([[hours, attendance, marks]])[0]
            probability = round(max(model.predict_proba(
                [[hours, attendance, marks]])[0]) * 100, 2)

            if prediction == 1:
                result = "Good Performance"
            else:
                result = "Needs Improvement"

        except ValueError as e:
            result = str(e)

    return render_template(
        "index.html",
        result=result,
        probability=probability
    )


if __name__ == "__main__":
    app.run(debug=True)
