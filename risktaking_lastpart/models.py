from otree.api import (
	models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
	Currency as c, currency_range
)

import itertools, random


author = 'Christan König-Kersting'

doc = """
Questionnaires for active / passive risk taking experiment
"""


class Constants(BaseConstants):
	name_in_url = 'ristaking_lastpart'
	players_per_group = None
	num_rounds = 1

	lotteries = {
		1: {
			'win': 600,
			'lose': 600,
		},
		2: {
			'win': 690,
			'lose': 540,
		},
		3: {
			'win': 780,
			'lose': 480,
		},
		4: {
			'win': 870,
			'lose': 420,
		},
		5: {
			'win': 960,
			'lose': 360,
		},
		6: {
			'win': 1050,
			'lose': 300,
		},
		7: {
			'win': 1140,
			'lose': 240,
		},
		8: {
			'win': 1230,
			'lose': 180,
		},
		9: {
			'win': 1320,
			'lose': 120,
		},
		10: {
			'win': 1410,
			'lose': 90,
		},
		11: {
			'win': 1500,
			'lose': 0
		}
	}


class Subsession(BaseSubsession):
	pass

class Group(BaseGroup):
	pass


class Player(BasePlayer):
	age = models.PositiveIntegerField(min=0, max=110, doc="age in years")
	gender = models.CharField(choices=['männlich', 'weiblich', 'anderes', 'keine Angabe'], widget=widgets.RadioSelectHorizontal, doc="gender")
	studies = models.CharField(doc="field of studies")	

	native_german = models.BooleanField(choices=[(True, 'Ja'), (False, 'Nein')], doc="is German native language")
	free_income = models.IntegerField(doc="free income in euro")
	smoking = models.PositiveSmallIntegerField(choices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], widget=widgets.RadioSelectHorizontal, doc="smoking intensity on 0-10 likert")
	risk_soep = models.PositiveSmallIntegerField(choices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], widget=widgets.RadioSelectHorizontal, doc="SOEP risk question on 0-10 likert")
	math_grade = models.CharField(choices=['1.0', '1.3', '1.7', '2.0', '2.3', '2.7', '3.0', '3.3', '3.7', '4.0', '5.0'], doc="Abitur math grade")


	goal_of_experiment = models.TextField(doc="free form input for believed goal of experiment")
	payoff_importance = models.PositiveSmallIntegerField(choices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], widget=widgets.RadioSelectHorizontal, doc="0-10 likert on how important payoff considerations are for the participant")
	num_experiments = models.PositiveSmallIntegerField(doc="guessed number of previous experiment participations at AWI Lab")
	instructions_sufficient = models.TextField(doc="comments on the instructions / clarity")

	# Eckel and Grossman risk elicitation task
	eg_choice = models.PositiveSmallIntegerField(doc="eckel grossman task selected")
	eg_outcome = models.CharField(doc="eckel grossman task lottery outcome")
	eg_payoff = models.PositiveIntegerField(doc="eckel grossman task payoff if selected")


	crt_bat = models.FloatField(
		verbose_name="Ein Schläger und ein Ball kosten zusammen 1,10€. \
			Der Schläger kostet 1,00€ mehr als der Ball. Was kostet der Ball (in Cent)?", doc="ball/bat crt question")
	crt_machines = models.FloatField(
		verbose_name="Wenn 5 Maschinen 5 Minuten brauchen um 5 Werkstücke herzustellen, \
		wie lange würden 100 Maschinen brauchem um 100 Werkstücke herzustellen (in Minuten)?", doc="x machines in x minutes crt question")
	crt_lake = models.FloatField(
		verbose_name="Auf einem See befindet sich eine Fläche bedeckt mit Seerosen. Jeden \
		Tag verdoppelt sich die Grüße der bedeckten Fläche. Wenn es 48 Tage dauert, bis die \
		die Fläche den gesamten See bedeckt, wie lange würde es dauern, bis die Fläche den \
		halben See bedeckt (in Tagen)?", doc="lake flowers crt question")


	def play_Lottery(self):
		winning_probability = 0.5
		self.eg_outcome = "win" if random.random() < winning_probability else "lose"
		self.eg_payoff = Constants.lotteries[self.eg_choice][self.eg_outcome]

		if self.participant.vars['relevant_round'] == 0:
			self.payoff = c(self.eg_payoff/100)
			self.participant.vars['lottery_outcome'] = 'gelb' if self.eg_outcome == 'win' else 'grün'
			self.participant.vars['low_payoff'] = c(Constants.lotteries[self.eg_choice]['lose']/100)
			self.participant.vars['high_payoff'] = c(Constants.lotteries[self.eg_choice]['win']/100)