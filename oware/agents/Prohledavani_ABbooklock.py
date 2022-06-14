import random

"""
features:
Alpha-Beta prunning
Fixed advanced heuristic
Iteartive deepening
Quinescence search - Actually working now :D
Iteartive tables
Best-first search
Nega scout
GameLight
Opening and engame books
Endlock
"""


class GameLight:
    def __init__(self, score0=0, score1=0, pits0=(4,)*6, pits1=(4,)*6):
        self.score0, self.score1 = score0, score1
        self.pits0, self.pits1 = pits0, pits1
        self.ended = False
        self.endlock = False

        self.win_score = 10 ** 5

    def copy(self):
        return GameLight(self.score0, self.score1, self.pits0, self.pits1)

    def play(self, pit):
        if not 0 <= pit < 6 or self.pits0[pit] == 0:
            return False

        all_diff, rest = self.pits0[pit] // 11, self.pits0[pit] % 11
        all_pits = tuple((i != pit)*(p + all_diff + ((i-pit-1) % 12 < rest)) for i, p in enumerate(self.pits0 + self.pits1))
        if not any(all_pits[6:]):
            return False

        collected = [False]*12
        last = True
        score_diff = 0
        if rest == 0:
            rest = 11
        for i in range(rest+pit, pit, -1):
            last &= (all_pits[i % 12] in (2, 3))
            if last is False or i % 12 < 6 or self.score0 + score_diff >= 25:
                break
            collected[i % 12] = last
            score_diff += collected[i % 12] * all_pits[i % 12]

        if self.score0 + score_diff >= 25 or (self.score0 + score_diff == 24 and self.score1 == 24):
            self.score0 += score_diff
            self.ended = True
            self.rotate()
            return True

        collected_all_pits = tuple(p*(1-collected[i]) for i, p in enumerate(all_pits))
        if not any(collected_all_pits[6:]):
            self.pits0 = all_pits[:6]
            self.pits1 = all_pits[6:]
        else:
            self.score0 += score_diff
            self.pits0 = collected_all_pits[:6]
            self.pits1 = collected_all_pits[6:]

        self.rotate()
        if not any(self.pits1) and not any(map(lambda i: self.pits0[i] > 5-i, range(6))):
            self.score0 += sum(self.pits0)
            self.ended = True

        return True

    def rotate(self):
        self.score1, self.score0 = self.score0, self.score1
        self.pits1, self.pits0 = self.pits0, self.pits1

    def players_score(self):
        return self.score0 + self.score1

    def estimated_score(self):
        if self.endlock:
            if self.score0 > self.score1:
                return 190*self.win_score
            elif self.score0 < self.score1:
                return -190*self.win_score
            else:
                return 0
        if self.ended:
            if self.score0 >= 25:
                return 190*self.win_score
            elif self.score1 >= 25:
                return -190*self.win_score
            else:
                return 0
        else:
            score_diff = 3.0*(self.score0 - self.score1)
            score_advantage = 2.0*(self.score0**2 - self.score1**2)
            biggest_pit_advantage = 0.1*(max(self.pits0) - max(self.pits1))
            options_disadvantage = 0.5*(self.pits1.count(0) - self.pits0.count(0))
            taking_advantage = 1.0*(  # Don't look
                + sum(map(lambda x: ((self.pits1[(x[0]+x[1]-6) % 12] in (1, 2)) * (self.pits1[(x[0]+x[1]-6) % 12] + 1)) if (x[0]+x[1]) % 12 >= 6 else -1, enumerate(self.pits0)))
                - sum(map(lambda x: ((self.pits0[(x[0]+x[1]-6) % 12] in (1, 2)) * (self.pits0[(x[0]+x[1]-6) % 12] + 1)) if (x[0]+x[1]) % 12 >= 6 else -1, enumerate(self.pits1)))
            )
            return score_diff + score_advantage + biggest_pit_advantage + options_disadvantage + taking_advantage

    def to_index(self):
        return tuple((self.score0, self.score1) + self.pits0 + self.pits1)


def make(game):
    return GameLight(game.player_score, game.opponent_score, tuple(game.player_pits), tuple(game.opponent_pits))


def cache(f):
    def g(self, game, depth, nocache=False, *args, **kwargs):
        i = game.to_index()
        if game.endlock:
            return f(self, game, depth, nocache=nocache, *args, **kwargs)

        s = squeeze(i)
        if s in self.endgames:
            return (self.endgames[s][0] * self.win_score, self.endgames[s][1])
        if i in self.tables and self.tables[i][0] >= depth:
            return self.tables[i][1]
        elif nocache:
            return f(self, game, depth, nocache=nocache, *args, **kwargs)
        else:
            self.tables[i] = (depth, f(self, game, depth, nocache=nocache, *args, **kwargs))
            return self.tables[i][1]
    return g


def squeeze(position):
    return "".join([chr(position[i]+35) for i in range(14)])


class Agent:
    name = "Daniel"
    win_score = 10 ** 5

    def __init__(self):
        super().__init__()
        self.min_depth = 4
        self.moves_left = 181
        self.greatest_depth = self.min_depth
        self.tables = {}
        import agents.knihovna  # Dovolil jsem si dát data do separátního souboru
        self.openings = agents.knihovna.openings
        self.endgames = agents.knihovna.endgames

    def play(self, game) -> None:
        self.move = -2

        game = make(game)
        game_index = game.to_index()
        squeezed_index = squeeze(game_index)
        if squeezed_index == "##''''''''''''":
            self.moves_left += 1
        self.moves_left -= 2

        if squeezed_index in self.openings:
            # print("open", squeezed_index)
            self.move, self.greatest_depth = self.openings[squeezed_index]
            self.greatest_depth += 1
        elif game_index in self.tables:
            self.greatest_depth = self.tables[game_index][0]
        else:
            self.greatest_depth = self.min_depth

        while self.greatest_depth <= self.moves_left:
            self.move = self.search(game, self.greatest_depth)[1]
            self.greatest_depth += 1

        game.endlock = True
        self.move = self.search(game, self.moves_left)[1]


    @cache
    def search(self, game, depth, nocache=False, alpha=-10**5, beta=10**5, last_capture=win_score, quiescence=False):
        if game.ended:
            return (game.estimated_score(), -1)
        elif depth == 0:
            if quiescence or last_capture > 2:
                return (game.estimated_score(), -1)
            else:
                return self.search(game, 3, nocache=nocache, alpha=alpha, beta=beta, quiescence=True)  # quiescence search

        next_states = []
        for to_play in range(6):
            game_copy = game.copy()
            if game_copy.play(to_play):
                next_states.append((to_play, game_copy, game_copy.to_index()))

        best = (-200 * self.win_score, -3)  # minus nekonečno, žádný validní tah
        score = game.players_score()

        random.shuffle(next_states)
        next_states.sort(
            key=lambda x: (x[2] not in self.tables, self.tables[x[2]][1][0] if x[2] in self.tables else x[1].estimated_score()),
            reverse=False
        )  # best-first search
        for to_play, game_copy, _ in next_states:
            if game_copy.players_score() > score:
                new_last_capture = 0
            else:
                new_last_capture = last_capture

            turn = (
                -self.search(game_copy, depth-1, nocache=nocache, alpha=-beta, beta=-alpha, last_capture=new_last_capture+1, quiescence=quiescence)[0],
                to_play
            )
            alpha = max(turn[0], alpha)
            best = max(best, turn)
            if alpha >= beta:
                break

        return best

    # Do tohoto uložte index vybraného ďolíku
    move = -2
