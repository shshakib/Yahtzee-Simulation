from Yahtzee.Strategy import Strategy
from collections import Counter

class HeuristicStrategy(Strategy):
    def decide(self, roll, scorecard):
        """
        Apply predefined rules to keep dice hoping for specific combinations: Straights, Full House, Three/Four Kind, Yahtzee
        """
        return [] #We don't reroll in Heuristics

    def choose_category(self, dice, scorecard):
        """
        Prioritize high-scoring categories (Yahtzee, Full House, etc.). If no luck, then go with Chance category.
        """
        counts = Counter(dice)
        possible_categories = {}

        if 5 in counts.values() and 'Yahtzee' not in scorecard.used_categories:
            possible_categories['Yahtzee'] = 50
        if 3 in counts.values() and 2 in counts.values() and 'Full House' not in scorecard.used_categories:
            possible_categories['Full House'] = 25
        if sorted(dice) in [list(range(i, i + 5)) for i in range(1, 3)] and 'Large Straight' not in scorecard.used_categories:
            possible_categories['Large Straight'] = 40
        if len(set(dice)) == 5 and (sorted(dice)[-1] - sorted(dice)[0] == 4) and 'Large Straight' not in scorecard.used_categories:
            possible_categories['Large Straight'] = 40
        if (set([1, 2, 3, 4]).issubset(dice) or set([2, 3, 4, 5]).issubset(dice) or set([3, 4, 5, 6]).issubset(dice)) and 'Small Straight' not in scorecard.used_categories:
            possible_categories['Small Straight'] = 30
        if 4 in counts.values() and 'Four of a Kind' not in scorecard.used_categories:
            possible_categories['Four of a Kind'] = sum(dice)
        if 3 in counts.values() and 'Three of a Kind' not in scorecard.used_categories:
            possible_categories['Three of a Kind'] = sum(dice)
        
        # Add logic for number-based categories
        for number in range(1, 7):
            if str(number) not in scorecard.used_categories:
                possible_categories[str(number)] = counts[number] * number

        # Choose the highest available category
        if possible_categories:
            for category, score in sorted(possible_categories.items(), key=lambda item: -item[1]):
                if category not in scorecard.used_categories:
                    return category, score

        # Fallback to 'Chance' if all else fails
        return 'Chance', sum(dice)
    
    def is_straight(self, roll, large=False):
        """
        Check for Small or Large Straight
        """
        unique_values = sorted(set(roll))
        if large:
            return unique_values in [list(range(i, i + 5)) for i in range(1, 3)]
        return (set([1, 2, 3, 4]).issubset(unique_values) or
                set([2, 3, 4, 5]).issubset(unique_values) or
                set([3, 4, 5, 6]).issubset(unique_values))

    def is_full_house(self, roll):
        """
        Check for Full House.
        """
        counts = Counter(roll).values()
        return sorted(counts) == [2, 3]
