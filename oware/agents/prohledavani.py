import random

from game import freeze

class Agent:
    name = "Alexandr Obsáhlý"

    save = set()

    def search(self, game, depth):
        if depth == 0:
            if freeze(game) in self.save:
                print(game)
            return
        self.save.add(freeze(game))
        for i in range(6):
            game_copy = game.copy()
            if game_copy.play(i):
                self.search(game_copy, depth - 1)








    # Zbytek je jako ve spravny_nahodny.py

    def play(self, game) -> None:
        nase_skore = game.player_score
        skore_soupere = game.opponent_score
        nase_doliky = game.player_pits       # Proti směru hodinových ručiček
        doliky_soupere = game.opponent_pits  # -            ||              -

        # Vybere náhodný ďolík ze kterého opravdu může hrát
        neprazdne = [i for i in range(6) if game.copy().play(i)]
        self.move = random.choice(neprazdne)

        # A skončí výpočet
        return

    # Do tohoto uložte index vybraného ďolíku
    move = -1
