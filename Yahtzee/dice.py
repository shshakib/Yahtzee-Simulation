import random
from collections import defaultdict

class Dice:
    def __init__(self):
        '''Creating a list for the five dice'''
        self.dice = [0] * 5

    def roll(self, keep=[]):
        '''Rolling a dice and keeping the ones that was selected'''
        for i in range(5):
            if i not in keep:
                self.dice[i] = random.randint(1, 6)
        return self.dice
    


# #Roll the dice
# def roll_dice(num_dice=5):
#     dice_results = []
#     for _ in range(num_dice):
#         dice_results.append(random.randint(1, 6))
#     return dice_results