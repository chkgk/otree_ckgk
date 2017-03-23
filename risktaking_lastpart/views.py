from otree.api import Currency as c, currency_range, safe_json
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class Vignettes(Page):
	form_model = models.Player
	form_fields = ['ch_no', 'sq_act', 'sq_no', 'ch_act']

class Demographics(Page):
	form_model = models.Player
	form_fields = ['age', 'gender', 'studies']

	
class End(Page):
	def vars_for_template(self):
		return {
			'relevant_round': self.participant.vars['relevant_round'],
			'lottery_outcome': self.participant.vars['lottery_outcome'],
			'low_payoff': self.participant.vars['low_payoff'],
			'high_payoff': self.participant.vars['high_payoff'],
			'payoff': self.participant.payoff,
			'payoff_euro': self.participant.payoff.to_real_world_currency(self.session),
			'participation_fee': self.session.config['participation_fee'],
			'payoff_total': self.participant.payoff_plus_participation_fee()
		}



page_sequence = [
	Vignettes,
	Demographics,
	End
]
