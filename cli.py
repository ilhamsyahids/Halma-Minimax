import Halma

class CLI:
    def __init__(self):
        # init settings
        self.board_size = 8
        self.time_limit = 60  # in seconds
        self.human_player = Halma.RED

        self.start_game()

        print("-> HALMA <-")
        print("== MENU ==")
        print("1 | Start Game")
        print("2 | Settings")
        print("0 | Exit")
        print()

        selected_menu = input("=> ")
        if selected_menu == '1':
            self.select_game_mode()

    def select_game_mode(self):
        print("-> START GAME <-")
        print("== SELECT GAME MODE ==")
        print("1 | Human vs Human")
        print("2 | Human vs Minimax Bot")
        print("3 | Human vs Minimax + Local Search Bot")
        print("4 | Minimax Bot vs Minimax + Local Search Bot")
        print("0 | Back")
        print()

    def select_board_size(self):
        print("-> START GAME <-")
        print("== SELECT BOARD SIZE ==")
        print("1 | 8x8")
        print("2 | 10x10")
        print("3 | 16x16")
        print()

    def start_game(self):
        self.game = Halma.Halma(self.board_size)


cli = CLI()
