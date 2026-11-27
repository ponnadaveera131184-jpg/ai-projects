
from flask import Flask, render_template, request

app = Flask(__name__)

ROWS = 4
COLS = 4
GOAL = (3, 3)
OBSTACLE = (1, 1)

ACTIONS = {
    "UP": (-1, 0),
    "DOWN": (1, 0),
    "LEFT": (0, -1),
    "RIGHT": (0, 1)
}

GAMMA = 0.9
THETA = 0.001


def get_next_state(state, action):
    row, col = state
    dr, dc = ACTIONS[action]

    nr = row + dr
    nc = col + dc

    if not (0 <= nr < ROWS and 0 <= nc < COLS):
        return state

    if (nr, nc) == OBSTACLE:
        return state

    return (nr, nc)


def value_iteration():
    values = {
        (r, c): 0.0
        for r in range(ROWS)
        for c in range(COLS)
    }

    for iteration in range(1000):
        delta = 0

        for r in range(ROWS):
            for c in range(COLS):
                state = (r, c)

                if state == GOAL or state == OBSTACLE:
                    continue

                old_value = values[state]
                best_value = float("-inf")

                for action in ACTIONS:
                    next_state = get_next_state(state, action)

                    reward = 10 if next_state == GOAL else -1

                    new_value = reward + GAMMA * values[next_state]
                    best_value = max(best_value, new_value)

                values[state] = best_value
                delta = max(delta, abs(old_value - best_value))

        if delta < THETA:
            break

    return values, iteration + 1


def get_policy(values):
    policy = {}

    for state in values:
        if state == GOAL:
            policy[state] = "GOAL"
            continue

        if state == OBSTACLE:
            policy[state] = "BLOCKED"
            continue

        best_action = None
        best_value = float("-inf")

        for action in ACTIONS:
            next_state = get_next_state(state, action)
            reward = 10 if next_state == GOAL else -1
            value = reward + GAMMA * values[next_state]

            if value > best_value:
                best_value = value
                best_action = action

        policy[state] = best_action

    return policy


@app.route("/", methods=["GET", "POST"])
def index():
    values, iterations = value_iteration()
    policy = get_policy(values)

    show_result = request.method == "POST"

    return render_template(
        "index.html",
        values=values,
        policy=policy,
        rows=ROWS,
        cols=COLS,
        goal=GOAL,
        obstacle=OBSTACLE,
        iterations=iterations,
        show_result=show_result
    )


if __name__ == "__main__":
    app.run(debug=True)
