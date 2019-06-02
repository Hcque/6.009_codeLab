"""6.009 Lab 4 -- HyperMines"""

import sys
sys.setrecursionlimit(10000)
# NO ADDITIONAL IMPORTS


# Helper functions
def build_init(dims, value):
    """Return a high dimensional nested list.
    
    Args:
        dims(list) : dimension list
        value (float/bool) : value to be filled in each cell
    
    >>> build_init([3,2], 0)
    [[0, 0], [0, 0], [0, 0]]
    """
    # base case
    if len(dims) == 1:
        return [value]*dims[0]

    return [build_init(dims[1:], value) for i in range(dims[0])]


def get_value(coor, board):
    """Return value in certain coordinate.
    
    Args:
        coor (list) : coorndinate of point of which value to be gotten
        board (nested list) : a high dimensional grid
    >>> board = [[1,2,3],
    ...          [4,5,6]]
    >>> get_value([1,1], board)
    5
    """
    # base case
    if len(coor) == 1:
        return board[coor[0]]
    
    return get_value(coor[1:], board[coor[0]])


def replace_value(coor, value, board):
    """Change value to coor's positions. 
    
    Args:
        coor (list) : coorodante 
        board (nested lists)
        value (float / bool): value filled in the rest cells
        
    >>> board = [[1,2,3],
    ...          [5,5,5]]
    >>> replace_value([0,0], 0, board)
    >>> print(board)
    [[0, 2, 3], [5, 5, 5]]
    """
    # base case
    if len(coor) == 1:
        board[coor[0]] = value
    else:
        replace_value(coor[1:], value, board[coor[0]])


def get_neighbors(coor, dims, board):
    """
    Args:
        coor (list) : the place to get neighbors
        dims (list) : dimensions of board
        board (nested list)
    
    Return:
        a generator object contain all neighbors' coordinates
        
    >>> board = [[1,2,3,4],
    ...          [5,6,7,8],
    ...          [9,10,11,12]]                
    >>> list(get_neighbors([1,1], [3,4], board))
    [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
    """
    if len(coor) == 0:
        yield ()
    else:
        yield from ((i,)+j for i in [coor[0]-1, coor[0], coor[0]+1] \
                    for j in get_neighbors(coor[1:], dims[1:], board[coor[0]])\
                    if 0 <= i < dims[0])
    
    
def get_coors(dims):
    """
    Args:
        dims (list) : dimensions of board
    Return:
        generator of all coordinates in the board
    >>> list(get_coors([3,2]))
    [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)]
    """
    if len(dims) == 0:
        yield ()
    else:
        yield from ((i,)+j for i in range(dims[0]) for j in get_coors(dims[1:]))
# End helper functions


