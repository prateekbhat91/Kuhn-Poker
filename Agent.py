"""
Reinforcement Learning in Artificial Intelligence Final Project.

Created on 04/13/2016
@author     : Manish Kumar, Prateek Bhat and Ritesh Agarwal
@desc       : Define the Agent for Kuhn Poker
@version    : uses Python 2.7
"""

from __future__ import division
"Import libraries"
import random
from collections import defaultdict
import operator
import math

"Import modules created"
import environment as env

"Parameters for the game"
epsilon = 0.01
alpha = 0.1
gamma = 0.9
Lambda = 0.9

"An object of this class will handle all te observations in the game like" \
"the capital on whihc the agent started the game, the reward obtained, action sequence played in the game" \
"the bet amount by the agent during the whole game, the oppoent card if it was shown otherwise None, " \
"the selected card during the decision of the max action selection "

class observation(object):

    def __init__(self):
        self.capital = 0
        self.reward = 0
        self.actionSequence = ()
        self.betamount = 0
        self.opponentCard = ""
        self.lastCard = ""
        self.selectedCard = ""

    def updateObservation(self,reward,action,bet,oppCard,agentCard):
        self.actionSequence = action
        self.betamount = bet
        self.opponentCard = oppCard
        self.lastCard = agentCard
        self.reward = reward

    def delete(self):
        self.capital = 0
        self.reward = 0
        self.actionSequence = ()
        self.pot = 0
        self.opponentCard = ""
        self.lastCard = ""

    def setCapital(self,amount):
        self.capital = amount

"Careate an observe object"
Observe = observation()

"Delete the observe object after the end of each experiment"
def episodeEnd():
    Observe.delete()

"Possible action sequences"
possibleActions = [("pass","pass",None),("bet","bet",None),("bet","pass",None),("pass","bet","pass"),("pass","bet","bet")]


"Q-value for each state action pair in the form " \
"{(capital, card in hand): opponent card {count:, possible action sequence: } }"
Qvalue = defaultdict(dict)

"Eligibility traces in the form" \
"{ ( (capital,card in hand) , probable opponent card):{ possible action sequence: } }"
eligibilityTraces = defaultdict(dict)

"Actions available"
actionAvailable = ["bet", "pass"]

"Set the initial capital to begin with"
def initialCapital(initialMoney):
    Observe.setCapital(initialMoney)

"Initialize the card in the beginning of each game"
def cardInit():
    global card
    card = None

"Initialize eligibility traces"
def etInit():
    eligibilityTraces = defaultdict(dict)


"To set the default value of Qvalues"
def setDefaultQvalue(money, Card):
    # global card
    for cards in list(set(env.cardsAvailable) - set(Card)):
        if cards not in Qvalue[(money,Card)].keys():
            Qvalue[(money,Card)][cards]=defaultdict(dict)
        Qvalue[(money, Card)][cards].setdefault("count",0)
        for possActions in possibleActions:
            Qvalue[(money, Card)][cards].setdefault(possActions,0)
    # print "Qvalue in set default = ", Qvalue


"To set the default value of Eligibility Traces"
def setDefaultET(state):
    for actions in possibleActions:
        eligibilityTraces[state].setdefault(actions,0)


"Returns the action which has the highest Qvalue"
def chooseMaxAction(state,turn):
    tempCards = []
    for oppCard in Qvalue[state].keys():
        card1 = oppCard
        num1 = Qvalue[state][oppCard]["count"]
        tempCards.append((card1,num1))

    randNum = random.random()

    try:
        card1_avg = tempCards[0][1]/ (tempCards[0][1]+tempCards[1][1])
        # card2_avg =  tempCards[1][1]/ (tempCards[0][1]+tempCards[1][1])
    except:
        card1_avg = 0.5
        # card2_avg = 0.5
    if randNum < card1_avg:
        cardSelected = tempCards[0][0]
    else:
        cardSelected = tempCards[1][0]

    max_value = float("-inf")
    item_list = []
    if turn == 1:
        item_list = Qvalue[state][cardSelected].items()
    else:
        for ind in xrange(2):
            action = possibleActions[3+ind]
            item = (action,Qvalue[state][cardSelected][action])
            item_list.append(item)

    for item in item_list:
        if item[0] == "count":
            pass
        else:
            if item[1] >= max_value:
                max_value = item[1]

    maxActionlist = [act[0] for act in item_list if act[1] == max_value and act[0] != "count"]
    max_action = random.choice(maxActionlist)
    # print "Action list = ", maxActionlist
    # print "Max action = ", max_action
    # raw_input()
    return max_action,cardSelected

"Choose epsilon greedy action"
def chooseEgreedyaction(state,turn):
    P = random.choice(range(1,11))
    if P <= epsilon*10:
        # print "Exploration"
        cardsLeft = list(set(env.cardsAvailable) - set(card))
        greedyCard = random.choice(cardsLeft)
        if turn == 1:
            greedyAction = random.choice(possibleActions)
        else:
            greedyAction = random.choice(possibleActions[3:])
    else:
        greedyAction,greedyCard = chooseMaxAction(state,turn)
    return greedyAction,greedyCard



"Returns the action taken and bet placed if any depending on the turn of the agent"
def takeAction(minBet,turn):
    global card

    setDefaultQvalue(Observe.capital,card)
    action,Observe.selectedCard = chooseEgreedyaction((Observe.capital,card),turn)
    # print "\n Inside take Action"
    # print "Eligibility traces = ", eligibilityTraces
    setDefaultET(((Observe.capital,card),Observe.selectedCard))
    # print "Eligibility traces after set default = ", eligibilityTraces
    # print "\n"
    if turn == 1:
        action = action[0]
    else:
        action = action[2]


    if action == "bet":
        if Observe.capital >= minBet:
            Observe.capital -= minBet

        else:
            minBet = Observe.capital
            Observe.capital -= Observe.capital
        setDefaultET(((Observe.capital, card), Observe.selectedCard))
    else:
        minBet = 0

    # print Qvalue
    # raw_input()
    return action,minBet














