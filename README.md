# Yahtzee Strategy Simulation

## Overview
This project simulates the game of Yahtzee using different strategies. The program uses an object-oriented approach and a different class for each strategy. The main code runs simulations for each strategy, analyzes the results, and saves the simulation data for further use.

## Structure

### Main Code
The main code **Simulates Games** which runs a specified number of games for each strategy. Then it will **Analyze Results** by calculating and printing the average score for each strategy. It also handles **Saves/Loads Results** for future uses.

### Strategies
The following strategies are implemented:
1. **Greedy Strategy**: Considers current state to gain the most out of it by keeping dice with the highest frequency.
2. **Heuristic Strategy**: Uses predefined rules.
3. **Maximize Yahtzees Strategy**: Keeping the dice that match the value of our first roll trying to maximize Yahtzee
4. **Probabilistic Strategy**: Keeps the dice with the highest frequency to maximize the chances of high-value combinations.
5. **Rational Yahtzees Strategy**: Like the Probabilistic Strategy but also considers other combinations.

### Other Classes
- **Dice**: Handles the rolling and keeping of dice.
- **Player**: Manages the player's scorecard, dice, and strategy, and plays turns accordingly.
- **ScoreCard**: Tracks the scores for various categories in Yahtzee.

## Running the Simulation
To run the simulation ensure you have all dependencies installed: such as NumPy, Matplotlib, and then run the main code main.py. The main code will:
- Test each strategy by simulating a series of games.
- Print the average score for each strategy.
- Load or save the results to a file.

### Example Output
```plaintext
Testing strategy: HeuristicStrategy
Average Score: 121.4257
Standard Deviation: 27.322903936258314

Testing strategy: MaximizeYahtzees
Average Score: 144.6301
Standard Deviation: 32.95189636409413

Testing strategy: RationalYahtzeesStrategy
Average Score: 124.5453
Standard Deviation: 32.08900976829918
.
.
.

...
```

## Customizing the Simulation
You can change the number of game runs by editing the `num_games` in the `simulate_games` function call.

---
## Sources
https://github.com/dpmerrell/yahtzee
https://en.wikipedia.org/wiki/Yahtzee
http://gunpowder.cs.loyola.edu/~jglenn/research/optimal_yahtzee.pdf
https://www-set.win.tue.nl/~wstomv/misc/yahtzee/Yahtzee-talk-NWD.pdf
