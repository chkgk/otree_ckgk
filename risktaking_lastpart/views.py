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
	pass


page_sequence = [
	Vignettes,
	Demographics,
	End
]
