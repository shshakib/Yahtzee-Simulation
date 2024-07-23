from Yahtzee.Strategy import Strategy
from collections import Counter

class RationalYahtzeesStrategy(Strategy):
    def decide(self, roll, scorecard):
        counts = Counter(roll)
        target_value = counts.most_common(1)[0][0]
        keep_indices_lst = [index for index, value in enumerate(roll) if value == target_value]
        return keep_indices_lst

    def choose_category(self, dice, scorecard):
        counts = Counter(dice)
        possible_categories = {}

        if 5 in counts.values() and 'Yahtzee' not in scorecard.used_categories:
            return 'Yahtzee', 50
        if sorted(dice) in [list(range(i, i + 5)) for i in range(1, 3)] and 'Large Straight' not in scorecard.used_categories:
            return 'Large Straight',40
        if len(set(dice)) == 5 and (sorted(dice)[-1] - sorted(dice)[0]== 4) and 'Large Straight' not in scorecard.used_categories:
            return 'Large Straight',40
        if (set([1, 2, 3, 4]).issubset(dice) or set([2, 3, 4, 5]).issubset(dice) or set([3, 4, 5, 6]).issubset(dice)) and 'Small Straight' not in scorecard.used_categories:
            return 'Small Straight',30
        if 3 in counts.values() and 2 in counts.values() and 'Full House' not in scorecard.used_categories:
            return 'Full House',25
        if 4 in counts.values() and 'Four of a Kind' not in scorecard.used_categories:
            return 'Four of a Kind', sum(dice)
        if 3 in counts.values() and 'Three of a Kind' not in scorecard.used_categories:
            return 'Three of a Kind', sum(dice)

        for number in range(1, 7):
            if str(number) not in scorecard.used_categories:
                return str(number), counts[number]*number

        return 'Chance', sum(dice)
