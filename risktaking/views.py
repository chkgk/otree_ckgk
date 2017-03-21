from otree.api import Currency as c, currency_range, safe_json
from . import models
from ._builtin import Page, WaitPage
from .models import Constants



class Settings(Page):
    form_model = models.Player
    form_fields = ['default', 'mode', 'max_steps', 'interval', 'small_step', 'big_step', 'skip_trial']

class Welcome(Page):
	pass

class Instructions1(Page):
	pass

class Instructions2(Page):
	def vars_for_template(self):
		return {
			'default': safe_json(self.player.default),
			'mode': safe_json(self.player.mode)		
		}

class TryOutAnnouncement(Page):
	pass

class TryOut(Page):
	def is_displayed(self):
		return self.player.skip_trial == "nein"

	def vars_for_template(self):
		return {
			'big_step': safe_json(self.player.big_step), 
			'interval': safe_json(self.player.interval),
			'default': safe_json(self.player.default),
			'mode': safe_json(self.player.mode)
		}

class MainTaskPrep(Page):
	pass

class MainTask(Page):
	form_model = models.Player
	form_fields = ['low_payoff', 'high_payoff']

	def vars_for_template(self):
		return {
			'small_step': safe_json(self.player.small_step),
			'big_step': safe_json(self.player.big_step),
			'max_steps': safe_json(self.player.max_steps), 
			'interval': safe_json(self.player.interval),
			'default': safe_json(self.player.default),
			'mode': safe_json(self.player.mode)
		}

	def before_next_page(self):
		self.player.set_payoff();

class Vignettes(Page):
	form_model = models.Player
	form_fields = ['ch_no', 'sq_act', 'sq_no', 'ch_act']

class Demographics(Page):
	form_model = models.Player
	form_fields = ['age', 'gender', 'studies']

class Feedback(Page):
    pass

class End(Page):
	pass


#page_sequence = [ Settings ] + [ Step for i in range(Constants.steps) ] + [ Feedback ]

page_sequence = [
#	Settings,
#	Welcome,
 	Instructions1,
 	Instructions2,
 	TryOutAnnouncement,
#	TryOut,
 	MainTaskPrep,
#	MainTask,
	Vignettes,
	Demographics,
#	Feedback,
	End
]
