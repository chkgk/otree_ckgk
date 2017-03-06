from otree.api import (
	models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
	Currency as c, currency_range
)

import itertools, random

author = 'Christian König gen. Kersting'

doc = """
Active Risk Taking, new Design
"""


class Constants(BaseConstants):
	name_in_url = 'risktaking'
	players_per_group = None
	num_rounds = 1	# change to 10 later on


class Subsession(BaseSubsession):
	def before_session_starts(self):
		treatment = itertools.cycle([1, 2, 3, 4])
		for player in self.get_players():
			player.treatment = next(treatment)
			if player.treatment in [1, 2]:
				player.default = "Safe"
			else:
				player.default = "Risky"

			if player.treatment in [1, 3]:
				player.mode = "Active"
			else:
				player.mode = "Passive"

			player.lottery_outcome = random.choice(["low", "high"])


class Group(BaseGroup):
	pass


class Player(BasePlayer):
	mode = models.CharField(initial="active", choices=['Active', 'Passive'])
	default = models.CharField(initial="safe", choices=['Safe', 'Risky'])


	lottery_outcome = models.CharField(choices=["low", "high"])

	low_payoff = models.FloatField()
	high_payoff = models.FloatField()

	max_steps = models.IntegerField(initial=20)
	interval = models.IntegerField(initial=5) 

	small_step = models.IntegerField(initial=8)
	big_step = models.IntegerField(initial=12)

	skip_trial = models.CharField(choices=["nein", "ja"], initial="ja")

	def set_payoff(self):
		if self.lottery_outcome == "high":
			self.payoff = c(self.high_payoff)
		else:
			self.payoff = c(self.low_payoff)