# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 10:13:21 2019

@author: Administrator
"""

## CODE FOR MINES IMPLEMENTATION

def dump(game):
    """Print a human-readable representation of game.

    Arguments:
       game (dict): Game state


    >>> dump({'dimensions': [1, 2], 'mask': [[False, False]], 'board': [['.', 1]], 'state': 'ongoing'})
    dimensions: [1, 2]
    board: ['.', 1]
    mask:  [False, False]
    state: ongoing
    """
    lines = ["dimensions: %s" % (game["dimensions"], ),
             "board: %s" % ("\n       ".join(map(str, game["board"])), ),
             "mask:  %s" % ("\n       ".join(map(str, game["mask"])), ),
             "state: %s" % (game["state"], ),
             ]
    print("\n".join(lines))

# Helper function
def fill_entry(rows, cols, value):
    """Return a rows*cols nested list.
    input:
        rows (int) : number of rows
        cols (int) : number of columns
        value (float) : value to be filled in each cell
    
    """
    ans = []
    for i in range(rows):
        r = []
        for j in range(cols):
            r.append(value)
        ans.append(r)
    return ans

def neibour_idx(num_rows, num_cols, r, c):
    """Return a list of index for neibours of (r,c).
    """
    ans = []
    for x in [r-1, r, r+1]:
        for y in [c-1, c, c+1]:
            if 0 <= x < num_rows:
                if 0 <= y < num_cols:
                    ans.append((x, y))
    return ans                    

def calcu_squares(game):
    """Return :
            bombs (int) : number of bombs have been found 
            covered_squares (int) : numbers of covered squares
    """
    bombs = 0
    covered_squares = 0
    for r in range(game["dimensions"][0]):
        for c in range(game["dimensions"][1]):
            if game["board"][r][c] == ".":
                if  game["mask"][r][c] == True:
                    bombs += 1
            elif game["mask"][r][c] == False:
                covered_squares += 1
    return bombs, covered_squares
# End helper function

def new_game(num_rows, num_cols, bombs):
    """Start a new game.

    Return a game state dictionary, with the "dimensions", "state", "board" and
    "mask" fields adequately initialized.

    Parameters:
       num_rows (int): Number of rows
       num_cols (int): Number of columns
       bombs (list): List of bombs, given in (row, column) pairs, which can be
                     either tuples or lists

    Returns:
       A game state dictionary

    >>> dump(new_game(2, 4, [(0, 0), (1, 0), (1, 1)]))
    dimensions: [2, 4]
    board: ['.', 3, 1, 0]
           ['.', '.', 1, 0]
    mask:  [False, False, False, False]
           [False, False, False, False]
    state: ongoing
    """
    # fill entry (revise 2)
    board = fill_entry(num_rows, num_cols, 0)
    for b in bombs:
        board[b[0]][b[1]] = '.'
    mask = fill_entry(num_rows, num_cols, False) # revise 2
    for r in range(num_rows):
        for c in range(num_cols):
            if board[r][c] == 0:
                neighbor_bombs = 0
                for x, y in neibour_idx(num_rows, num_cols, r, c): # revise 4
                    if board[x][y] == '.':
                        neighbor_bombs += 1
                board[r][c] = neighbor_bombs
    return {"dimensions": [num_rows, num_cols], "board" : board, "mask" : mask, "state": "ongoing"}


def reveal_squares(game, row, col):
    """Helper function: recursively reveal squares on the board, and return
    the number of squares that were revealed."""
    if game["board"][row][col] != 0:
        if game["mask"][row][col]:
            return 0
        else:
            game["mask"][row][col] = True
            return 1
    else:
        revealed = set()
        # conditions (revise 3) (revise 5)
        num_rows, num_cols = game["dimensions"]
        for r, c in neibour_idx(num_rows, num_cols, row, col):
            if game["board"][r][c] != '.' and not game["mask"][r][c]:
                game["mask"][r][c] = True
                revealed.add((r, c))
        total = len(revealed)
        for r,c in revealed:
            if game["board"][r][c] != "." :
                total += reveal_squares(game, r, c)
        return total
    
def dig(game, row, col):
    """Recursively dig up (row, col) and neighboring squares.

    Update game["mask"] to reveal (row, col); then recursively reveal (dig up)
    its neighbors, as long as (row, col) does not contain and is not adjacent
    to a bomb.  Return an integer indicating how many new squares were
    revealed.

    The state of the game should be changed to "defeat" when at least one bomb
    is visible on the board after digging (i.e. game["mask"][bomb_location] ==
    True), "victory" when all safe squares (squares that do not contain a bomb)
    and no bombs are visible, and "ongoing" otherwise.

    Parameters:
       game (dict): Game state
       row (int): Where to start digging (row)
       col (int): Where to start digging (col)

    Returns:
       int: the number of new squares revealed

    >>> game = {"dimensions": [2, 4],
    ...         "board": [[".", 3, 1, 0],
    ...                   [".", ".", 1, 0]],
    ...         "mask": [[False, True, False, False],
    ...                  [False, False, False, False]],
    ...         "state": "ongoing"}
    >>> dig(game, 0, 3)
    4
    >>> dump(game)
    dimensions: [2, 4]
    board: ['.', 3, 1, 0]
           ['.', '.', 1, 0]
    mask:  [False, True, True, True]
           [False, False, True, True]
    state: victory

    >>> game = {"dimensions": [2, 4],
    ...         "board": [[".", 3, 1, 0],
    ...                   [".", ".", 1, 0]],
    ...         "mask": [[False, True, False, False],
    ...                  [False, False, False, False]],
    ...         "state": "ongoing"}
    >>> dig(game, 0, 0)
    1
    >>> dump(game)
    dimensions: [2, 4]
    board: ['.', 3, 1, 0]
           ['.', '.', 1, 0]
    mask:  [True, True, False, False]
           [False, False, False, False]
    state: defeat
    """
    state = game["state"]
    if state == "defeat" or state == "victory":
        game["state"] = state
        return 0

    if game["board"][row][col] == '.':
        game["mask"][row][col] = True
        game["state"] = "defeat"
        return 1
    
    bombs, covered_squares = calcu_squares(game) # (revise 4)
    if bombs != 0:
        game["state"] = "defeat"
        return 0
    if covered_squares == 0:
        game["state"] = "victory"
        return 0

    revealed = reveal_squares(game, row, col)
    bombs, covered_squares = calcu_squares(game)  # (revise 4)
    bad_squares = bombs + covered_squares
    if bad_squares > 0:
        game["state"] = "ongoing"
        return revealed
    else:
        game["state"] = "victory"
        return revealed


def render(game, xray=False):
    """Prepare a game for display.

    Returns a two-dimensional array (list of lists) of "_" (hidden squares), "."
    (bombs), " " (empty squares), or "1", "2", etc. (squares neighboring bombs).
    game["mask"] indicates which squares should be visible.  If xray is True (the
    default is False), game["mask"] is ignored and all cells are shown.

    Parameters:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game["mask"]

    Returns:
       A 2D array (list of lists)

    >>> render({"dimensions": [2, 4],
    ...         "state": "ongoing",
    ...         "board": [[".", 3, 1, 0],
    ...                   [".", ".", 1, 0]],
    ...         "mask":  [[False, True, True, False],
    ...                   [False, False, True, False]]}, False)
    [['_', '3', '1', '_'], ['_', '_', '1', '_']]

    >>> render({"dimensions": [2, 4],
    ...         "state": "ongoing",
    ...         "board": [[".", 3, 1, 0],
    ...                   [".", ".", 1, 0]],
    ...         "mask":  [[False, True, False, True],
    ...                   [False, False, False, True]]}, True)
    [['.', '3', '1', ' '], ['.', '.', '1', ' ']]
    """
    x, y = game['dimensions']
    result = [[0]*y for i in range(x)]
    if xray :
        for i in range(x):
            for j in range(y):   
                if game['board'][i][j] == 0:
                    result[i][j] = ' '
                else:
                    result[i][j] = str(game['board'][i][j])
    else:
        for i in range(x):
            for j in range(y):
                reveal = game['mask'][i][j]
                value = game['board'][i][j]
                if not reveal:
                    result[i][j] = '_'
                elif value == 0:
                    result[i][j] = ' '
                else:
                    result[i][j] = str(value)
    return result   

def render_ascii(game, xray=False):
    """Render a game as ASCII art.

    Returns a string-based representation of argument "game".  Each tile of the
    game board should be rendered as in the function "render(game)".

    Parameters:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game["mask"]

    Returns:
       A string-based representation of game

    >>> print(render_ascii({"dimensions": [2, 4],
    ...                     "state": "ongoing",
    ...                     "board": [[".", 3, 1, 0],
    ...                               [".", ".", 1, 0]],
    ...                     "mask":  [[True, True, True, False],
    ...                               [False, False, True, False]]}))
    .31_
    __1_
    """
    x, y = game['dimensions']
    after_ren = render(game, xray)
    ans = ''
    for i in range(x):
        for j in range(y):
            ans = ans + after_ren[i][j]
        ans = ans + '\n'
    return ans[:-1]
