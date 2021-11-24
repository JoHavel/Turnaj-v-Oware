#!/usr/bin/env python3
#
# Nový a lepší turnaj / souboj agentů, který umí i vypisovat různé tabulky, hrát jeden proti všem,
# vykreslovat zápasy (textově/graficky), nebo různě měnit čas na tah.
import signal
import argparse
import sys
from random import Random

from utils import import_agent
from oware_utils import agent_combat

parser = argparse.ArgumentParser()
parser.add_argument("files", type=str, nargs="*", help="Agenti, mezi kterými se odehrají turnaj")
parser.add_argument("-n", "--number", type=int, default=1, help="Počet zápasů, které spolu odehraje uspořádaná dvojice agentů")
parser.add_argument("-M", "--moves", type=int, default=2*90, help="Počet tahů v jednom zápasu")
parser.add_argument("-s", "--silent", action="store_true", help="Bude hlásit jen nejdůležitější věci")

parser.add_argument("-G", "--ghostly", action="store_true", help="Nebude se nic hrát, jen se výsledky zápasů přečtou z build/nazev_souboru_bez slozky_1__nazev_souboru_bez_slozky_2.txt tak, jak je vrací ./oware.py --table nazev_souboru_1 nazev_souboru_2")

parser.add_argument("-H", "--half", action="store_true", help="Tunraj, kde bude hrát první vždy hráč více vlevo, počet zápasů bude tedy poloviční")
parser.add_argument("-C", "--challenger", action="store_true", help="Místo turnaje bude hrát první vyzyvatel se všemi")
parser.add_argument("--handicap", type=float, default=1, help="Faktor, kterým se vynásobí čas vyzívajícího agenta (s -C)")

parser.add_argument("-t", "--table", action="store_true", help="Místo samotného pořadí vrátí tabulku v pořadí na vstupu")
parser.add_argument("-T", "--Table", action="store_true", help="Místo samotného pořadí vrátí tabulku i se jmény v pořadí podle bodů")

parser.add_argument("-L", "--time", type=float, default=1, help="Čas (v sekundách) na tah")
parser.add_argument("--times", type=float, default=None, nargs="+", help="Časy, které se použijí na zápasy, jejich počet musí být roven -n")
parser.add_argument("--rtime", action="store_true", help="Náhodný čas na tah, jeden na celý turnaj")
parser.add_argument("--rtimes", action="store_true", help="Náhodný --times, jedno na celý turnaj")

parser.add_argument("-v", "--verbose", action="store_true", help="Zobrazí textově celý průběh všech zápsů")
parser.add_argument("-f", "--fancy", action="store_true", help="Při verbose zobrazí místo čísel tečky")

parser.add_argument("-g", "--graphic", action="store_true", help="Zobrazí textově celý průběh všech zápsů")

parser.add_argument("-r", "--rotate", action="store_true", help="Při verbose/graphic bude otáčet s hrací plochou podle toho, kdo je na tahu")
parser.add_argument("--wait_time", type=float, default=2, help="Čas (v sekundách), po který bude -g/-v zobrazovat jednu pozici")

r = Random()


