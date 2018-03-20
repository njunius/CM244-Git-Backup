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
                        'Animal Handling':'talks about their fondness for raising animals with',
                        'Intimidate': 'intimidate',
                        'Sleight of Hand': 'impress',
                        'Apologize': 'apologize to',
                        'Bluff': 'take over the conversation from',
                        'Barter': 'promise a favor to'
                      }
        
        self.encounter_skills = ['Deception', 'Performance', 'Persuasion', 'Insight', 'Manipulate', 'Cultural Knowledge', 'Animal Handling', 'Intimidate', 'Sleight of Hand']
        
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
        
        self.action_log = [] # tuple of (who, skill, successes, failures, apoligized_skill, bluffed_skill, bartered_skill, bluff_modifier, barter_modifier)
        
    def copy(self):
        res = State(self.game)
        res.whose_turn = self.whose_turn
        res.action_log = self.action_log.copy()
        return res
        
    def get_whose_turn(self):
        return self.game.agents[self.whose_turn].name
           
    def get_moves(self):
        moves = list(self.game.skills.keys()).copy()
        for skill in self.game.skills.keys():
            for entry in self.action_log:
                if entry[0] == self.whose_turn and entry[1] in moves:
                    moves.remove(entry[1])
                elif entry[0] == self.whose_turn and entry[4] in moves:
                    moves.remove(entry[4])
                elif entry[0] == self.whose_turn and entry[5] in moves:
                    moves.remove(entry[5])
                elif entry[0] == self.whose_turn and entry[6] in moves:
                    moves.remove(entry[6])
        
        return moves
        
    def apply_move(self, move):
        num_successes = 0
        num_failures = 0
        bluff_mod = 0
        barter_mod = 0
        apoligized_skill = ''
        bluffed_skill = ''
        bartered_skill = ''
        available_moves = self.get_moves()

        if len(self.action_log) > 1:
            num_successes = self.action_log[-2][2]
            num_failures = self.action_log[-2][3]
            bluff_mod = self.action_log[-2][7]
            barter_mod = self.action_log[-2][8]
            apoligized_skill = self.action_log[-2][4]
            bluffed_skill = self.action_log[-2][5]
            bartered_skill = self.action_log[-2][6]

        if (move == 'Apologize' or move == 'Bluff' or move == 'Barter') and len(available_moves) > 0:
            worst_option = available_moves[0]
            for skill in available_moves:
                if skill in self.game.encounter_skills:
                    if self.game.agents[self.whose_turn].skill_bonus(skill) < self.game.agents[self.whose_turn].skill_bonus(worst_option):
                        worst_option = skill
            if move == 'Apologize':
                num_failures -= 1
                apoligized_skill = worst_option
            elif move == 'Bluff':
                bluff_mod = 2
                bluffed_skill = worst_option
            else:
                barter_mod = 2
                bartered_skill = worst_option
            next_action = (self.whose_turn, move, num_successes, num_failures, apoligized_skill, bluffed_skill, bartered_skill, bluff_mod, barter_mod)
            self.action_log.append(next_action)
            
        
        else:
            my_final_roll = self.game.agents[self.whose_turn].skill_bonus(move) + bluff_mod + barter_mod
            other_final_roll = self.game.agents[1 - self.whose_turn].skill_bonus(move)
            
            if my_final_roll >= other_final_roll:
                num_successes += 1
            else:
                num_failures += 1
            next_action = (self.whose_turn, move, num_successes, num_failures, apoligized_skill, bluffed_skill, bartered_skill, bluff_mod, barter_mod)
            self.action_log.append(next_action)
        
        self.whose_turn = 1 - self.whose_turn
        
        #print(self.action_log)
        return self
    
    def is_terminal(self):
        num_actions = len(self.action_log)
        if len(self.action_log) < 2:
            return False
        for who, skill, successes, failures, apology, bluffed, bartered, bluff_mod, barter_mod in self.action_log:
            if successes > 2 or failures > 2:
                return True
        return False
        
    def get_score(self, agent):
        for who, skill, successes, failures, apology, bluffed, bartered, bluff_mod, barter_mod in reversed(self.action_log):
            if self.game.agents[self.whose_turn].name == agent:
                return successes - failures
        return 0