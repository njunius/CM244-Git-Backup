
# coding: utf-8

# In[1]:


import random
import math

encounter_skills = {'Deception':'CHA','Performance':'CHA','Persuasion':'CHA','Insight':'WIS','Manipulate':'INT',
                    'Cultural Knowledge':'INT','Animal Handling':'WIS','Intimidate':'STR','Sleight of Hand':'DEX'}
# Special skills removed.
#                     'Barter':'Special','Apologize':'Special','Bluff':'Special'}

ability_scores = ('STR','DEX','CON','INT','WIS','CHA')

def roll_stats():
    all_rolls = []
    for ability in ability_scores:
        roll1 = random.randint(1,6)
        roll2 = random.randint(1,6)
        roll3 = random.randint(1,6)
        roll4 = random.randint(1,6)
        rolls = [roll1,roll2,roll3,roll4]
        rolls.remove(min(rolls))
        score = sum(rolls)
        all_rolls.append(score)
    stats = dict(zip(ability_scores,all_rolls))
    return stats

def random_skills():
    all_skills = list(encounter_skills.keys())
    trained_skills = random.sample(all_skills,3)
    return trained_skills

base_stats = roll_stats()
base_skills = random_skills()

class Player:
    def __init__(self, name='Jo',stats=base_stats,proficiency_bonus=2, trained_skills=base_skills):
        self.name = name
        self.stats = stats
        self.trained_skills = trained_skills
        self.proficiency_bonus = proficiency_bonus
        
    def skill_bonus(self,skill):
        if encounter_skills[skill] == 'Special':
            return 'Special'
        stat_bonus = math.ceil(((self.stats[encounter_skills[skill]])-10)/2)
        if skill in self.trained_skills:
            stat_bonus = stat_bonus+self.proficiency_bonus
        return stat_bonus


