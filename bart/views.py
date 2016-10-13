# -*- coding: utf-8 -*-
from __future__ import division

from otree.common import Currency as c, currency_range, safe_json

from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class GeneralInstructions(Page):
	pass

class RiskTask(Page):
	form_model = models.Player
	form_fields = ['lottery_choice']

	def before_next_page(self):
		self.player.play_Lottery()

class TrialInstructions(Page):
	pass

class TrialPage(Page):
	pass

class FirstBartBlueInstructions(Page):
	def is_displayed(self):
		return self.player.task_order == "blue_first"

	template_name = "bart/BlueTaskInstructions.html" # NEEDS TO BE ADJUSTED

class FirstBartGreenInstructions(Page):
	def is_displayed(self):
		return self.player.task_order != "blue_first"
		
	template_name = "bart/GreenTaskInstructions.html" # NEEDS TO BE ADJUSTED

class FirstBartBlue(Page):
	def is_displayed(self):
		return self.player.task_order == "blue_first"

	form_model = models.Player
	template_name = "bart/BlueMainTask.html"
	form_fields = ['bart_blue_raw_data', 'bart_blue_sum_collected', 'bart_blue_avg_time', 'bart_blue_num_intact', 'bart_blue_avg_pumps_intact']

class FirstBartGreen(Page):
	def is_displayed(self):
		return self.player.task_order != "blue_first"

	form_model = models.Player
	template_name = "bart/GreenMainTask.html"
	form_fields = ['bart_green_raw_data', 'bart_green_sum_collected', 'bart_green_avg_time', 'bart_green_num_intact', 'bart_green_avg_pumps_intact']



class SecondBartBlueInstructions(Page):
	def is_displayed(self):
		return self.player.task_order != "blue_first"
	template_name = "bart/BlueTaskInstructions.html" # NEEDS TO BE ADJUSTED

class SecondBartGreenInstructions(Page):
	def is_displayed(self):
		return self.player.task_order == "blue_first"
	template_name = "bart/GreenTaskInstructions.html" # NEEDS TO BE ADJUSTED

class SecondBartBlue(Page):
	def is_displayed(self):
		return self.player.task_order != "blue_first"

	form_model = models.Player
	template_name = "bart/BlueMainTask.html"
	form_fields = ['bart_blue_raw_data', 'bart_blue_sum_collected', 'bart_blue_avg_time', 'bart_blue_num_intact', 'bart_blue_avg_pumps_intact']

	def before_next_page(self):
		self.player.set_payoffs()


class SecondBartGreen(Page):
	def is_displayed(self):
		return self.player.task_order == "blue_first"

	form_model = models.Player
	template_name = "bart/GreenMainTask.html"
	form_fields = ['bart_green_raw_data', 'bart_green_sum_collected', 'bart_green_avg_time', 'bart_green_num_intact', 'bart_green_avg_pumps_intact']

	def before_next_page(self):
		self.player.set_payoffs()

class RiskQuestionnaire1(Page):
	form_model = models.Player
	form_fields = [
		'active_risk_1',
		'active_risk_2',
		'active_risk_3',
		'active_risk_4',
		'active_risk_5',
		'active_risk_6',

		'passive_risk_1',
		'passive_risk_2',
		'passive_risk_3',
		'passive_risk_4',
		'passive_risk_5',
		'passive_risk_6',
	]

class RiskQuestionnaire2(Page):
	form_model = models.Player
	form_fields = [
		'active_risk_7',
		'active_risk_8',
		'active_risk_9',
		'active_risk_10',
		'active_risk_11',
		'active_risk_12',

		'passive_risk_7',
		'passive_risk_8',
		'passive_risk_9',
		'passive_risk_10',
		'passive_risk_11',
		'passive_risk_12',
	]

class Questionnaires(Page):
	form_model = models.Player
	form_fields = ['age', 'female', 'studies', 'nationality']
	

class Results(Page):
	def vars_for_template(self):
		highpayoff = self.player.lotteries[self.player.lottery_choice]['win']
		lowpayoff = self.player.lotteries[self.player.lottery_choice]['lose']
		return { 'highpayoff': highpayoff, 'lowpayoff': lowpayoff }

class FinalPage(Page):
	def vars_for_template(self):
		totalpoints = self.player.payoff + 3000
		return { 'totalpoints': totalpoints, 'money_to_pay': self.participant.money_to_pay() }
	

# need to add the other pages later on
page_sequence = [
   # GeneralInstructions,
	RiskTask,
	TrialInstructions,
	TrialPage,
	FirstBartBlueInstructions,
	FirstBartGreenInstructions,
	FirstBartBlue,
	FirstBartGreen,
	SecondBartBlueInstructions,
	SecondBartGreenInstructions,
	SecondBartBlue,
	SecondBartGreen,
	RiskQuestionnaire1,
	RiskQuestionnaire2,
	Questionnaires,
	Results,
	FinalPage
]
