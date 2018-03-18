from game import Simulator

# Reutrn value is a dictionary where each key is a map position and the values are
# lists of paths that reach that position with different ability sets.
def analyze(design):
    # Called every time the design is edited
    # Returns results that can be inspected
    
    sim = Simulator(design)
    init = sim.get_initial_state()
    moves = sim.get_moves()
    
    queue = [init]
    
    # dict where keys are states and values are states
    prev = {}
    prev[init] = None
    
    while queue:
        # state are a tuple of pos, abilities 
        current_state = queue.pop(0)
        for move in moves:
            next_state = sim.get_next_state(current_state, move)
            if next_state != None and next_state not in prev:
                queue.append(next_state)
                prev[next_state] = current_state        
    
    return prev
    
def inspect(results, pos, draw_line):
    current_state = None
    for state in results:
        current_state = state
        current_coordinates, current_abilities = state
        
        if current_coordinates == pos:
            prev_state = results[current_state]
            #prev_coordinates, prev_abilities = results[current_state]
            
            while prev_state != None:
                prev_coordinates, prev_abilities = prev_state
                draw_line(current_coordinates, prev_coordinates, state, prev_abilities)
                current_state = prev_state
                current_coordinates, current_abilities = current_state
                prev_state = results[current_state]
                