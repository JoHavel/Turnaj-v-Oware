import random


class Agent:
    name = "Traianus"

    def play(self, game) -> None:
        nase_skore = game.player_score
        skore_soupere = game.opponent_score
        nase_doliky = game.player_pits       # Proti směru hodinových ručiček
        doliky_soupere = game.opponent_pits  # -            ||              -

        # Vybere z důlků, který maximalizuje naše skore
        best = -1
        best_index = []
        for i in range(6):
            game_copy = game.copy()
            # play odehraje (na kopii) a vrátí, zda byl tah validní
            # (rotate=False zajistí, že se neprohodí strany (player vs opponent))
            if game_copy.play(i, rotate=False):
                if game_copy.player_score == best:
                    best_index.append(i)
                if game_copy.player_score > best:
                    best = game_copy.player_score
                    best_index = [i]

        self.move = random.choice(best_index)

        # A skončí výpočet
        return

    # Do tohoto uložte index vybraného ďolíku
    move = -1
