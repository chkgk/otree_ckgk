from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

import random


author = 'Christian König-Kersting'

doc = """
Outcome Bias Add on. 
"""


class Constants(BaseConstants):
    name_in_url = 'outcomebias'
    players_per_group = 2
    num_rounds = 1

    lottery_high_payoff = 300
    lottery_low_payoff = 100

    agent_fix_pay = 100
    principal_fix_pay = 0
    reward_pot = 100


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    treatment = models.CharField()
    winning_color = models.CharField(choices=['yellow', 'orange'])
    lottery_outcome = models.CharField()
    reward_good = models.PositiveIntegerField(min=0, max=Constants.reward_pot)
    reward_bad = models.PositiveIntegerField(min=0, max=Constants.reward_pot)

    def set_treatment(self):
        self.treatment = 'agent' if self.id_in_subsession % 2 == 0 else 'computer'
        self.lottery_outcome = random.choice(['good', 'bad'])
        if self.treatment == 'computer':
            self.winning_color = random.choice(['yellow', 'orange'])

    def set_payoffs(self):
        lottery_pay = Constants.lottery_high_payoff if self.lottery_outcome == "good" else Constants.lottery_low_payoff
        reward = self.reward_good if self.lottery_outcome == "good" else self.reward_bad
        for player in self.get_players():
            if player.role() == "agent":
                player.payoff = Constants.agent_fix_pay + reward
            else:
                player.payoff = Constants.principal_fix_pay + (Constants.reward_pot - reward) + lottery_pay

class Player(BasePlayer):
    
    def role(self):
    	if self.id_in_group == 1:
    		return 'agent'
    	else:
    		return 'principal'