def main(args: argparse.Namespace):
    # Příprava
    agents = [import_agent(file) for file in args.files]
    if None in agents:
        print("Nějakého agenta se nepodařilo načíst. Turnaj neuskutečňuji!")
        exit(1)
    names = [agent.name for agent in agents]
    n = len(names)

    score = [[0 for _ in range(n)] for _ in range(n)]
    ##########

    # if not args.silent: # Při -s nemusíme řešit počet her
    if args.challenger:
        n_of_games = 2 * (n - 1) * args.number
    else:
        n_of_games = n * (n - 1) * args.number

    if args.half:
        n_of_games = n_of_games//2
    game_number = 1  # number of current game
    #####################

    def signum(x: int) -> int:
        """ Return sign of x. """
        return (x > 0) - (x < 0)

    # Časy
    times = args.times
    if times is None:
        if args.rtimes and args.rtime:
            print("--rtimes nebo --rtime nelze kombinovat spolu. Ukončuji")
            exit(1)

        if args.rtimes:
            times = [r.random() for _ in range(args.number)]
        elif args.rtime:
            times = [r.random()] * args.number
        else:
            times = [args.time] * args.number
    else:
        if len(times) != args.number:
            print("Počet časů nesedí počtu zápasů. Ukončuji")
            exit(1)
        if args.rtimes or args.rtime:
            print("--rtimes nebo --rtime nelze kombinovat s --times. Ukončuji")
            exit(1)

    # Zápasy
    for i in range(n):
        for j in range(i + 1 if args.half else 0, n):
            if (i == j) or (args.challenger and ((i != 0) and (j != 0))):
                continue

            if args.challenger:
                if i == 0:
                    time_pairs = [(time * args.handicap, time) for time in times]
                else:
                    time_pairs = [(time, time * args.handicap) for time in times]
            else:
                time_pairs = [(time, time) for time in times]

            if args.ghostly:
                with open("build/%s__%s.txt" % (args.files[i].split("/")[-1], args.files[j].split("/")[-1])) as file:
                    score[i][j] += int(file.readline())
                    score[j][i] += int(file.readline())
                continue


            for n in range(args.number):
                sc = agent_combat(args, i, j, *time_pairs[n])
                game_points = signum(sc[0] - sc[1])  # Winner takes 1, looser -1 and by draw both takes 0
                score[i][j] += game_points + 1
                score[j][i] -= game_points - 1

                if not args.silent:
                    print("Odehrána hra %i/%i.\nHra %s vs. %s skončila %i:%i"
                          % (game_number, n_of_games, names[i], names[j], sc[0], sc[1]), file=sys.stderr)
                    game_number += 1
    ########

    # Výpis výsledků
    if args.table:
        for i in range(n):
            for j in range(n):
                if i == j:
                    print(" ", end="    ")
                else:
                    print(score[i][j], end="    ")
            print()

    elif args.Table:
        points = [sum(score[i][j] for j in range(n)) for i in range(n)]
        # https://stackoverflow.com/questions/9764298/how-to-sort-two-lists-which-reference-each-other-in-the-exact-same-way
        _, indices = zip(*sorted(zip(points, range(n)), reverse=True))

        # names = [name.split()[0] for name in names]
        maxlen = max(len(name) for name in names)
        # names_with_spaces = [" " * int((maxlen - len(name))/2) + name + " " * int((maxlen - len(name) + 1)/2) for name in names]
        names_with_spaces = [name + " " * int(maxlen - len(name)) for name in names]

        print("| " + " " * maxlen + " | " + " | ".join(names_with_spaces) + " | Umístění | Suma |")
        print("|-" + ("-" * maxlen + "-|-") * (n + 1) + "---------|------|")

        rank = 1
        for i in indices:
            print("| " + names_with_spaces[i], end=" | ")
            print(" | ".join(
                " " * int((maxlen - 1) / 2) + "X" + " " * int(maxlen / 2) if j == i else
                " " * int((maxlen - 5) / 2) + (" " if (score[i][j] < 10) else "") +
                str(score[i][j]) + ":" + str(score[j][i]) +
                (" " if (score[j][i] < 10) else "") +
                " " * int((maxlen - 4) / 2)
                for j in indices
            ), end=" | ")
            print(("    " if (rank < 10) else "") + str(rank) + ".   | " +
                  ("  " if (points[i] < 10) else (" " if (points[i] < 100) else "")) + str(points[i]), end="  |")
            print()
            rank += 1
    else:
        points = [sum(score[i][j] for j in range(n)) for i in range(n)]
        # https://stackoverflow.com/questions/9764298/how-to-sort-two-lists-which-reference-each-other-in-the-exact-same-way
        _, indices = zip(*sorted(zip(points, range(n)), reverse=True))

        for i in indices:
            print("%3d: %s (%s)" % (points[i], names[i], args.files[i]))
    #####################


def on_signal(sig, frame):
    """ Silent quit (without throwing exception). """
    print()
    quit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, on_signal)  # Ctrl-C stops without exception

    arguments = parser.parse_args()
    main(arguments)
