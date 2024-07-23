from Yahtzee.dice import Dice
from Yahtzee.ScoreCard import ScoreCard
from Yahtzee.HeuristicStrategy import HeuristicStrategy

class Player:
    def __init__(self, strategy):
        self.scorecard = ScoreCard()
        self.dice =Dice()
        self.strategy = strategy

    def play_turn(self):
        if isinstance(self.strategy, HeuristicStrategy):
            roll = self.dice.roll()
            best_category, best_score=self.strategy.choose_category(roll, self.scorecard)
            self.scorecard.update(best_category, best_score)
        else:
            keep_lst = []
            final_roll = []
            for roll_num in range(3):
                roll = self.dice.roll(keep_lst)
                if roll_num < 2:
                    keep_lst = self.strategy.decide(roll, self.scorecard)
                final_roll = roll
            best_category, best_score = self.strategy.choose_category(final_roll, self.scorecard)
            self.scorecard.update(best_category, best_score)


