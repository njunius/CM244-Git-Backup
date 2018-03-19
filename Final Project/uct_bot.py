#
# Nick Junius
# Based on code written by Michael Gunning and Nick Junius in 2015

import random
import greedo
from math import sqrt
from math import log

ITERMAX = 1000

class Node:
    def __init__(self, move = None, parent = None, state = None, last_move = None):
        self.move = move
        self.parent = parent
        self.child_nodes = []
        self.reward = 0.0
        self.times_visited = 0.0
        self.untried_moves = state.get_moves()
        self.who = last_move
        self.state = state
        
    def uct_select_child(self):
        selected_child_node = max(self.child_nodes, key = lambda c: c.reward/c.times_visited + sqrt(2 * log(self.times_visited)/c.times_visited))
        return selected_child_node
        
    def add_child(self, m, s, last_move = None):
        new_child = Node(move = m, parent = self, state = s, last_move = last_move)
        self.untried_moves.remove(m)
        self.child_nodes.append(new_child)
        return new_child
        
def think(state):
            
    rootnode = Node(state = state, last_move = state.get_whose_turn())
    rootnode.times_visited = 0.0
    
    for iterations in range(ITERMAX):
        node = rootnode
        next_state = state.copy()
        
        # Selection
        # while node still has children to explore and all moves have been tried
        while not node.untried_moves and node.child_nodes:
            node = node.uct_select_child()
            next_state.apply_move(node.move)
            
        # Expansion
        if node.untried_moves != []:
            move = random.choice(node.untried_moves)
            turn = next_state.get_whose_turn()
            next_state.apply_move(move)            
            node = node.add_child(move, next_state, last_move = turn)
        
        # Rollout
        while not next_state.is_terminal():
            rollout_move = greedo.think(next_state)
            next_state.apply_move(rollout_move)
        
        # Backpropogation
        while node != None:
            result = next_state.get_score(node.who)
            node.times_visited += 1
            node.reward += result
            node = node.parent
    
    chosen_node = max(rootnode.child_nodes, key = lambda c: c.reward/c.times_visited)
    print('{0} tried to {1} {2} and rolled {3}. {2} rolled {4}'.format(chosen_node.who,
                                                                        chosen_node.state.move_made, 
                                                                        chosen_node.state.conversation_partner,
                                                                        chosen_node.state.my_final_roll, 
                                                                        chosen_node.state.other_final_roll))
                                                                        
    if chosen_node.state.my_final_roll >= chosen_node.state.other_final_roll:
        print('{0} thinks more highly of {1}'.format(chosen_node.state.conversation_partner, chosen_node.who))
    else:
        print('{0} thinks {1} is making a fool of themselves'.format(chosen_node.state.conversation_partner, chosen_node.who))
        
    print('{0} has {1} successful and {2} failed moves so far. {3} has {4} successful and {5} failed moves so far.\n'.format(chosen_node.who,
                                                                                                                                         chosen_node.state.get_successes(chosen_node.who),
                                                                                                                                         chosen_node.state.get_failures(chosen_node.who),
                                                                                                                                         chosen_node.state.conversation_partner,
                                                                                                                                         chosen_node.state.get_successes(chosen_node.state.conversation_partner),
                                                                                                                                         chosen_node.state.get_failures(chosen_node.state.conversation_partner)))
    return chosen_node.move
    