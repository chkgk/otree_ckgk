from otree.api import (
	models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
	Currency as c, currency_range
)

import itertools

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


class Group(BaseGroup):
	pass


class Player(BasePlayer):
	mode = models.CharField(initial="active", choices=['active', 'passive'])
	default = models.CharField(initial="safe", choices=['safe', 'risky'])
	low_payoff = models.FloatField()
	high_payoff = models.FloatField()

	max_steps = models.IntegerField(initial=10)
	interval = models.IntegerField(initial=3) #s

	small_step = models.IntegerField(initial=3)
	big_step = models.IntegerField(initial=6)

	def adjust_lottery_payoffs(self):
		pass