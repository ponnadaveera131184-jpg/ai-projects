
from flask import Flask, render_template, request
import heapq

app = Flask(__name__)

GOAL = (1, 2, 3, 4, 5, 6, 7, 8, 0)


def heuristic(state, method):
    distance = 0

    for i, value in enumerate(state):
        if value == 0:
            continue

        if method == "misplaced":
            if value != GOAL[i]:
                distance += 1
        else:
            current_row, current_col = divmod(i, 3)
            goal_row, goal_col = divmod(value - 1, 3)
            distance += abs(current_row - goal_row) + abs(current_col - goal_col)

    return distance


def get_neighbors(state):
    zero = state.index(0)
    row, col = divmod(zero, 3)

    moves = []

    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = row + dr, col + dc

        if 0 <= nr < 3 and 0 <= nc < 3:
            new_pos = nr * 3 + nc
            new_state = list(state)
            new_state[zero], new_state[new_pos] = new_state[new_pos], new_state[zero]
            moves.append(tuple(new_state))

    return moves


def is_solvable(state):
    numbers = [x for x in state if x != 0]
    inversions = 0

    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            if numbers[i] > numbers[j]:
                inversions += 1

    return inversions % 2 == 0


def astar(start, method):
    queue = []
    heapq.heappush(queue, (heuristic(start, method), 0, start))

    parent = {start: None}
    cost = {start: 0}
    explored = 0

    while queue:
        _, g, current = heapq.heappop(queue)
        explored += 1

        if current == GOAL:
            path = []
            while current is not None:
                path.append(list(current))
                current = parent[current]

            return path[::-1], explored

        for neighbor in get_neighbors(current):
            new_cost = g + 1

            if neighbor not in cost or new_cost < cost[neighbor]:
                cost[neighbor] = new_cost
                parent[neighbor] = current

                f = new_cost + heuristic(neighbor, method)
                heapq.heappush(queue, (f, new_cost, neighbor))

    return None, explored


@app.route("/", methods=["GET", "POST"])
def index():
    solution = None
    explored = 0
    error = None
    method = "manhattan"

    if request.method == "POST":
        try:
            values = [int(x) for x in request.form["board"].replace(",", " ").split()]
            method = request.form.get("heuristic", "manhattan")

            if len(values) != 9 or sorted(values) != list(range(9)):
                raise ValueError("Enter all numbers from 0 to 8 exactly once.")

            if method not in ["manhattan", "misplaced"]:
                raise ValueError("Invalid heuristic selected.")

            start = tuple(values)

            if not is_solvable(start):
                error = "This puzzle cannot be solved."
            else:
                solution, explored = astar(start, method)

        except ValueError as e:
            error = str(e)

    return render_template(
        "index.html",
        solution=solution,
        explored=explored,
        error=error,
        method=method
    )


if __name__ == "__main__":
    app.run(debug=True)
