from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Christian König genannt Kersting'

doc = """
Coinflip app to replicate Haghani and Dewey (2016).
"""


class Constants(BaseConstants):
    name_in_url = 'coinflip'
    players_per_group = None
    num_rounds = 1

    endowment = 100
    eur_per_point = 0.01
    betting_timeout = 60 # in seconds, equals 5min

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
	Punkte = models.PositiveIntegerField()
	Historie = models.TextField()

