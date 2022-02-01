from dataclasses import dataclass
import copy


@dataclass
class Game:
    """
    The main class of the project. Contains state of a game (pits, score, ended), can return states from the view of
    a current player (player_score, opponent_score, player_pits, opponent_pits).

    play implements full rules of the game.

    copy offers the possibility of splitting game and trying next moves/guarantee that an internal state of a game is
    unchangeable by players' scripts.



    score stores pair of ints whose represent captured seeds
    pits stores an array of ints whose represent seeds in pits
    _player (can be 0 or 1) states which player plays
    _n_of_pits gives a number of pits at one side (that belongs to one player)
    _n_of_seeds gives a number of all seeds in a game
    """

    score: [int]
    pits: [int]
    ended: bool
    _player: int
    _n_of_pits: int
    _n_of_seeds: int

    @property
    def player_score(self) -> int:
        """
        :return: score of the current player
        """
        return self.score[self._player]

    @property
    def opponent_score(self) -> int:
        """
        :return: score of the opponent of the current player
        """
        return self.score[1 - self._player]

    @property
    def player_pits(self) -> [int]:
        """
        :return: an array with numbers of seeds of the current player
        """
        return self.pits[self._n_of_pits * self._player:self._n_of_pits * (1 + self._player)]

    @property
    def opponent_pits(self) -> [int]:
        """
        :return: an array with numbers of seeds of the opponent of the current player
        """
        return self.pits[self._n_of_pits * (1 - self._player):self._n_of_pits * (2 - self._player)]

    def rotate(self):
        """
        Change the player on the turn.
        """
        self._player = 1 - self._player

    def copy(self):
        """
        :return: copy of the game (full copy -- changing copy doesn't change original and reversely)
        """
        return Game(self.score.copy(), self.pits.copy(), self.ended, self._player, self._n_of_pits, self._n_of_seeds)

    def play(self, pit: int, rotate: bool = True) -> bool:
        """
        Play move by _player.

        :param pit: int from interval 0 to _n_of_pits - 1, from which pit player choose for this turn
        :param rotate: may the meaning of player and opponent be switched
        :return: true if everything is ok, false when the move is invalid (in this case restore the game state)
        """

        if type(pit) == int and self._n_of_pits > pit >= 0 and self.player_pits[pit] != 0:
            pit += self._player * self._n_of_pits  # player's move from global view

            # keep copy of state before sowing because of 0 sow on opponent's side
            pits_recovery = self.pits.copy()
            score_recovery = self.score.copy()

            # grab seeds
            hand = self.pits[pit]
            self.pits[pit] = 0

            # sow seeds
            for i in range(1, hand + 1):
                self.pits[(pit + i + (i - 1) // (2 * self._n_of_pits - 1)) % (2 * self._n_of_pits)] += 1

            # If there is no seed in the opponent's pits, it's invalid move!
            if not any(self.opponent_pits):
                self.pits = pits_recovery
                self.score = score_recovery
                return False

            # keep copy of state before gather because of full gather of opponent's side
            pits_recovery = self.pits.copy()
            score_recovery = self.score.copy()

            # gather seeds
            last_pit = (pit + hand + (hand - 1) // (2 * self._n_of_pits - 1)) % (2 * self._n_of_pits)
            while (last_pit >= 0 and last_pit // self._n_of_pits != self._player and
                   (self.pits[last_pit] == 2 or self.pits[last_pit] == 3)):
                self.score[self._player] += self.pits[last_pit]
                self.pits[last_pit] = 0

                last_pit -= 1

            # if score > 1/2 of seeds, the player wins, if the score of both = 1/2 of seeds, it's draw
            if self.score[0] > self._n_of_seeds // 2 or self.score[1] > self._n_of_seeds // 2 or \
                    (self.score[0] == self._n_of_seeds // 2 and self.score[1] == self._n_of_seeds // 2):
                self.ended = True
                if rotate:
                    self.rotate()
                return True

            # If there is no seed in the opponent's pits, do not gather!
            if not any(self.opponent_pits):
                self.pits = pits_recovery
                self.score = score_recovery
            self.rotate()

            # if a new player cannot move (opponent has 0 seeds in pits and player can't gather any on opponent's side),
            # new player get all seeds from pits
            if not any(map(lambda it: self.player_pits[it] > self._n_of_pits - it, range(self._n_of_pits))) and \
                    not any(self.opponent_pits):
                self.score[self._player] += sum(self.player_pits)
                for i in range(self._n_of_pits):
                    self.pits[self._player * self._n_of_pits + i] = 0
                self.ended = True

            # if not rotate, rotate back
            if not rotate:
                self.rotate()

            return True
        else:
            return False

    @property
    def _player0_score(self) -> int:
        """
        :return: score of the first player regardless of _player
        """
        return self.score[0]

    @property
    def _player1_score(self) -> int:
        """
        :return: score of the second player regardless of _player
        """
        return self.score[1]

    @property
    def _player0_pits(self) -> [int]:
        """
        :return: pits of the first player regardless of _player
        """
        return self.pits[0:self._n_of_pits]

    @property
    def _player1_pits(self) -> [int]:
        """
        :return: pits of the second player regardless of _player
        """
        return self.pits[self._n_of_pits:2 * self._n_of_pits]


def new_game(nop: int = 6, nosip: int = 4) -> Game:
    """
        :return: new Game, set values like score, number of seeds, ...

        Separate function because Game is @dataclass and has default constructor, which is overwritten by new
        constructor.

        Optional arguments:
            :param nop: the number of pits in one row (belonging to one player), default 6.
            :param nosip: the number of seeds in one pit, default 4.
    """
    return Game(pits=[nosip] * 2 * nop, score=[0, 0], ended=False, _player=0, _n_of_pits=nop, _n_of_seeds=2*nop*nosip)


def freeze(game: Game):
    """
    Vytvoří z hry tuple s důležitými informacemi, tuple se pak dá používat např. pro indexování množiny nebo slovníku (dict).

    Na výsledku není možné volat žádné funkce z Game a nelze ho měnit. K tomu slouží thaw, které zase vrátí Game.
    :param game: Game, kterou chceme zamrazit
    :return: tuple reprezentující neměnný aktuální stav game
    """
    return tuple(((game.player_score, game.opponent_score), tuple(game.player_pits + game.opponent_pits)))


def thaw(state: tuple, ended=False, _player=0, _n_of_pits=6, _n_of_seeds=48):
    """
    Odmrazí tuple vrácené z freeze, aby se daná hra zase dala měnit a byly na ní volatelné funkce z Game.

    :param state: výstup z freeze
    :param ended:       \
    :param _player:     |  Dodatečné informace, pokud hrajeme jinou verzi oware
    :param _n_of_pits:  |
    :param _n_of_seeds: /
    :return: "kopie" hry ze které vznikl state
    """
    return Game(*map(list, state), ended, _player=_player, _n_of_pits=_n_of_pits, _n_of_seeds=_n_of_seeds)
