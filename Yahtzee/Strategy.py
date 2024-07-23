

#This is like a base strategy class to define a template for all other strategies
class Strategy:
    def decide(self, roll, scorecard):
        '''decision-making on which dice to keep'''
        pass

    def choose_category(self, dice, scorecard):
        '''Decision-making on which category to score'''
        pass