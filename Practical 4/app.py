
from flask import Flask, render_template, request
import math

app = Flask(__name__)

EMPTY = " "
HUMAN = "X"
AI = "O"

WINNING_COMBINATIONS = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6)
]


def check_winner(board):
    for a, b, c in WINNING_COMBINATIONS:
        if board[a] == board[b] == board[c] != EMPTY:
            return board[a]

    if EMPTY not in board:
        return "Draw"

    return None


def minimax(board, depth, is_maximizing, alpha, beta):
    result = check_winner(board)

    if result == AI:
        return 10 - depth
    if result == HUMAN:
        return depth - 10
    if result == "Draw":
        return 0

    if is_maximizing:
        best_score = -math.inf

        for i in range(9):
            if board[i] == EMPTY:
                board[i] = AI
                score = minimax(board, depth + 1, False, alpha, beta)
                board[i] = EMPTY

                best_score = max(best_score, score)
                alpha = max(alpha, best_score)

                if beta <= alpha:
                    break

        return best_score

    else:
        best_score = math.inf

        for i in range(9):
            if board[i] == EMPTY:
                board[i] = HUMAN
                score = minimax(board, depth + 1, True, alpha, beta)
                board[i] = EMPTY

                best_score = min(best_score, score)
                beta = min(beta, best_score)

                if beta <= alpha:
                    break

        return best_score


def find_best_move(board):
    best_score = -math.inf
    best_move = None

    for i in range(9):
        if board[i] == EMPTY:
            board[i] = AI
            score = minimax(board, 0, False, -math.inf, math.inf)
            board[i] = EMPTY

            if score > best_score:
                best_score = score
                best_move = i

    return best_move


@app.route("/", methods=["GET", "POST"])
def index():
    board = [EMPTY] * 9
    message = "Your turn! You are X."
    game_over = False

    if request.method == "POST":
        board = request.form.getlist("board")

        if len(board) != 9 or any(x not in ["X", "O", " "] for x in board):
            board = [EMPTY] * 9

        action = request.form.get("action")

        if action == "reset":
            board = [EMPTY] * 9

        else:
            if not game_over and check_winner(board) is None:
                move = request.form.get("move", "")

                if move.isdigit():
                    position = int(move)

                    if 0 <= position < 9 and board[position] == EMPTY:
                        board[position] = HUMAN

                        if check_winner(board) is None:
                            ai_move = find_best_move(board)

                            if ai_move is not None:
                                board[ai_move] = AI

    result = check_winner(board)

    if result == HUMAN:
        message = "Congratulations! You won!"
        game_over = True
    elif result == AI:
        message = "AI wins! Better luck next time."
        game_over = True
    elif result == "Draw":
        message = "It's a draw!"
        game_over = True
    else:
        message = "Your turn! You are X."

    return render_template(
        "index.html",
        board=board,
        message=message,
        game_over=game_over
    )


if __name__ == "__main__":
    app.run(debug=True)
