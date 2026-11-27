
from flask import Flask, render_template, request
from sklearn.tree import DecisionTreeClassifier

app = Flask(__name__)

# Training dataset
# Features: [study_hours, attendance, previous_marks]
X = [
    [1, 40, 30],
    [2, 50, 35],
    [3, 55, 40],
    [4, 60, 45],
    [5, 70, 55],
    [6, 75, 65],
    [7, 80, 70],
    [8, 85, 80],
    [9, 90, 85],
    [10, 95, 90],
    [2, 45, 25],
    [5, 65, 50],
    [7, 75, 60],
    [8, 90, 75]
]

# 0 = Needs Improvement, 1 = Good Performance
y = [
    0, 0, 0, 0, 0, 1, 1,
    1, 1, 1, 0, 0, 1, 1
]

# Create and train Decision Tree model
model = DecisionTreeClassifier(random_state=42)
model.fit(X, y)


@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    study_hours = ""
    attendance = ""
    previous_marks = ""

    if request.method == "POST":
        try:
            study_hours = float(request.form["study_hours"])
            attendance = float(request.form["attendance"])
            previous_marks = float(request.form["previous_marks"])

            if not (0 <= study_hours <= 24):
                raise ValueError("Study hours must be between 0 and 24.")

            if not (0 <= attendance <= 100):
                raise ValueError("Attendance must be between 0 and 100.")

            if not (0 <= previous_marks <= 100):
                raise ValueError("Previous marks must be between 0 and 100.")

            result = model.predict([[
                study_hours,
                attendance,
                previous_marks
            ]])[0]

            if result == 1:
                prediction = "Good Performance"
            else:
                prediction = "Needs Improvement"

        except ValueError as error:
            prediction = str(error)

    return render_template(
        "index.html",
        prediction=prediction,
        study_hours=study_hours,
        attendance=attendance,
        previous_marks=previous_marks
    )


if __name__ == "__main__":
    app.run(debug=True)
