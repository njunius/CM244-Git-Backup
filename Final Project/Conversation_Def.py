import random

class Conversation(object):
    
    def __init__(self, char1, char2):
        self.agents = (char1, char2)
        self.skills = {
                        'Deception': 'deceive',
                        'Performance': 'perform for',
                        'Persuasion': 'persuade',
                        'Insight': 'make an insightful comment to',
                        'Manipulate': 'manipulate',
                        'Cultural Knowledge': '',
                        'Intimidate': 'intimidate',
                        'Sleight of Hand': 'impress'
                      }
        self.agent_1_skills = {
                                'Deception': 2,
                                'Performance': 2,
                                'Persuasion': 1,
                                'Insight': 0,
                                'Manipulate': 0,
                                'Cultural Knowledge': 1,
                                'Intimidate': 0,
                                'Sleight of Hand': -1
                              }
                         
        self.agent_2_skills = {
                                'Deception': 0,
                                'Performance': 2,
                                'Persuasion': 0,
                                'Insight': 3,
                                'Manipulate': 0,
                                'Cultural Knowledge': 2,
                                'Intimidate': -2,
                                'Sleight of Hand': 0
                              }
                         
    def make_initial_state(self):
        return(State(self))
        
class State(object):
    def __init__(self, game):
        self.game = game
        self.whose_turn = game.agents[0]
        self.my_final_roll = 0
        self.other_final_roll = 0
        self.move_made = ""
        self.conversation_partner = ""
        self.agent_1_successes = 0
        self.agent_2_successes = 0
        self.agent_1_failures = 0
        self.agent_2_failures = 0
        
        # dicts where keys are strings corresponding to skill names and values are number of times used
        self.agent_1_used_skills = {}
        self.agent_2_used_skills = {}
                                   
    def copy(self):
        res = State(self.game)
        res.whose_turn = self.whose_turn
        res.my_final_roll = self.my_final_roll
        res.other_final_roll = self.other_final_roll
        res.move_made = self.move_made
        res.conversation_partner = self.conversation_partner
        res.agent_1_successes = self.agent_1_successes
        res.agent_2_successes = self.agent_2_successes
        res.agent_1_failures = self.agent_1_failures
        res.agent_2_failures = self.agent_2_failures
        res.agent_1_used_skills = self.agent_1_used_skills.copy()
        res.agent_2_used_skills = self.agent_2_used_skills.copy()
        return res
        
    def get_whose_turn(self):
        return self.whose_turn
        
    def get_moves(self):
        if self.whose_turn == self.game.agents[0]:
            return [skill for skill in self.game.skills.keys() if skill not in self.agent_1_used_skills]
        else:
            return [skill for skill in self.game.skills.keys() if skill not in self.agent_2_used_skills]
        
    def apply_move(self, move):
        my_roll = random.randint(1, 20)
        other_roll = random.randint(1, 20)
        if self.whose_turn == self.game.agents[0]:
            self.my_final_roll = my_roll + self.game.agent_1_skills[move]
            self.other_final_roll = other_roll + self.game.agent_2_skills[move]
            self.agent_1_used_skills[move] = 1
            if self.my_final_roll >= self.other_final_roll:
                self.agent_1_successes += 1
            else:
                self.agent_1_failures += 1
        else:
            self.my_final_roll = my_roll + self.game.agent_2_skills[move]
            self.other_final_roll = other_roll + self.game.agent_1_skills[move]
            self.agent_2_used_skills[move] = 1
            if self.my_final_roll >= self.other_final_roll:
                self.agent_2_successes += 1
            else:
                self.agent_2_failures += 1
        
        self.move_made = self.game.skills[move]
        self.whose_turn = self.game.agents[(self.game.agents.index(self.whose_turn)+1) % len(self.game.agents)]
        self.conversation_partner = self.game.agents[(self.game.agents.index(self.whose_turn)+2) % len(self.game.agents)]
        
        return self
    
    def is_terminal(self):
        return self.agent_1_failures > 2 or self.agent_1_successes > 2 or self.agent_2_failures > 2 or self.agent_2_successes > 2
        
    def get_score(self, agent):
        if agent == self.game.agents[0]:
            return self.agent_1_successes - self.agent_1_failures
        else:
            return self.agent_2_successes - self.agent_2_failures