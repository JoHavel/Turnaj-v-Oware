import random


class Agent:
    name = "Agamemnon"

    depth = 5
    # 0 = Alexander
    # 1 = Traianus
    # 2 = +4 (po 100 hrách proti Traianovi)
    # 3 = +44
    # 4 = +36
    # 5 = +80
    # 6 - už se nestíhá na mém počítači
    # 7 - na mém ještě jde

    def max(self, game, depth):
        if depth == 0 or game.ended:
            return game.player_score

        return max(self.min(g, depth-1) for i in range(6)
                   if (g := game.copy()).play(i))

    def min(self, game, depth):
        if depth == 0 or game.ended:
            return game.opponent_score

        return min(self.max(g, depth-1) for i in range(6)
                   if (g := game.copy()).play(i))

    def play(self, game) -> None:
        if self.depth == 0:
            return

        best = -1
        best_index = []

        for i in range(6):
            if (g := game.copy()).play(i):
                score = self.min(g, self.depth-1)
                if score == best:
                    best_index.append(i)
                    continue
                if score > best:
                    best = score
                    best_index = [i]

        self.move = random.choice(best_index)
        return

    # Do tohoto uložte index vybraného ďolíku
    move = -1
