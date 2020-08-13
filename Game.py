from random import randrange
import numpy as np


# Here is the game setup for MineSweeper, where the bombs are -1, and all other numbers
#     represent proximity to the bombs.
class Game:

    def __init__(self, num_tiles):
        if num_tiles == 80:
            self.tiles = (8, 10)
            self.number_bombs = 10
            self.board = np.zeros(self.tiles, dtype=int)
        elif num_tiles == 252:
            self.tiles = (14, 18)
            self.number_bombs = 40
            self.board = np.zeros(self.tiles, dtype=int)
        elif num_tiles == 480:
            self.tiles = (20, 24)
            self.number_bombs = 99
            self.board = np.zeros(self.tiles, dtype=int)
        else:
            print('We cannot support this number of tiles yet. Please try 80, 252, or 480.')
            exit(1)

        while np.sum(self.board) > -self.number_bombs:
            position = randrange(num_tiles)
            position_y = int(np.floor(position / self.tiles[0]))
            position_x = position % self.tiles[0]
            if not self.board[position_x][position_y]:
                self.board[position_x][position_y] = -1

        # At this point, the bombs are placed, so let's
        #    set up proximity values, where pos is a pair
        #    of coordinates

        def find_number(posx, posy):
            main_box = self.board[posx][posy]
            to_place = 0
            neighbors = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))

            # Check that the coordinates exist and then check the box
            for x in neighbors:
                check_box = (x[0] + posx, x[1] + posy)
                if check_box[0] in range(self.tiles[0]) and check_box[1] in range(self.tiles[1]):
                    # We now know this position is real
                    if self.board[check_box[0]][check_box[1]] < 0:
                        to_place += 1

            return to_place

        for i in range(self.tiles[0]):
            for j in range(self.tiles[1]):
                if self.board[i][j] != -1:
                    self.board[i][j] = find_number(i, j)

    def display_board(self):
        for i in range(self.tiles[0]):
            for j in range(self.tiles[1]):
                print(self.board[i][j], end=' ')
            print('')

    def find_pos(self, x, y):
        return self.board[x][y]
