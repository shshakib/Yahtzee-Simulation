import os
import random
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
import pickle

from Yahtzee.Player import Player
from Yahtzee.MaximizeYahtzeesStrategy import MaximizeYahtzees
from Yahtzee.MarkovChainStrategy import MarkovChainStrategy
from Yahtzee.ProbabilisticStrategy import ProbabilisticStrategy
from Yahtzee.GreedyStrategy import GreedyStrategy
from Yahtzee.RationalYahtzeesStrategy import RationalYahtzeesStrategy
from Yahtzee.HeuristicStrategy import HeuristicStrategy

def simulate_games(strategy, num_games=10000):
    '''Simulate a number of games (default = 10000) for specified strategy and save results'''
    results_lst= []
    for i in range(num_games):
        player= Player(strategy)
        for j in range(13):
            player.play_turn()
            #print(f"Game {i+1}, Turn {j+1}: Roll - {player.dice.dice}, Scorecard - {player.scorecard.scores}")
        results_lst.append(player.scorecard.total_score())
    return results_lst


def analyze_results(results):
    '''Analyze the results and average/std score'''
    average_score = sum(results)/len(results)
    std_deviation = np.std(results)
    print(f"Average Score: {average_score}")
    print(f"Standard Deviation: {std_deviation}\n")

def save_results(strategy_name, results):
    '''Save results of the simulation to pkl'''
    with open(f'{strategy_name}_results.pkl', 'wb') as f:
        pickle.dump(results, f)

def load_results(strategy_name):
    '''Load results of before run from the simulation from pkl'''
    with open(f'{strategy_name}_results.pkl', 'rb') as f:
        return pickle.load(f)

if __name__ == "__main__":
    #Uncomment the following line and comment the line after if you want to run MarkovChain
    strategies = [HeuristicStrategy(), GreedyStrategy(), MaximizeYahtzees(), RationalYahtzeesStrategy(), ProbabilisticStrategy(), MarkovChainStrategy(num_simulations=1)]
    #strategies = [HeuristicStrategy(), MaximizeYahtzees(), RationalYahtzeesStrategy(), GreedyStrategy(), ProbabilisticStrategy()]

    for strategy in strategies:
        strategy_name_cls = strategy.__class__.__name__
        print(f"Testing strategy: {strategy_name_cls}")
        results_file = f'{strategy_name_cls}_results.pkl'
        if os.path.exists(results_file):
            print(f"Loading results for {strategy_name_cls}")
            results = load_results(strategy_name_cls)
        else:
            results = simulate_games(strategy)
            save_results(strategy_name_cls, results)
        analyze_results(results)
