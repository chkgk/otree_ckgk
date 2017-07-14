from otree.api import Currency as c, currency_range
from . import views
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):
    def play_round(self):
        if self.player.round_number <= self.session.config['main_task_rounds']:
            yield (views.MainTask, {'low_payoff': 50, 'high_payoff': 100})

            if self.player.lottery_outcome == 'high':
                correct_payoff = c(100)
            else:
                correct_payoff = c(50)

            assert self.player.lottery_payoff == correct_payoff