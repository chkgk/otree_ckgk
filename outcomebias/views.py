from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants

import random


class Arrival(WaitPage):
	group_by_arrival_time = True

	title_text = "Arrival Hall"
	body_text = "For this experiment, we need groups of two. \
	Please wait for another participant to log on."

	def after_all_players_arrive(self):
		self.group.set_treatment()

class Welcome(Page):
	pass

class Instructions(Page):
	pass

class RoleAssignment(Page):
	pass

class WinningColorChoice(Page):
	form_model = models.Group
	form_fields = ['winning_color']

	def is_displayed(self):
		return self.group.treatment == 'agent' and self.player.role() == 'agent'

class RewardDecision(Page):
	form_model = models.Group
	form_fields = ['reward_good', 'reward_bad']

	def is_displayed(self):
		return self.player.role() == 'principal'

class ResultsWaitPage(WaitPage):
	template_name = 'outcomebias/MyWaitPage.html'
	title_text = "Please Wait"

	def after_all_players_arrive(self):
		self.group.set_payoffs()

class Results(Page):
	pass


page_sequence = [
	Arrival,
	Welcome,
	#Instructions,
	#RoleAssignment,
	WinningColorChoice,
	RewardDecision,
	ResultsWaitPage,
	Results
]
