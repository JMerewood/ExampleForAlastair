from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)
import random
import numpy


author = 'JM'

doc = """
SimpleAdditionTask
"""


class Constants(BaseConstants):
    name_in_url = 'Round1'
    players_per_group = None
    task_timer = 180
    num_rounds = 50
    payment_per_correct_answer = c(5)
    point_for_correct = 1
    max_rand = 99
    min_rand = 40
    num_rows = 3
    num_cols = 3


class Subsession(BaseSubsession):

    def creating_session(self):
        players = self.get_players()
        if 'task_timer' in self.session.config:
            task_timer = self.session.config['task_timer']
        else:
            task_timer = Constants.task_timer

        for p in self.get_players():
            p.task_timer = task_timer


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    combined_payoff = models.CurrencyField()
    number_entered = models.IntegerField(label='')
    sum_of_numbers = models.IntegerField()
    correct = models.IntegerField(initial=0)

    task_timer = models.IntegerField(
        doc=""" The length of the real effort task timer. """
    )

    rand_left = models.IntegerField()
    rand_mid = models.IntegerField()
    rand_right = models.IntegerField()
    solution = models.IntegerField()
    answer = models.IntegerField(label='')
    answer_correct = models.IntegerField(initial=0)
    num_correct = models.IntegerField(initial=0)
    m_left = numpy.zeros((Constants.num_rows, Constants.num_cols))
    m_mid = numpy.zeros((Constants.num_rows, Constants.num_cols))
    m_right = numpy.zeros((Constants.num_rows, Constants.num_cols))

    def initialize(self):
        self.num_correct = sum([p.answer_correct for p in self.in_all_rounds()])
        self.rand_left = random.randint(Constants.min_rand, Constants.max_rand)
        self.rand_mid = random.randint(Constants.min_rand, Constants.max_rand)
        self.rand_right = random.randint(Constants.min_rand, Constants.max_rand)
        self.solution = self.rand_left + self.rand_mid + self.rand_right

        for i in range(Constants.num_rows):
            for j in range(Constants.num_cols):
                self.m_left[i][j] = random.randint(0, self.rand_left - 1)
                self.m_mid[i][j] = random.randint(0, self.rand_mid - 1)
                self.m_right[i][j] = random.randint(0, self.rand_right - 1)

        self.m_left[random.randint(0, Constants.num_rows - 1)][random.randint(0, Constants.num_cols - 1)] = self.rand_left
        self.m_mid[random.randint(0, Constants.num_rows - 1)][random.randint(0, Constants.num_cols -1)] = self.rand_mid
        self.m_right[random.randint(0, Constants.num_rows - 1)][random.randint(0, Constants.num_cols - 1)] = self.rand_right

