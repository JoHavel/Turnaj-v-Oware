#!/usr/bin/env python3

from game import *
from utils import agent_combat, agent_play, import_agent
import sys
import signal


def on_signal(sig, frame):
    """ Silent quit (without throwing exception). """
    print()
    quit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, on_signal)  # Ctrl-C stops without exception
    verbose = True

    if any(map(lambda it: it == "-s" or it == "silent", sys.argv)):
        verbose = False

    if verbose:
        rotate = False

        if any(map(lambda it: it == "-r" or it == "rotate", sys.argv)):
            rotate = True

        if any(map(lambda it: it == "-f" or it == "fancy", sys.argv)):
            symbols = [' ', '⠁', '⠉', '⠋', '⠛', '⠟', '⠿', '⡿', '⣿']

            def show(i: int):
                """ Print seeds in fancy format. """
                if i > 16:
                    return i
                else:
                    if i > 8:
                        return "⣿" + symbols[i - 8]
                    else:
                        return symbols[i] + " "
        else:
            def show(i: int):
                """ Print seeds as numbers. """
                return "%02d" % i

        game = new_game()
        agent = [None, None]
        agent_files = ["", ""]
        print("""q = quit, n = new, number i = play(i), a ... = add agent, c = cancel agent""")
        while True:
            # draw game:
            if rotate:
                print("   ", *map(show, game.opponent_pits.__reversed__()), "   ", sep="|")
                print(show(game.opponent_score), "-" * 19, show(game.player_score), sep=" ")
                print("   ", *map(show, game.player_pits), "   ", sep="|")
            else:
                print("   ", *map(show, game._player1_pits.__reversed__()), "   ", sep="|")
                print(show(game._player1_score), "-" * 19, show(game._player0_score), sep=" ")
                print("   ", *map(show, game._player0_pits), "   ", sep="|")

            # read user input
            try:
                line = input()
            except EOFError:  # Ctrl-D exits without exception
                break

            if len(line) == 0:  # autoplay
                if not game.ended and agent[game._player] is not None:
                    agent_play(agent[game._player], game, agent_files[game._player])
                continue
            if line[0] == 'q':  # quit
                break
            if line[0] == 'n':  # new game
                if game.ended:
                    game = new_game()
                else:           # do not discard game without the certainty
                    if input("Opravdu chceš novou hru? (y / n)") == "y":
                        game = new_game()

            try:                # number = move
                if not game.play(int(line)):
                    print("To nebyl validní tah!", file=sys.stderr)
            except ValueError:
                pass

            if line[0] == 'a':  # add agent
                agent_files[game._player] = line[1:].strip()  # get agent file
                agent_cls = import_agent(agent_files[game._player])
                if agent_cls is not None:  # if import succeeded
                    agent[game._player] = agent_cls()

                    if not game.ended:  # do not play automatically ended game
                        agent_play(agent[game._player], game, agent_files[game._player])

            if line[0] == 'c':  # cancel
                agent[game._player] = None
    else:
        inp = list(filter(lambda x: x[0] != '-', sys.argv[1:]))  # filter out all options
        if len(inp) != 2:
            raise Exception("-s lze použít pouze se 2 agenty")
        score = agent_combat(inp)
        if score[0] > score[1]:
            print("Vyhrál", inp[0], "%i:%i" % score)
        if score[0] < score[1]:
            print("Vyhrál", inp[1], "%i:%i" % score[::-1])
        if score[0] == score[1]:
            print("Remíza", "%i:%i" % score)
