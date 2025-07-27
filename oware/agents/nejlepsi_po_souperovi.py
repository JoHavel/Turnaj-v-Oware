import random


class Agent:
    name = "Napoleon Bonaparte"

    @staticmethod
    def best_move(game, deep: int) -> int:
        best = -1
        best_index = 0
        for i in range(6):
            game_copy = game.copy()
            # play odehraje (na kopii) a vrátí, zda byl tah validní
            if game_copy.play(i, rotate=False):
                if deep != 0:
                    game_copy.rotate()
                    game_copy.play(Agent.best_move(game_copy.copy(), deep - 1))
                if game_copy.player_score > best:
                    best = game_copy.player_score
                    best_index = i
        return best_index

    def play(self, game) -> None:
        nase_skore = game.player_score
        skore_soupere = game.opponent_score
        nase_doliky = game.player_pits       # Proti směru hodinových ručiček
        doliky_soupere = game.opponent_pits  # -            ||              -

        self.move = self.best_move(game, 2)

        # A skončí výpočet
        return

    # Do tohoto uložte index vybraného ďolíku
    move = -1
