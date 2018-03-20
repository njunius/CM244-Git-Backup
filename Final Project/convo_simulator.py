from Conversation_Def import Conversation
from collections import defaultdict
from NPCs import roll_stats, random_skills, Player

import sys
import time
import importlib

assert len(sys.argv) is 3
_, red_module, blue_module = sys.argv


bots = {
  'Morgan': importlib.import_module(red_module),
  'Jules': importlib.import_module(blue_module),
}

morgan_stats = roll_stats()
morgan_skills = random_skills()
morgan = Player('Morgan', morgan_stats, 2, morgan_skills)

print('Morgan:')
print(morgan_stats)
print(morgan_skills)

jules_stats = roll_stats()
jules_skills = random_skills()
jules = Player('Jules', jules_stats, 2, jules_skills)

print('\nJules:')
print(jules_stats)
print(jules_skills)

rounds = 1
wins = defaultdict(int)

game = Conversation(morgan, jules)

for i in range(rounds):

  print("")
  print("Conversation %d" % i)

  state = game.make_initial_state()
  
  while not state.is_terminal():
    tick = time.time()
    move = bots[state.get_whose_turn()].think(state.copy())
    tock = time.time()
    print(state.get_whose_turn(), "thought for", tock-tick, "seconds")
    state.apply_move(move)

  print('')
  print(state.action_log)
  prev_entry = state.action_log[0]
  for entry in state.action_log:
    print('\n{} tries to {} {}'.format(state.game.agents[entry[0]].name, state.game.skills[entry[1]], state.game.agents[1 - entry[0]].name))
    
    if state.action_log.index(entry) > 1:
        prev_entry = state.action_log[state.action_log.index(entry) - 2]
        
    if entry[1] == 'Apologize' or entry[1] == 'Barter':
        print('{} accepts'.format(state.game.agents[1 - entry[0]].name))
    elif entry[1] == 'Bluff':
        print('{} acquiesces'.format(state.game.agents[1 - entry[0]].name))
    elif (entry[2] > 0 and prev_entry == entry) or entry[2] > prev_entry[2]:
        print('{} thinks more highly of {}'.format(state.game.agents[1 - entry[0]].name, state.game.agents[entry[0]].name))
    else:
        print('{} thinks {} is making a fool of themselves'.format(state.game.agents[1 - entry[0]].name, state.game.agents[entry[0]].name))
    prev_entry = entry
  
  print('\n{} got what they wanted'.format(state.game.agents[prev_entry[0]].name))


print("")

