from Conversation_Def import Conversation
from collections import defaultdict

import sys
import time
import importlib

assert len(sys.argv) is 3
_, red_module, blue_module = sys.argv


bots = {
  'Olivia': importlib.import_module(red_module),
  'Viola': importlib.import_module(blue_module),
}

rounds = 10
wins = defaultdict(int)

game = Conversation(sorted(bots.keys())[1], sorted(bots.keys())[0])

for i in range(rounds):

  print("")
  print("Conversation %d" % i)

  state = game.make_initial_state()
  
  while not state.is_terminal():
    tick = time.time()
    move = bots[state.whose_turn].think(state.copy())
    tock = time.time()
    print(state.whose_turn, "thought for", tock-tick, "seconds")
    state.apply_move(move)

  winner = max(game.agents,key=state.get_score)
  print("%s wins this round!" % winner)
  wins[winner] = 1 + wins[winner]

print("")
print("Final win counts:", dict(wins))
