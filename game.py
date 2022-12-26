class Game:

    def __init__(self, id):

        # reveals if player 1 and 2 have moved
        self.p1_went = False
        self.p2_went = False
        self.ready = False

        # unique ID to determine what client is in what game
        self.id = id
        self.moves = [None, None]
        self.wins = [0, 0]
        self.draws = 0

    # player is in the range of [0,1]
    def get_player_move(self, player):
        return self.moves[player]

    # update our move list with other players move
    def play(self, player, move):
        self.moves[player] = move
        if player == 0:
            self.p1_went = True
        else:
            self.p2_went = True

    # reveals if both players are ready
    def connected(self):
        return self.ready

    # return if both players used a move
    def both_went(self):
        return self.p1_went and self.p2_went

    # obtain the move that each player used
    def winner(self):
        p1 = self.moves[0]
        p2 = self.moves[1]

        # calculate which player has won the game based on selected move
        winner = -1
        if p1 == "Rock" and p2 == "Scissors":
            winner = 0
        elif p1 == "Scissors" and p2 == "Rock":
            winner = 1
        elif p1 == "Scissors" and p2 == "Paper":
            winner = 0
        elif p1 == "Rock" and p2 == "Paper":
            winner = 1
        elif p1 == "Paper" and p2 == "Scissors":
            winner = 1
        elif p1 == "Paper" and p2 == "Rock":
            winner = 0

        return winner

    def reset(self):
        self.p1_went = False
        self.p2_went = False
