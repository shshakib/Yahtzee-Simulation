import random
from collections import defaultdict

class ScoreCard:
    def __init__(self):
        '''Scorecard using a default dict'''
        self.scores = defaultdict(int)
        self.used_categories = set()

    def update(self, category, score):
        '''Update scorecard with new score checking to make sure category is not already used'''
        if category not in self.used_categories:
            self.scores[category] = score
            self.used_categories.add(category)
        else:
            self.scores[category] = max(self.scores[category], score)  # Ensure we don't override with lower scores

    def total_score(self):
        '''Calculate the total score, including the upper section'''
        upper_section = sum(self.scores[num] for num in range(1, 7))
        bonus = 35 if upper_section >= 63 else 0
        lower_section = sum(score for category, score in self.scores.items() if isinstance(category, str))
        return upper_section + bonus + lower_section
