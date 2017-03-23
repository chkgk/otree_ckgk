from otree.api import Currency as c, currency_range, safe_json
from . import models
from ._builtin import Page, WaitPage
from .models import Constants



class Welcome(Page):
	def vars_for_template(self):
		return {
			'exchange_rate': format(self.session.real_world_currency_per_point*100, '.2f').replace('.', ',')
		}

class Instructions1(Page):
	pass

class Instructions2(Page):
	def vars_for_template(self):
		return {
			'default': safe_json(self.participant.vars['default']),
			'mode': safe_json(self.participant.vars['mode']),
			'big_step': safe_json(self.session.vars['big_step']), 
			'small_step': safe_json(self.session.vars['small_step']),
			'interval': safe_json(self.session.vars['interval']),
		}

class TryOutAnnouncement(Page):
	pass

class TryOut(Page):

	def vars_for_template(self):
		return {
			'big_step': safe_json(self.session.vars['big_step']), 
			'small_step': safe_json(self.session.vars['small_step']),
			'interval': safe_json(self.session.vars['interval']),
			'default': safe_json(self.participant.vars['default']),
			'mode': safe_json(self.participant.vars['mode'])
		}

class MainTaskPrep(Page):
	pass


page_sequence = [
	Welcome,
	Instructions1,
	Instructions2,
	TryOutAnnouncement,
	TryOut,
	MainTaskPrep
]
