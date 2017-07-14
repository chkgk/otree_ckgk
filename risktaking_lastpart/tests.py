from otree.api import Currency as c, currency_range
from . import views
from ._builtin import Bot
from .models import Constants

class PlayerBot(Bot):
    def play_round(self):
        # come up with failing inputs

        # passing inputs
        yield (views.RiskTask, {'eg_choice': 5})

        yield (views.CognitiveReflection, {
            'crt_bat': 5,
            'crt_machines': 5,
            'crt_lake': 47
        })

        yield (views.Questionnaire, {
            'instructions_sufficient': 'yes, totally',
            'num_experiments': 20,
            'goal_of_experiment': 'learning cool stuff',
            'payoff_importance': 3
        })
        
        yield (views.Demographics, {
            'age': 20,
            'gender': 'männlich',
            'studies': 'Economics', 
            'native_german': True, 
            'smoking': 5, 
            'free_income': 400, 
            'math_grade': '2.0', 
            'risk_soep': 3,
        })
    