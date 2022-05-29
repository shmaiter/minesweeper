import random
import re

# we need to create a board object that represents the minesweeper track,
# where we are gonna need to create some functions like: "create new borad object",
# "dig here" or "render this game for this object"


class Board:
    def __init__(self, dim_size, num_bombs):
        # keep track of this variables globally
        self.dim_size = dim_size
        self.num_bombs = num_bombs

        # let's create a board
        self.board = self.make_new_board()
        self.assing_values_to_board()

        # initialize a set to keep track of locations that were uncovered
        # locations will be save as tuples into the set
        self.dug = set()  # if user digit 0, 0, then self.dug = {(0, 0)}

    def make_new_board(self):
        # construct a new board based on the di size and num bombs
        # we should construct the list of lists here (or whatever representation you prefer,
        # but since we have a 2-D board, list of lists is most natural)

        # generate a new board
        board = [[None for _ in range(self.dim_size)]
                 for _ in range(self.dim_size)]
        # array created will look like this
        # [[None, None, ..., None
        # [None, None, ..., None]
        # [...                  ]
        # [None, None, ..., None]]

        # plant the bombs
        bombs_planted = 0
        while bombs_planted < self.num_bombs:
            # Exponentiation: 2**5 same as 2*2*2*2*2
            # return a random integer N such that a < N < b
            loc = random.randint(0, self.dim_size**2 - 1)

            # the floor division // rounds the result down to the nearest whole number
            # we want the number of times dim_size goes into loc to tell
            row = loc // self.dim_size
            col = loc % self.dim_size  # we want the ramainder to tell us what index in that row to

            if board[row][col] == '*':
                # we've already planted a bomb on this loc so continue to the next iteration
                continue

            board[row][col] = '*'  # plant the bomb
            bombs_planted += 1

        return board

    def assing_values_to_board(self):
        # assing values from 0-8 for empty spaces, which
        # represents how many neighboring bombs there are. We can precompute these and it'll save us some
        # effort checking what's around the board later on.
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == "*":
                    # if this is already a bomb, we don't want to calculate anything
                    continue
                self.board[r][c] = self.get_num_neighboring_bombs(r, c)

    def get_num_neighboring_bombs(self, row, col):
        # let's iterate through each of the neighboring positions and sum number of bombs

        # LIST OF POSITIONS AROUND THE CURRENT LOCATION
        # top left: (row-1, col-1)
        # top middle: (row-1, col)
        # top right: (row-1, col+1)
        # left: (row, col-1)
        # right: (row, col+1)
        # bottom left: (row+1, col-1)
        # bottom middle: (row+1, col)
        # bottom right: (row+1, col+1)

        # make sure to not go out of bounds!
        num_neighboring_bombs = 0
        # check above and below rows
        for r in range(max(0, row-1), min(self.dim_size-1, row+1)+1):
            # check above and below rows
            for c in range(max(0, col-1), min(self.dim_size-1, col+1)+1):
                if r == row and c == col:
                    # don't check original location
                    continue

                if self.board[r][c] == '*':
                    num_neighboring_bombs += 1

        return num_neighboring_bombs

    def dig(self, row, col):
        # dig the location
        # return True if isn't a bomb, other wise False

        # a few scenarios:
        # 1. hit a bomb -> game over
        # 2. dig at location with neighboring bombs -> finish dig
        # 3. dig at location with no neighboring bombs -> recursively dig neighbors!

        self.dug.add((row, col))  # keep track that we dug here

        if self.board[row][col] == '*':
            return False
        elif self.board[row][col] > 0:
            return True

        # self.board[row][col] == 0
        for r in range(max(0, row-1), min(self.dim_size-1, row+1)+1):  # check above and below rows
            # check above and below rows
            for c in range(max(0, col-1), min(self.dim_size-1, col+1)+1):
                if (r, c) in self.dug:
                    continue  # don't dig where you've already dug
                self.dig(r, c)
        return True

    def __str__(self):
        # this is a magic function where if you call print on this object,
        # it'll print out what this function returns
        # return a string that shows the board to the player

        visible_board = [[None for _ in range(
            self.dim_size)] for _ in range(self.dim_size)]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row, col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = ' '

        # put this together on a string
        string_rep = ''

        # get max column widths for printing
        widths = []
        for idx in range(self.dim_size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(
                len(
                    max(columns, key=len)
                )
            )

        # print the csv strings
        indices = [i for i in range(self.dim_size)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'

        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / self.dim_size)
        string_rep = indices_row + '-'*str_len + '\n' + string_rep + '-'*str_len

        return string_rep


def play(dim_size=10, num_bombs=10):
    # Step 1: create board and plant the bombs
    board = Board(dim_size, num_bombs)

    # Step 2: show the user the borad and ask for where they want to dig

    # Step 3a: if location is a bomb, show game over message
    # Step 3b: if location is not a bomb, dig recursively until each square is
    #          at least next to a bomb
    # Step 4: repeat steps 2 and 3a/3b until theres no more places to dig, so VICTORY!

    safe = True
    while len(board.dug) < board.dim_size ** 2 - num_bombs:
        print(board)

        # 0,0 or 0, 0 or 0,    0
        user_input = re.findall(
            r'[^,\s]+', input("Where would you like to dig? Input as row, col: "))
        print(user_input)
        row, col = int(user_input[0]), int(user_input[-1])
        if row < 0 or row >= board.dim_size or col < 0 or col >= dim_size:
            print("Invalid location. Try another location in range 0-8")
            continue

        # if it's valid we dig
        safe = board.dig(row, col)
        if not safe:
            break  # game over

    if safe:
        print("CONGRATULATIONS!!!! YOU WON!!")
    else:
        # dug a bomb
        print("SORRY GAME OVER")
        board.dug = [(r, c) for r in range(board.dim_size)
                     for c in range(board.dim_size)]
        print(board)


if __name__ == '__main__':
    play()
