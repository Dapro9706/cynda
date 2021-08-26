import discord


def check4(a, b, c, d):
    return a == b == c == d


def isDone(board):
    boardHeight = len (board[0])
    boardWidth = len (board)
    # check horizontal spaces
    for y in range (boardHeight):
        for x in range (boardWidth - 3):
            if check4 (board[x][y], board[x + 1][y], board[x + 2][y], board[x + 3][y]):
                return [True, board[x][y]]

    # check vertical spaces
    for x in range (boardWidth):
        for y in range (boardHeight - 3):
            if check4 (board[x][y], board[x][y + 1], board[x][y + 2], board[x][y + 3]):
                return [True, board[x][y]]

    # check / diagonal spaces
    for x in range (boardWidth - 3):
        for y in range (3, boardHeight):
            if check4 (board[x][y], board[x + 1][y - 1], board[x + 2][y - 2], board[x + 3][y - 3]):
                return [True, board[x + 1][y - 1]]

    # check \ diagonal spaces
    for x in range (boardWidth - 3):
        for y in range (boardHeight - 3):
            if check4 (board[x][y], board[x + 1][y + 1], board[x + 2][y + 2], board[x + 3][y + 3]):
                return [True, board[x + 1][y + 1]]

    count = 0
    for x in range (boardWidth):
        for y in range (boardHeight):
            if not board[x][y] == " ":
                count += 1
    if count == boardWidth * boardHeight:
        return [True, None]
    return [False, 0]


def playc4(board, player, col):
    for i in range (6):
        if board[5 - i][col] == " ":
            board[5 - i][col] = player
            return board
    raise RuntimeError ("Already filled Column")


def check_possibile(board):
    count = []
    for i in range (7):
        if board[0][i] == " ":
            count.append (i)
    return count


async def show_boardc4(ctx, board):
    send = ""
    for i in range (6):
        for j in range (7):
            if board[i][j] == "X":
                send += ":red_circle:"
            elif board[i][j] == "O":
                send += ":blue_circle:"
            else:
                send += ":black_circle:"
        send += "\n"
    e = discord.Embed (title="Connect-4", description=send, color=51)
    await ctx.send (embed=e)
