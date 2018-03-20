import random
import copy
class Conversation(object):
    
    def __init__(self, char1, char2):
        self.agents = (char1, char2)
        self.skills = {
                        'Deception': 'deceive',
                        'Performance': 'perform for',
                        'Persuasion': 'persuade',
                        'Insight': 'make an insightful comment to',
                        'Manipulate': 'manipulate',
                        'Cultural Knowledge': 'talk about history with',
                        'Intimidate': 'intimidate',
                        'Sleight of Hand': 'impress',
                        'Apologize': 'apologizes to'
                      }
                      
        self.agent_skills = [
                                {
                                    'Deception': 2,
                                    'Performance': 2,
                                    'Persuasion': 1,
                                    'Insight': 0,
                                    'Manipulate': 0,
                                    'Cultural Knowledge': 1,
                                    'Intimidate': 0,
                                    'Sleight of Hand': -1
                                },
                                
                                {
                                    'Deception': 0,
                                    'Performance': 2,
                                    'Persuasion': 0,
                                    'Insight': 3,
                                    'Manipulate': 0,
                                    'Cultural Knowledge': 2,
                                    'Intimidate': -2,
                                    'Sleight of Hand': 0
                                }
                                
                            ]
                            
    def make_initial_state(self):
        return(State(self))
        
class State(object):
    def __init__(self, game):
        self.game = game
        self.whose_turn = 0
        
        self.action_log = [] # tuple of (who, skill, successes, failures)
        
    def copy(self):
        res = State(self.game)
        res.whose_turn = self.whose_turn
        res.action_log = self.action_log.copy()
        return res
        
    def get_whose_turn(self):
        return self.game.agents[self.whose_turn]
           
    def get_moves(self):
        moves = list(self.game.skills.keys()).copy()
        for skill in self.game.skills.keys():
            for entry in self.action_log:
                if entry[0] == self.whose_turn and entry[1] in moves:
                    moves.remove(entry[1])
                
        return moves
        
    def apply_move(self, move):
        num_successes = 0
        num_failures = 0
        if len(self.action_log) > 1:
            num_successes = self.action_log[-1][2]
            num_failures = self.action_log[-1][3]

        if move == 'Apologize':
            available_moves = self.get_moves()
            for skill in available_moves:
                if skill != 'Apologize':
                    num_failures -= 1
                    apology_action = (self.whose_turn, move, num_successes, num_failures)
                    self.action_log.append(apology_action)
                    used_skill = (self.whose_turn, skill, num_successes, num_failures)
                    self.action_log.append(used_skill)
        
        else:
            my_final_roll = self.game.agent_skills[self.whose_turn][move]
            other_final_roll = self.game.agent_skills[1-self.whose_turn][move]
            if my_final_roll >= other_final_roll:
                num_successes += 1
            else:
                num_failures += 1
            next_action = (self.whose_turn, move, num_successes, num_failures)
            self.action_log.append(next_action)
        
        self.whose_turn = 1 - self.whose_turn
        
        print(self.action_log)
        return self
    
    def is_terminal(self):
        num_actions = len(self.action_log)
        if len(self.action_log) < 2:
            return False
        for who, skill, successes, failures in self.action_log:
            if successes > 2 or failures > 2:
                return True
        return False
        
    def get_score(self, agent):
        for who, skill, successes, failures in reversed(self.action_log):
            if self.game.agents[self.whose_turn] == agent:
                return successes - failures
        return 0