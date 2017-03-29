from otree.api import (
	models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
	Currency as c, currency_range
)
import itertools, random

author = 'Christian König-Kersting'

doc = """
Instructions for risktaking experiment
"""


class Constants(BaseConstants):
	name_in_url = 'risktaking_instructions'
	players_per_group = None
	num_rounds = 1


class Subsession(BaseSubsession):
	def before_session_starts(self):
		treatment = itertools.cycle([1, 2, 3, 4])
		for player in self.get_players():
			current_treatment = next(treatment)
			if current_treatment in [1, 2]:
				player.participant.vars['default'] = "Safe"
			else:
				player.participant.vars['default']  = "Risky"

			if current_treatment in [1, 3]:
				player.participant.vars['mode']  = "Active"
			else:
				player.participant.vars['mode']  = "Passive"

			player.participant.vars['relevant_round'] = random.randint(1, self.session.config['main_task_rounds'])

		self.session.vars['small_step'] = 8
		self.session.vars['big_step'] = 12
		self.session.vars['interval'] = 5
		self.session.vars['max_steps'] = 10

		self.session.vars['steps'] = [
			{'small_step': 8, 'big_step': 12}, # 0
			{'small_step': 4, 'big_step': 6}, # 1
			{'small_step': 2, 'big_step': 3}, # 2
			{'small_step': 12, 'big_step': 18}, # 3
			{'small_step': 16, 'big_step': 24}, # 4
			{'small_step': 32, 'big_step': 64}, # 5
			{'small_step': 10, 'big_step': 15}, # 6
			{'small_step': 18, 'big_step': 27}, # 7
			{'small_step': 5, 'big_step': 7.5}, # 8 
			{'small_step': 15, 'big_step': 22.5}, # 9
		]


class Group(BaseGroup):
	pass


class Player(BasePlayer):
	pass