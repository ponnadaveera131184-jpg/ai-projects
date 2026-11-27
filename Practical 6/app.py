
from flask import Flask, render_template, request

app = Flask(__name__)

COLORS = ["Red", "Green", "Blue"]

GRAPH = {
    "A": ["B", "C"],
    "B": ["A", "C", "D"],
    "C": ["A", "B", "D"],
    "D": ["B", "C"]
}


def is_valid(node, color, assignment):
    for neighbor in GRAPH[node]:
        if assignment.get(neighbor) == color:
            return False
    return True


def backtracking(assignment):
    if len(assignment) == len(GRAPH):
        return True

    unassigned = [node for node in GRAPH if node not in assignment]
    node = unassigned[0]

    for color in COLORS:
        if is_valid(node, color, assignment):
            assignment[node] = color

            if backtracking(assignment):
                return True

            del assignment[node]

    return False


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    assignment = {}

    if request.method == "POST":
        if backtracking(assignment):
            result = "Map coloring completed successfully!"
        else:
            result = "No valid coloring found."

    return render_template(
        "index.html",
        graph=GRAPH,
        assignment=assignment,
        result=result
    )


if __name__ == "__main__":
    app.run(debug=True)
