
class Board:
  def __init__(self, board):
    self.board = board
    self.size = len(board)

  def __str__(self):
    string = ""
    for i in range(self.size + 1):
      for j in range(self.size + 1):
        if i == 0 and j == 0:
          string += '  '
          continue
        if i == 0:
          string += chr(j + 64) + '  '
          continue
        if j == 0:
          string += str(i) + ' '
          continue
        string += str(self.board[i - 1][j - 1]) + ' '
      string += '\n'

    return string
