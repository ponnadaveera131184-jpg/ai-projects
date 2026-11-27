
from flask import Flask, render_template, request

app = Flask(__name__)


def blocks_world(start, goal):
    steps = []
    current = start.copy()

    steps.append("Initial State: " + str(current))

    for block in goal:
        if block in current:
            current.remove(block)
            current.append(block)
            steps.append("Move Block " + block + " to the top")

    steps.append("Goal State: " + str(current))
    return steps, current


@app.route("/", methods=["GET", "POST"])
def index():
    steps = None
    final_state = None
    error = None

    if request.method == "POST":
        start = request.form.get("start", "").upper().split()
        goal = request.form.get("goal", "").upper().split()

        if (not start or not goal or
                len(start) != len(set(start)) or
                len(goal) != len(set(goal)) or
                set(start) != set(goal)):
            error = "Enter the same unique blocks in both states."
        else:
            steps, final_state = blocks_world(start, goal)

    return render_template(
        "index.html",
        steps=steps,
        final_state=final_state,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True)
