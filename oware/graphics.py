#!/usr/bin/env python3

import time
import tkinter as tk
from itertools import chain
from tkinter.filedialog import askopenfilename

from utils import import_agent, agent_play

from game import Game, new_game

# constants
agent_delay = 100  # ms

class Pit(tk.Canvas):
    """
    Widget showing pit with seeds in 'fancy' format.
    """

    seeds = 0  # number of seeds in the pit

    def __init__(self, master=None, size=80, seed_radius=7):
        """
        :param master: parent widget
        :param size: maximum size of pit (with margins)
        :param seed_radius: size of seed
        """
        super().__init__(master)
        self.size = size
        self.seed_radius = seed_radius
        self.master = master
        self.config(height=self.size, width=self.size)

    def draw_circle(self, x, y, r, **kwargs) -> None:
        """
        Draw circle on canvas.

        :param x: x coord of center
        :param y: y coord of center
        :param r: radius of circle
        :param kwargs: standard tkinter's canvas arguments (outline, fill, ...)
        """
        return self.create_oval(x - r, y - r, x + r, y + r, kwargs)

    def update_widget(self, color="#000000") -> None:
        self.delete("all")  # clear
        self.draw_circle(self.size / 2, self.size / 2, self.size / 2.1, fill="", outline=color)  # draw pit

        # draw seeds TODO programmatically TODO raise maximum of seeds (currently 13)
        for centerx, centery in [  # centers of seeds in nice layout
                                    (self.size / 2, self.size / 2),
                                    (self.size / 2 + 2 * self.seed_radius, self.size / 2),
                                    (self.size / 2 + self.seed_radius, self.size / 2 + self.seed_radius * 3 ** (1 / 2)),
                                    (self.size / 2 - self.seed_radius, self.size / 2 + self.seed_radius * 3 ** (1 / 2)),
                                    (self.size / 2 - 2 * self.seed_radius, self.size / 2),
                                    (self.size / 2 + self.seed_radius, self.size / 2 - self.seed_radius * 3 ** (1 / 2)),
                                    (self.size / 2 - self.seed_radius, self.size / 2 - self.seed_radius * 3 ** (1 / 2)),
                                    (self.size / 2 + 3 * self.seed_radius,
                                     self.size / 2 + self.seed_radius * 3 ** (1 / 2)),
                                    (self.size / 2, self.size / 2 + 2 * self.seed_radius * 3 ** (1 / 2)),
                                    (self.size / 2 - 3 * self.seed_radius,
                                     self.size / 2 + self.seed_radius * 3 ** (1 / 2)),
                                    (self.size / 2, self.size / 2 - 2 * self.seed_radius * 3 ** (1 / 2)),
                                    (self.size / 2 - 3 * self.seed_radius,
                                     self.size / 2 - self.seed_radius * 3 ** (1 / 2)),
                                    (self.size / 2 + 3 * self.seed_radius,
                                     self.size / 2 - self.seed_radius * 3 ** (1 / 2)),
                                ][0:self.seeds]:  # draw only self.seeds of seeds
            self.draw_circle(centerx, centery, self.seed_radius, fill="#00FF00")  # draw seed on center[xy]


class GameGraphics(tk.Frame):
    """ Main class of graphical interface of game """

    def __init__(self, game: Game, master=None):
        """
        :param game: Game with which start
        """
        super().__init__(master)
        self.master = master
        self.game = game                  # simply Game
        self.pits = []                    # widgets representing pits
        self.scores = []        # widgets representing scores
        self.create_widgets()
        self.files = ["", ""]             # files with agents for autoplay
        self.auto_players = [None, None]  # objects of agents for autoplay
        self.turn = 0                     # counter of turns for synchronizing agents

    def create_widgets(self) -> None:
        """ Create pits and score """
        # lower pits
        for i in range(self.game._n_of_pits):
            pit = Pit(self)                                             # create pit
            pit.bind("<ButtonPress-1>", lambda _, it=i: self.play(it))  # bind play function on every pit
            pit.grid(row=1, column=i + 1)                               # place pit
            self.pits.append(pit)                                       # add for updating

        # upper pits
        for i in range(self.game._n_of_pits):
            pit = Pit(self)
            pit.grid(row=0, column=self.game._n_of_pits - i)
            pit.bind("<ButtonPress-1>", lambda _, it=self.game._n_of_pits + i: self.play(it))
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

    def play(self, pit: int) -> None:
        """
        Play turn. Monitor, if move is valid (including player on turn).

        :param pit: chosen move (pits of second player has `self.game._n_of_pits` offset)
        """
        pit2 = pit - self.game._player * self.game._n_of_pits
        if self.game.play(pit2):
            self.update_widgets(True, pit)
            self.turn += 1

            self.after(agent_delay, lambda t=self.turn, p=self.game._player: self.autoplay(t, p))

    def autoplay(self, turn: int, player: int) -> None:
        """
        Play turn by agent.

        :param turn: number for check, if this was called and executed in same turn
        :param player: 0 or 1 (lower or upper)
        """
        if self.auto_players[player] is not None and turn == self.turn and not self.game.ended:
            try:
                # !can't be done with self.play, because of 2 call of game.play
                self.update_widgets(True, agent_play(self.auto_players[player], self.game, self.files[player])[1]
                                    # add offset (with last player on turn)
                                    + (1 - self.game._player) * self.game._n_of_pits)
                self.turn += 1
                self.after(agent_delay, lambda t=self.turn, p=self.game._player: self.autoplay(t, p))
            except Exception as e:
                print(e)

    def reset(self) -> None:
        """ Reset game to new_game. """
        self.game = new_game()
        self.update_widgets()  # Redraw widgets

    def add_agent(self, player: int) -> None:
        """
        Add autoplaying agent from file

        :param player: 0 or 1 (lower or upper)
        """

        self.files[player] = askopenfilename()  # get file from picker
        agent_cls = import_agent(self.files[player])
        if agent_cls is not None:  # if import succeeded
            self.auto_players[player] = agent_cls

            if self.game._player == player:  # if player is on turn, play
                self.autoplay(self.turn, player)

    def remove_agent(self, player: int) -> None:
        """
        Remove a autoplaying agent.

        :param player: 0 or 1 (lower or upper)
        """
        self.auto_players[player] = None

    @staticmethod
    def run(game: Game = None) -> None:
        """
        Entrypoint of graphic interface.

        :param game: Game with which start, None = new_game()
        """
        if game is None:
            game = new_game()

        # initialize tkinter
        root = tk.Tk()
        root.title("Oware")
        root.iconbitmap("")
        # root.geometry("600x300")

        app = GameGraphics(game, master=root)
        app.pack()

        # all items in menu
        menubar = tk.Menu(root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Nová", command=app.reset)
        menubar.add_cascade(label="Hra", menu=filemenu)
        agentmenu = tk.Menu(menubar, tearoff=0)
        agentmenu.add_command(label="Horní", command=lambda it=1: app.add_agent(it))
        agentmenu.add_command(label="Dolní", command=lambda it=0: app.add_agent(it))
        menubar.add_cascade(label="Přidej agenta", menu=agentmenu)
        agentmenu2 = tk.Menu(menubar, tearoff=0)
        agentmenu2.add_command(label="Horní", command=lambda it=1: app.remove_agent(it))
        agentmenu2.add_command(label="Dolní", command=lambda it=0: app.remove_agent(it))
        menubar.add_cascade(label="Odeber agenta", menu=agentmenu2)
        root.config(menu=menubar)

        # start! :)
        app.mainloop()


if __name__ == '__main__':
    GameGraphics.run()
