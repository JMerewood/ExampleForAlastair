from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import random
import time

class start(Page):

    def is_displayed(self):
        return self.round_number == 1

    def before_next_page(self):
        self.participant.vars['correctr1'] = 0
        self.participant.vars['expiry_timestamp'] = time.time() + self.player.task_timer


class Sum(Page):
    form_model = 'player'
    form_fields = ['answer']

    def get_timeout_seconds(self):
        return self.participant.vars['expiry_timestamp'] - time.time()

    def is_displayed(self):
        if self.participant.vars['expiry_timestamp'] - time.time() > 3:
            return True
        else:
            return False


    def vars_for_template(self):
        self.player.initialize()

        return {
        }

    def before_next_page(self):
        if self.player.answer == self.player.solution:
            self.player.answer_correct = 1
            self.player.payoff = Constants.payment_per_correct_answer
            self.player.correct = Constants.point_for_correct
            self.participant.vars['correctr1'] += self.player.correct


class results(Page):

    def is_displayed(self):
        if self.round_number == Constants.num_rounds:
            return True
        else:
            return False

    def vars_for_template(self):

        all_players = self.player.in_all_rounds()
        combined_payoff = 0
        for player in all_players:
            combined_payoff += player.payoff
            self.player.combined_payoff = combined_payoff
        return{
            'combined_payoff': combined_payoff,
            }

    def before_next_page(self):
        self.participant.vars['payoffr1'] = self.player.combined_payoff





page_sequence = [start,
                 Sum,
                 results,]
