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
        
    def uct_select_child(self):
        selected_child_node = sorted(self.child_nodes, key = lambda c: (c.reward/c.times_visited) + sqrt(4 * log(self.times_visited)/c.times_visited))[-1]
        return selected_child_node
        
    def add_child(self, m, s, last_move = None):
        new_child = Node(move = m, parent = self, state = s, last_move = last_move)
        self.untried_moves.remove(m)
        self.child_nodes.append(new_child)
        return new_child
        
def think(state):
            
    rootnode = Node(state = state, last_move = state.get_whose_turn())
    
    rootnode.times_visited = 1.0
    
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
            
    return sorted(rootnode.child_nodes, key = lambda c: c.reward/c.times_visited)[-1].move
    