class HyperMinesGame:
    def __init__(self, dims, bombs):
        """Start a new game.

        This method should properly initialize the "board", "mask",
        "dimensions", and "state" attributes.

        Args:
           dims (list): Dimensions of the board
           bombs (list): Bomb locations as a list of lists, each an
                         N-dimensional coordinate

        >>> g = HyperMinesGame([2, 4, 2], [[0, 0, 1], [1, 0, 0], [1, 1, 1]])
        >>> g.dump()
        dimensions: [2, 4, 2]
        board: [[3, '.'], [3, 3], [1, 1], [0, 0]]
               [['.', 3], [3, '.'], [1, 1], [0, 0]]
        mask:  [[False, False], [False, False], [False, False], [False, False]]
               [[False, False], [False, False], [False, False], [False, False]]
        state: ongoing
        """
        self.dimensions = dims
        self.board = build_init(dims, 0)
        for c in bombs:
            replace_value(c, '.', self.board)
        for coor in get_coors(dims):
            if get_value(coor, self.board) == 0:
                neighb_bombs = 0
                for c in get_neighbors(coor, dims, self.board):
                    if get_value(c, self.board) == '.':
                        neighb_bombs += 1
                replace_value(coor, neighb_bombs, self.board)
                
        self.mask = build_init(dims, False)
        self.state = 'ongoing'

    def dump(self):
        """Print a human-readable representation of this game."""
        lines = ["dimensions: %s" % (self.dimensions, ),
                 "board: %s" % ("\n       ".join(map(str, self.board)), ),
                 "mask:  %s" % ("\n       ".join(map(str, self.mask)), ),
                 "state: %s" % (self.state, )]
        print("\n".join(lines))


    def dig(self, coords):
        """Recursively dig up square at coords and neighboring squares.

        Update the mask to reveal square at coords; then recursively reveal its
        neighbors, as long as coords does not contain and is not adjacent to a
        bomb.  Return a number indicating how many squares were revealed.  No
        action should be taken and 0 returned if the incoming state of the game
        is not "ongoing".

        The updated state is "defeat" when at least one bomb is visible on the
        board after digging, "victory" when all safe squares (squares that do
        not contain a bomb) and no bombs are visible, and "ongoing" otherwise.

        Args:
           coords (list): Where to start digging

        Returns:
           int: number of squares revealed

        >>> g = HyperMinesGame.from_dict({"dimensions": [2, 4, 2],
        ...         "board": [[[3, '.'], [3, 3], [1, 1], [0, 0]],
        ...                   [['.', 3], [3, '.'], [1, 1], [0, 0]]],
        ...         "mask": [[[False, False], [False, True], [False, False], [False, False]],
        ...                  [[False, False], [False, False], [False, False], [False, False]]],
        ...         "state": "ongoing"})
        >>> g.dig([0, 3, 0])
        8
        >>> g.dump()
        dimensions: [2, 4, 2]
        board: [[3, '.'], [3, 3], [1, 1], [0, 0]]
               [['.', 3], [3, '.'], [1, 1], [0, 0]]
        mask:  [[False, False], [False, True], [True, True], [True, True]]
               [[False, False], [False, False], [True, True], [True, True]]
        state: ongoing
        >>> g = HyperMinesGame.from_dict({"dimensions": [2, 4, 2],
        ...         "board": [[[3, '.'], [3, 3], [1, 1], [0, 0]],
        ...                   [['.', 3], [3, '.'], [1, 1], [0, 0]]],
        ...         "mask": [[[False, False], [False, True], [False, False], [False, False]],
        ...                  [[False, False], [False, False], [False, False], [False, False]]],
        ...         "state": "ongoing"})
        >>> g.dig([0, 0, 1])
        1
        >>> g.dump()
        dimensions: [2, 4, 2]
        board: [[3, '.'], [3, 3], [1, 1], [0, 0]]
               [['.', 3], [3, '.'], [1, 1], [0, 0]]
        mask:  [[False, True], [False, True], [False, False], [False, False]]
               [[False, False], [False, False], [False, False], [False, False]]
        state: defeat
        """
        state = self.state
        if state == "defeat" or state == "victory":
            return 0
        
        if get_value(coords, self.board) == '.':  
            replace_value(coords, True, self.mask)
            self.state = "defeat"
            return 1
        
        bombs, covered_squares = self.calcu_squares() 
        if bombs != 0:
            self.state = "defeat"
            return 0
        if covered_squares == 0:
            self.state = "victory"
            return 0
        
        revealed = self.reveal_squares(coords) 
        bombs, covered_squares = self.calcu_squares()  
        bad_squares = bombs + covered_squares
        if bad_squares > 0:
            self.state = "ongoing"
            return revealed
        else:
            self.state = "victory"
            return revealed
        
    def reveal_squares(self, coor):
        """Helper function: recursively reveal squares on the board, and return
        the number of squares that were revealed.
        >>> g = HyperMinesGame([2, 3], [[0, 0], [1, 0], [1, 1]])
        >>> g.reveal_squares([0,0])
        1
        """
        if get_value(coor, self.board) != 0:
            if get_value(coor, self.mask):
                return 0
            else:
                replace_value(coor, True, self.mask)
                return 1
        else:
            revealed = set()
            for c in get_neighbors(coor, self.dimensions, self.board):
                if get_value(c, self.board) != '.' and not get_value(c, self.mask):
                    replace_value(c, True, self.mask)
                    revealed.add(c)
            total = len(revealed)
            for coo in revealed:
                if get_value(coo, self.board) != "." :
                    total += self.reveal_squares(coo)
            return total
    
    def calcu_squares(self):
        """
        Return :
            bombs (int) : number of bombs have been found 
            covered_squares (int) : numbers of covered squares
        
        >>> g = HyperMinesGame([2, 3], [[0, 0], [1, 0], [1, 1]])
        >>> print(g.calcu_squares())
        (0, 3)        
        """
        bombs = 0
        covered_squares = 0
        for coor in get_coors(self.dimensions):
            if get_value(coor, self.board) == ".":
                if get_value(coor, self.mask) == True:
                    bombs += 1
            elif get_value(coor, self.mask) == False:
                covered_squares += 1
        return bombs, covered_squares
        
    def render(self, xray=False):
        """Prepare the game for display.

        Returns an N-dimensional array (nested lists) of "_" (hidden squares),
        "." (bombs), " " (empty squares), or "1", "2", etc. (squares
        neighboring bombs).  The mask indicates which squares should be
        visible.  If xray is True (the default is False), the mask is ignored
        and all cells are shown.

        Args:
           xray (bool): Whether to reveal all tiles or just the ones allowed by
                        the mask

        Returns:
           An n-dimensional array (nested lists)

        >>> g = HyperMinesGame.from_dict({"dimensions": [2, 4, 2],
        ...            "board": [[[3, '.'], [3, 3], [1, 1], [0, 0]],
        ...                      [['.', 3], [3, '.'], [1, 1], [0, 0]]],
        ...            "mask": [[[False, False], [False, True], [True, True], [True, True]],
        ...                     [[False, False], [False, False], [True, True], [True, True]]],
        ...            "state": "ongoing"})
        >>> g.render(False)
        [[['_', '_'], ['_', '3'], ['1', '1'], [' ', ' ']],
         [['_', '_'], ['_', '_'], ['1', '1'], [' ', ' ']]]

        >>> g.render(True)
        [[['3', '.'], ['3', '3'], ['1', '1'], [' ', ' ']],
         [['.', '3'], ['3', '.'], ['1', '1'], [' ', ' ']]]
        """
        # build new 
        dims = self.dimensions
        board = self.board
        result = build_init(dims, 0)
        
        if xray :
            for coor in get_coors(dims):  
                if get_value(coor, board) == 0: 
                    replace_value(coor, ' ', result)
                else:
                    value = get_value(coor, board)
                    replace_value(coor, str(value), result)
        else:
            for coor in get_coors(dims): 
                reveal = get_value(coor, self.mask)
                value = get_value(coor, self.board)
                if not reveal:
                    replace_value(coor, '_', result)
                elif value == 0:
                    replace_value(coor, ' ', result)
                else:
                    replace_value(coor, str(value), result)
        return result   


    @classmethod
    def from_dict(cls, d):
        """Create a new instance of the class with attributes initialized to
        match those in the given dictionary."""
        game = cls.__new__(cls)
        for i in ('dimensions', 'board', 'state', 'mask'):
            setattr(game, i, d[i])
        return game


if __name__ == '__main__':
    import doctest
    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    doctest.testmod(optionflags=_doctest_flags)
    
    # answer questions
    dims = [[10], [10,20], [10,20,3]]
    coors = [[5], [5, 13], [5,13,0]]
    for dim,coor in zip(dims, coors):
        g = HyperMinesGame(dim, [])
        print()
        print(list((get_neighbors(coor, g.dimensions, g.board))))
    
    
    
    
