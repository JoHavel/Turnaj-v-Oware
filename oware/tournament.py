#!/usr/bin/env python3
import signal

from utils import agent_combat, import_agent
import sys


def on_signal(sig, frame):
    """ Silent quit (without throwing exception). """
    print()
    quit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, on_signal)  # Ctrl-C stops without exception
    repeat = 1
    files = sys.argv[1:]            # skip this file
    if len(files) > 0:
        try:
            repeat = int(files[0])  # 1. arg. is number -> it represents number of pairs of n_of_games between 2 agents
            files = files[1:]       # and agents are from second argument
        except ValueError:
            pass                    # first argument isn't number -> all arguments are agents

    # for informative printing
    n_of_agents = len(files)
    n_of_games = n_of_agents * (n_of_agents - 1) * repeat
    game_number = 1  # number of current game

    points = dict([(file, 0) for file in files])  # dictionary -- name_of_file -> current points


    def signum(x: int) -> int:
        """ Return sign of x. """
        return (x > 0) - (x < 0)

    # main part
    for file_a in files:
        for file_b in files:
            if file_b != file_a:
                for _ in range(repeat):
                    score = agent_combat((file_a, file_b))
                    game_points = signum(score[0] - score[1])  # Winner takes 1, looser -1 and by draw both takes 0
                    points[file_a] += game_points
                    points[file_b] -= game_points
                    print("Odehrána hra %i/%i.\nHra %s vs. %s skončila %i:%i"
                          % (game_number, n_of_games, file_a, file_b, score[0], score[1]), file=sys.stderr)
                    game_number += 1

    print()  # one line before rating
    ranking = sorted(points.items(), key=lambda it: it[1], reverse=True)
    for position in ranking:
        agent = import_agent(position[0])
        if agent is not None:
            print("%3d: %s (%s)" % (position[1], agent.name, position[0]))
        else:  # if import failed:
            print("%3d: undefined (%s)" % (position[1], position[0]))
