from otree.api import Currency as c, currency_range, safe_json
from . import models
from ._builtin import Page, WaitPage
from .models import Constants



class Settings(Page):
    form_model = models.Player
    form_fields = ['default', 'mode', 'max_steps', 'interval', 'small_step', 'big_step']


class MainTask(Page):
	def vars_for_template(self):
		return {
			'small_step': safe_json(self.player.small_step),
			'big_step': safe_json(self.player.big_step),
			'max_steps': safe_json(self.player.max_steps), 
			'interval': safe_json(self.player.interval),
			'default': safe_json(self.player.default),
			'mode': safe_json(self.player.mode)
		}

class Feedback(Page):
    pass


#page_sequence = [ Settings ] + [ Step for i in range(Constants.steps) ] + [ Feedback ]

page_sequence = [
	Settings,
	MainTask
]
