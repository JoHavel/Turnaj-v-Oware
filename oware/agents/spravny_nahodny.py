import random


class Agent:
    name = "Alexandr Veliký"

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
