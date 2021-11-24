import sys
import time

from game import new_game, Game
import random
from utils import import_agent, KillableThread, run_agent


def agent_play(agent, game: Game, tim: int, file_name: str, verbose: bool = True) -> (bool, int):
    thread = KillableThread()
    thread.run = lambda: run_agent(agent, game, file_name)
    thread.start()
    thread.join(timeout=tim)
    if thread.is_alive():
        thread.kill()
        thread.join()

    move = agent.move
    if not game.play(move):
        if verbose:
            print("Agent %s zahrál neplatný tah %s ve stavu %s!" % (file_name, str(move), str(game)), file=sys.stderr)

        # If the agent played an invalid move, choose a random one.
        neprazdne = [i for i in range(6) if game.copy().play(i)]
        if len(neprazdne) == 0:
            print(game)
            raise Exception("Nastala chyba (v implementaci hry), která by neměla nastat. Přidejte issue na GitHub, nebo kontaktujte organizátora.")
        move = random.choice(neprazdne)
        game.play(move)
    return game.ended, move


def draw(game: Game, rotate: bool, show):
    if rotate:
        print("   ", *map(show, game.opponent_pits.__reversed__()), "   ", sep="|")
        print(show(game.opponent_score), "-" * 19, show(game.player_score), sep=" ")
        print("   ", *map(show, game.player_pits), "   ", sep="|")
    else:
        print("   ", *map(show, game._player1_pits.__reversed__()), "   ", sep="|")
        print(show(game._player1_score), "-" * 19, show(game._player0_score), sep=" ")
        print("   ", *map(show, game._player0_pits), "   ", sep="|")
    print()

def agent_combat(args, i: int, j: int, time_i, time_j) -> (int, int):
    game = new_game()
    files = [args.files[i], args.files[j]]
    players = [import_agent(files[0]), import_agent(files[1])]
    times = [time_i, time_j]

    if args.graphic:
        from oware_graphics import GameGraphics
        GameGraphics.run(args, game, files, players, times)
    else:

        # if args.verbose:
        if args.fancy:
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
        ##################

        if args.verbose:
            draw(game, args.rotate, show)
            start_time = time.time()

        for _ in range(args.moves):
            if agent_play(players[game._player], game, times[game._player], files[game._player])[0]:
                break
            if args.verbose:
                draw(game, args.rotate, show)
                wait_time = args.wait_time + time.time() - start_time
                if wait_time > 0:
                    time.sleep(wait_time)
                start_time = time.time()

    if not game.ended:
        print("Hra %s neskončila. Rozdávám zbylá semínka." % str(game), file=sys.stderr)
    else:
        if args.verbose:
            draw(game, args.rotate, show)
            if args.wait_time > 0:
                time.sleep(args.wait_time)

    return game._player0_score, game._player1_score


if __name__ == '__main__':
    print("Toto je pouze pomocný soubor pro oware.py!")
