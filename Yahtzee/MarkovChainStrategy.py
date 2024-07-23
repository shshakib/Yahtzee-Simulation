import os
import random
import pickle
from collections import defaultdict, Counter
from itertools import product, combinations
from Yahtzee.Strategy import Strategy

class MarkovChainStrategy(Strategy):
    def __init__(self, num_simulations=1, seed=42, feasible_states_file='feasible_states.pkl'):
        self.value_table = defaultdict(int)
        self.policy_table = {}
        self.num_simulations = num_simulations
        self.seed = seed
        self.feasible_states_file = feasible_states_file
        self.results_file = 'markov_chain_results.pkl'
        self.last_state_file = 'last_strategy_state.pkl'
        self.current_iteration = 0
        
        if os.path.exists(self.feasible_states_file):
            self.feasible_states = self.load_feasible_states()
        else:
            self.feasible_states = list(self.generate_feasible_states())
            self.save_feasible_states(self.feasible_states)
        
        self.initialize_tables()

        if os.path.exists(self.last_state_file):
            self.load_state(self.last_state_file)
        
        self.monte_carlo_value_iteration()

    def initialize_tables(self):
        for state in self.feasible_states:
            self.value_table[state] = 0
            self.policy_table[state] = None

    def generate_feasible_states(self):
        dice_combinations = MarkovChainStrategy.generate_dice_combinations()
        scorecard_states = MarkovChainStrategy.generate_scorecard_states()
        feasible_states = []
        for dice in dice_combinations:
            for scorecard in scorecard_states:
                state = MarkovChainStrategy.create_state(dice, scorecard)
                feasible_states.append(state)
        return feasible_states

    @staticmethod
    def create_state(dice, scorecard):
        return (dice, scorecard)

    @staticmethod
    def generate_dice_combinations():
        return list(product(range(1, 7), repeat=5))

    @staticmethod
    def generate_scorecard_states():
        categories = ['1', '2', '3', '4', '5', '6', '3K', '4K', 'FH', 'SS', 'LS', 'Y', 'C']
        states_lst = []
        for r in range(len(categories) + 1):
            for combo in combinations(categories, r):
                states_lst.append(frozenset(combo))
        return states_lst

    def save_feasible_states(self, states_lst):
        with open(self.feasible_states_file, 'wb') as f:
            pickle.dump(states_lst, f)

    def load_feasible_states(self):
        with open(self.feasible_states_file, 'rb') as f:
            return pickle.load(f)

    def monte_carlo_value_iteration(self, gamma=0.9):
        random.seed(self.seed)
        for iteration in range(self.current_iteration, self.num_simulations):
            delta = 0
            for state in self.feasible_states:
                v = self.value_table[state]
                max_value = float('-inf')
                best_action = None
                for action in self.generate_possible_actions():
                    new_state, reward = self.simulate(state, action)
                    value = reward + gamma * self.value_table[new_state]
                    if value > max_value:
                        max_value = value
                        best_action = action
                self.value_table[state] = max_value
                self.policy_table[state] = best_action
                delta = max(delta, abs(v - self.value_table[state]))
            if delta < 10:
                break

            self.current_iteration = iteration + 1
            self.save_state(self.last_state_file)
            self.save_state(f'strategy_state_{iteration + 1}.pkl')

        self.save_state(self.results_file)

    @staticmethod
    def generate_possible_actions():
        actions_lst = []
        for r in range(6):
            for combo in combinations(range(5), r):
                actions_lst.append(combo)
        return actions_lst

    def simulate(self, state, action):
        dice, scorecard = state
        new_dice = self.roll_dice(dice, action)
        reward = self.compute_reward(new_dice, scorecard)
        new_state = (new_dice, scorecard)
        return new_state, reward

    @staticmethod
    def roll_dice(dice, action):
        new_dice = list(dice)
        for i in action:
            new_dice[i] = random.randint(1, 6)
        return tuple(new_dice)

    @staticmethod
    def compute_reward(dice, scorecard):
        counts = Counter(dice)
        if 5 in counts.values():
            return 50
        if 3 in counts.values() and 2 in counts.values():
            return 25
        if any(set(range(i, i+5)) <= set(dice) for i in range(1, 3)):
            return 40
        if any(set(range(i, i+4)) <= set(dice) for i in range(1, 4)):
            return 30
        if 4 in counts.values():
            return 30
        if 3 in counts.values():
            return 20
        return sum(dice)

    def decide(self, roll, scorecard):
        state = (tuple(roll), frozenset(scorecard.used_categories))
        action = self.policy_table.get(state, [])
        return action

    def save_state(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump((self.value_table, self.policy_table, self.current_iteration), f)

    def load_state(self, filename):
        with open(filename, 'rb') as f:
            self.value_table, self.policy_table, self.current_iteration = pickle.load(f)
