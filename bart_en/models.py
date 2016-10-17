# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division

import random
import itertools

import otree.models
from otree.db import models
from otree import widgets
from otree.common import Currency as c, currency_range, safe_json
from otree.constants import BaseConstants
from otree.models import BaseSubsession, BaseGroup, BasePlayer
# </standard imports>

author = 'Christian König-Kersting'

doc = """
Balloon Analogue Risk Task implementation
"""


class Constants(BaseConstants):
	name_in_url = 'bart_en'
	players_per_group = None
	num_rounds = 1


class Subsession(BaseSubsession):
	def before_session_starts(self):
		treatments = itertools.cycle(["manual", "automatic"])
		for p in self.get_players():
			p.treatment = next(treatments)

class Group(BaseGroup):
	pass


class Player(BasePlayer):
	treatment = models.CharField()
	task_order = models.CharField()

	# Eckel and Grossman risk elicitation task
	lottery_choice = models.PositiveSmallIntegerField()
	lottery_outcome = models.CharField()
	lottery_payoff = models.PositiveIntegerField()

	# bart blue (128 max pushes)
	bart_blue_raw_data = models.CharField(max_length=500000) # needs to be changed to hidden input later
	bart_blue_sum_collected = models.CharField(max_length=100) # needs to be hidde later
	bart_blue_avg_time = models.CharField()
	bart_blue_num_intact = models.PositiveSmallIntegerField()
	bart_blue_avg_pumps_intact = models.FloatField()

	# # bart green (64 max pushes)
	# bart_green_raw_data = models.CharField(max_length=500000) # needs to be changed to hidden input later
	# bart_green_sum_collected = models.CharField(max_length=100) # needs to be hidde later
	# bart_green_avg_time = models.CharField()
	# bart_green_num_intact = models.PositiveSmallIntegerField()
	# bart_green_avg_pumps_intact = models.FloatField()


	# active / passive risk taking behavior questions
	active_risk_1 = models.PositiveIntegerField()
	active_risk_2 = models.PositiveIntegerField()
	active_risk_3 = models.PositiveIntegerField()
	active_risk_4 = models.PositiveIntegerField()
	active_risk_5 = models.PositiveIntegerField()
	active_risk_6 = models.PositiveIntegerField()
	active_risk_7 = models.PositiveIntegerField()
	active_risk_8 = models.PositiveIntegerField()
	active_risk_9 = models.PositiveIntegerField()
	active_risk_10 = models.PositiveIntegerField()
	active_risk_11 = models.PositiveIntegerField()
	active_risk_12 = models.PositiveIntegerField()

	passive_risk_1 = models.PositiveIntegerField()
	passive_risk_2 = models.PositiveIntegerField()
	passive_risk_3 = models.PositiveIntegerField()
	passive_risk_4 = models.PositiveIntegerField()
	passive_risk_5 = models.PositiveIntegerField()
	passive_risk_6 = models.PositiveIntegerField()
	passive_risk_7 = models.PositiveIntegerField()
	passive_risk_8 = models.PositiveIntegerField()
	passive_risk_9 = models.PositiveIntegerField()
	passive_risk_10 = models.PositiveIntegerField()
	passive_risk_11 = models.PositiveIntegerField()
	passive_risk_12 = models.PositiveIntegerField()


	# demographics
	payment_task = models.CharField()
	age = models.PositiveSmallIntegerField(min=0, max=99)
	female = models.PositiveSmallIntegerField(choices=[(0, 'male'), (1, 'female')])
	studies = models.CharField(blank=True)
	nationality = models.CharField()

	lotteries = {
		1: {
			'win': 3200,
			'lose': 3200,
		},
		2: {
			'win': 4000,
			'lose': 2800,
		},
		3: {
			'win': 4800,
			'lose': 2400,
		},
		4: {
			'win': 5600,
			'lose': 2000,
		},
		5: {
			'win': 6400,
			'lose': 1600,
		},
		6: {
			'win': 7200,
			'lose': 1200,
		},
		7: {
			'win': 8000,
			'lose': 800,
		},
		8: {
			'win': 8800,
			'lose': 400,
		},
		9: {
			'win': 9600,
			'lose': 0
		}
	}

	def play_Lottery(self):
		winning_probability = 0.5
		self.lottery_outcome = "win" if random.random() < winning_probability else "lose"
		self.lottery_payoff = self.lotteries[self.lottery_choice][self.lottery_outcome]


	def set_payoffs(self):
		self.payment_task = random.choice(["Part 2", "Part 1"])
		if self.payment_task == "Part 2":
			self.payoff = c(self.bart_blue_sum_collected)
		else:
			self.payoff = c(self.lottery_payoff)