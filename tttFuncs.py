import PIL
from PIL import ImageDraw
import discord.file
import discord.embeds


def play(bboard, player, spot):
    board = bboard
    if board[spot[0]][spot[1]] == " ":
        board[spot[0]][spot[1]] = player
        return board
    else:
        raise RuntimeError ("Already Played Position")


async def show_board(ctx, board, img: PIL):
    draw = ImageDraw.Draw (img)
    send = ""
    st = ":regional_indicator_"
    for i in range (3):
        for j in range (3):
            if board[i][j] == "X":
                draw.line ((120 * j + 30, 120 * i + 30, 120 * (j + 1) - 30,  120 * (i + 1) - 30), fill=(255, 0, 0),
                           width=2)
                draw.line ((120 * (j + 1) - 30, 120 * i + 30,  120 * j + 30, 120 * (i + 1) - 30), fill=(255, 0, 0),
                           width=2)
            elif board[i][j] == "O":
                draw.ellipse ((120 * j + 30, 120 * i + 30, 120 * (j + 1) - 30, 120 * (i + 1) - 30), outline=(0, 255, 0),
                              width=2)
    img.save ("data/board1.png")
    file = discord.File ("data/board1.png",filename="board.png")
    e = discord.Embed (title="TicTacToe")
    e.set_image (url="attachment://board.png")
    await ctx.send (file=file, embed=e)


async def log(ctx, str):
    await ctx.send ("> "+str)


def equals3(a, b, c):
    return True if (a == b == c and not a == " ") else False


def is_done(board):
    ret = [False, 0]

    # Check Win
    for i in range (3):
        if equals3 (board[i][0], board[i][1], board[i][2]):
            ret = [True, board[i][0]]
            break
        elif equals3 (board[0][i], board[1][i], board[2][i]):
            ret = [True, board[0][i]]
            break
    if not ret[0]:
        if equals3 (board[0][0], board[1][1], board[2][2]):
            ret = [True, board[0][0]]
        elif equals3 (board[2][0], board[1][1], board[0][2]):
            ret = [True, board[0][2]]
        count = 0

        # check draw
        for i in range (9):
            if not board[i // 3][i % 3] == " ":
                count += 1

        if count == 9:
            ret = [True, None]
    return ret


def find_all_empty(board):
    ret = []
    for i in range (9):
        if board[i // 3][i % 3] == " ":
            ret.append (i)
    return ret


def best_move(board):
    best_score = -infinity
    move = None
    for i in find_all_empty (board):
        score = minimax (play (board, "X", (i // 3, i % 3)), 0, -infinity, infinity, False)
        board[i // 3][i % 3] = " "
        if score > best_score:
            best_score = score
            move = i
    return move


scores = {
    "lose": -10,
    "win": 10,
    "tie": -5
}

infinity = 1000000000


def minimax(board, depth, alpha, beta, is_maximizing):
    result = is_done (board)
    if result[1] is None:
        return scores["tie"]
    elif result[1] == "X":
        return scores["win"]
    elif result[1] == "O":
        return scores["lose"]
    elif is_maximizing:
        best_score = -infinity
        for i in find_all_empty (board):
            score = minimax (play (board, 'X', (i // 3, i % 3)), depth + 1, alpha, beta, False)
            board[i // 3][i % 3] = " "
            best_score = max (score, best_score)
            alpha = max (best_score, alpha)
            if beta <= alpha:
                break
        return best_score
    else:
        best_score = infinity
        for i in find_all_empty (board):
            score = minimax (play (board, 'O', (i // 3, i % 3)), depth + 1, alpha, beta, True)
            board[i // 3][i % 3] = " "
            best_score = min (score, best_score)
            beta = min (best_score, beta)
            if beta <= alpha:
                break
        return best_score
