# 
# Nick Junius
# Based on code provided by Adam Smith in 2018 with the addition
# of the random tie breaking

import random

def think(state):
    me = state.get_whose_turn()
    
    def evaluate(move):
        return state.copy().apply_move(move).get_score(me) + random.random()
        
    return max(state.get_moves(), key = evaluate)