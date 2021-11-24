import time
import tkinter as tk
from itertools import chain

from graphics import Pit
from oware_utils import agent_play


class GameGraphics(tk.Frame):
    """ Main class of graphical interface of game """

    def __init__(self, args, game, files, players, times, master=None):
        super().__init__(master)
        self.master = master
        self.game = game                  # simply Game
        self.pits = []                    # widgets representing pits
        self.scores = []        # widgets representing scores
        self.create_widgets()
        self.files = files             # files with agents for autoplay
        self.auto_players = players  # objects of agents for autoplay
        self.args = args
        self.times = times

    def create_widgets(self) -> None:
        """ Create pits and score """
        # lower pits
        for i in range(self.game._n_of_pits):
            pit = Pit(self)                                             # create pit
            pit.grid(row=1, column=i + 1)                               # place pit
            self.pits.append(pit)                                       # add for updating

        # upper pits
        for i in range(self.game._n_of_pits):
            pit = Pit(self)
            pit.grid(row=0, column=self.game._n_of_pits - i)
            self.pits.append(pit)

        # scores
        self.scores = [tk.Label(self, width=10), tk.Label(self, width=10)]
        # more suitable placement, near to pits of the players
        self.scores[0].grid(row=1, column=0)
        self.scores[1].grid(row=0, column=self.game._n_of_pits + 1)
        # placement in middle
        # self.score[0].grid(row=0, column=0, rowspan=2)
        # self.score[1].grid(row=0, column=self.game.nop + 1, rowspan=2)

        # draw widgets
        self.update_widgets()

    def update_widgets(self, fancy=False, start=0) -> None:
        """
        :param fancy: drawing with delay for visible change
        :param start: start from with which pit (this pit will be green)
        """

        game_state = self.game

        self.scores[0]["text"] = str(game_state._player0_score)
        self.scores[1]["text"] = str(game_state._player1_score)

        # player on the turn has red score
        self.scores[self.game._player].config(fg="#FF0000")
        self.scores[1 - self.game._player].config(fg="#000000")

        for i in chain(range(start, 2 * self.game._n_of_pits), range(0, start)):  # every pit starting with `start`
            self.pits[i].seeds = game_state.pits[i]  # change number of seeds in pit
            if fancy:
                time.sleep(0.05)
                self.update()  # if we are delaying, we must update widgets by ourself

            if i // self.game._n_of_pits == self.game._player:
                self.pits[i].update_widget("#FF0000")  # the player on the turn has red pits
            elif i == start:
                self.pits[i].update_widget("#00FF00")  # the starting pit is green
            else:
                self.pits[i].update_widget()           # other pits are black

    def autoplay(self, player: int) -> None:
        if self.game.ended:
            self.master.destroy()
            return

        try:
            start_time = time.time()
            self.update_widgets(True, agent_play(self.auto_players[player], self.game, self.times[player], self.files[player])[1]
                                # add offset (with last player on turn)
                                + (1 - self.game._player) * self.game._n_of_pits)
            wait_time = self.args.wait_time + time.time() - start_time
            if wait_time < 0:
                wait_time = 0
            self.after(int(wait_time * 1000), lambda p=self.game._player: self.autoplay(p))
        except Exception as e:
            print(e)

    @staticmethod
    def run(args, game, files, players, times) -> None:

        # initialize tkinter
        root = tk.Tk()
        root.title("Oware")
        root.iconbitmap("")
        # root.geometry("600x300")

        app = GameGraphics(args, game, files, players, times, master=root)
        app.pack()

        # start! :)
        app.after(int(args.wait_time*1000), lambda p=0: app.autoplay(p))
        app.mainloop()


if __name__ == '__main__':
    print("Toto je pouze pomocný soubor pro oware.py!")
