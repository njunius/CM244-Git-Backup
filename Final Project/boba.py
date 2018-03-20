#
# Nick Junius
# Based on code written by Micahel Gunning and Nick Junius in 2015 as well as 
# a rollout algorithm partially made in a classroom in 2018

import greedo
import random

ROLLOUTS = 1

def think(state):

    moves = state.get_moves()
    
    best_move = greedo.think(state)
    best_expectation = float("-inf")
    
    me = state.get_whose_turn()
    
    def rollout(state):
        while not state.is_terminal():
            rollout_move = greedo.think(state)
            state.apply_move(rollout_move)
        return state.get_score(me)
            
    for move in moves:
        total_score = 0.0
        
        for r in range(ROLLOUTS):
            rollout_state = state.copy()
            
            rollout_state.apply_move(move)
            
            total_score += sum([rollout(rollout_state) for i in range(ROLLOUTS)])
            
        expectation = float(total_score) / ROLLOUTS
        
        if expectation > best_expectation:
            best_expectation = expectation
            best_move = move
            
    print("{} rollsout with move {} with expected score {}".format(me, best_move, best_expectation))
    return best_move