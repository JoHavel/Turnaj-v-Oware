import ctypes
import threading
from importlib.util import module_from_spec, spec_from_file_location
import sys
from game import new_game, Game
import random

# Constants
n_of_moves: int = 2*90
agent_time_limit: float = 1.0  # seconds


# https://stackoverflow.com/a/325528
class KillableThread(threading.Thread):
    """A thread that can be killed from another thread with kill."""
    def kill(self) -> None:
        """Stop the thread (by throwing EndingException in it)."""

        # Search for id of thread.
        thread_id = 0
        for tid, tobj in threading._active.items():
            if tobj is self:
                thread_id = tid
        # Throw exception
        ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(thread_id),
                                                   ctypes.py_object(EndingException))


class EndingException(BaseException):
    """Exception for KillableThread"""
    pass


def import_agent(file_path: str):
    """
    Import Agent from file.

    :param file_path: path to file from which import
    :return: object of imported class
    """
    try:
        file_name = file_path.split("/")[-1].split(".")[0]
        spec = spec_from_file_location(file_name, file_path)
        module = module_from_spec(spec)
        spec.loader.exec_module(module)
        agent = module.Agent
        if not hasattr(agent, "play"):
            print("Agent %s neobsahuje play!" % file_path, file=sys.stderr)
            return None
        if not hasattr(agent, "name"):
            print("Agent %s neobsahuje name!" % file_path, file=sys.stderr)
        if not hasattr(agent, "move"):
            print("Agent %s neobsahuje move!" % file_path, file=sys.stderr)
            return None
        if hasattr(agent, "init"):
            ag = agent()

            def init():
                try:
                    ag.init()
                except EndingException:
                    pass
            thread = KillableThread()
            thread.run = init
            thread.start()
            thread.join(timeout=agent_time_limit)
            if thread.is_alive():
                thread.kill()
                thread.join()
            return ag
        return agent()
    except FileNotFoundError:
        print("Soubor %s pravděpodobně nenalezen!" % file_path, file=sys.stderr)
        return None
    except AttributeError:
        print("Soubor %s neobsahuje třídu Agent!" % file_path, file=sys.stderr)
        return None


def run_agent(agent, game, file_name) -> None:
    """
    Function for thread. It lets player move.

    :param agent: a object created from Agent imported from user script
    :param game: a game, in which agent take turn (by active player)
    :param file_name: string identifying the agent in informative prints
    """
    try:
        agent.play(game.copy())
    except EndingException:
        pass  # EndingException is thrown from thread, it must be passed thought
    except BaseException as e:
        print("Agent %s vyhodil chybu:" % file_name, file=sys.stderr)
        print(e, file=sys.stderr)


def agent_combat(files: (str, str), verbose: bool = True) -> (int, int):
    """
    Import a pair of player and play a game between them.

    :param files: path to files from whose import agents
    :param verbose: if print informative prints (agent played invalid move...)
    :return: ending score of game (first_player, second_players)
    """
    game = new_game()
    players = [import_agent(files[0]), import_agent(files[1])]

    # If there was an import error, return (0, 0) (draw without points). TODO?
    if players[0] is None or players[1] is None:
        return 0, 0

    for i in range(n_of_moves):
        if agent_play(players[game._player], game, files[game._player], verbose=verbose)[0]:
            break

    if not game.ended:
        print("Hra %s neskončila. Rozdávám zbylá semínka." % str(game), file=sys.stderr)
        # (For visual control, that number of moves is sufficient.)

    return game._player0_score, game._player1_score


def agent_play(agent, game: Game, file_name: str = "unspecified", verbose: bool = True) -> (bool, int):
    """
    Let the agent play a move.

    :param agent: a object created from Agent imported from user script
    :param game: a game, in which agent take turn (by active player)
    :param file_name: string identifying the agent in informative prints
    :param verbose: if print informative prints (agent played invalid move...)
    :return: pair (if game ended, what move agent (or random chooser, when agent's turn was invalid) played)
    """
    thread = KillableThread()
    thread.run = lambda: run_agent(agent, game, file_name)
    thread.start()
    thread.join(timeout=agent_time_limit)
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
