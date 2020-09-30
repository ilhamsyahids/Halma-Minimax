
class Pawn:
  def __init__(self, x, y, kind = 0):
    self.x = x
    self.y = y
    self.kind = kind

  def __str__(self):
    return chr(self.y + 65) + str(self.x + 1)
