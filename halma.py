NEUTRAL = 0
RED = 1
GREEN = 2

from Board import Board
from Pawn import Pawn

class Halma:
    def __init__(self, board_size=8):
        self.board_size = board_size

        # set board with all blank
        self.board = [[0 for _ in range(self.board_size)] for _ in range(self.board_size)]

        # init pawns
        for i in range(self.board_size):
            for j in range(self.board_size):
                self.board[i][j] = self.get_home_info(i, j)

        # set goal
        self.goal_r = [i for row in self.board for i in row if i.kind == RED]
        self.goal_g = [i for row in self.board for i in row if i.kind == GREEN]

        self.board = Board(self.board)
        print(self.board)

    def move(self, from_x, to_x, from_y, to_y):
        self.board[to_x][to_y] = self.board[from_x][from_y]
        self.board[from_x][from_y] = 0

    def get_home_info(self, x, y):
        if x + y < 4:
            return Pawn(x, y, 1)
        elif x + y > self.board_size + 2:
            return Pawn(x, y, 2)
        else:
            return Pawn(x, y)

    def is_on_board(self, x, y):
        return 0 <= x < self.board_size and 0 <= y < self.board_size

    def check_winner(self):
        pass

if __name__ == "__main__":
    halma = Halma()
