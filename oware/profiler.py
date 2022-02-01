import cProfile

from game import *
from agents.prohledavani import Agent

Alexandr = Agent()

game = new_game()

target_depth = 6

for depth in range(target_depth):
    Alexandr.search(game, depth)

cProfile.run('Alexandr.search(game,target_depth)')
