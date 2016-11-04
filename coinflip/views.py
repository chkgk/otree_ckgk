from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class Instructions(Page):
	def vars_for_template(self):
		return {
			'timelimit': Constants.betting_timeout / 60, 
			'endowment': Constants.endowment,
			'exchangerate': Constants.eur_per_point
		}


class Betting(Page):
	timeout_seconds = Constants.betting_timeout
	form_model = models.Player
	form_fields = ['Punkte', 'Historie']

	def before_next_page(self):
		if self.timeout_happened:
			post_dictionary = self.request.POST
			self.player.Punkte = post_dictionary.get('Punkte')
			self.player.Historie = post_dictionary.get('Historie')

class Results(Page):
	pass


page_sequence = [
	Instructions,
	Betting,
	Results
]
