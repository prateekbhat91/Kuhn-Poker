"""
Reinforcement Learning in Artificial Intelligence Final Project.

Created on 04/13/2016
@author     : Manish Kumar, Prateek Bhat and Ritesh Agarwal
@desc       : Define the Agent for Kuhn Poker
@version    : uses Python 2.7
"""
from __future__ import division
import random
from collections import defaultdict
import operator
import math

import environment as env

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


Observe = observation()

def episodeEnd():
    Observe.delete()

"Parameters"
epsilon = 0.1
alpha = 0.1
gamma = 0.9
Lambda = 0.9

"Possible action sequences"
possibleActions = [("pass","pass",None),("bet","bet",None),("bet","pass",None),("pass","bet","pass"),("pass","bet","bet")]


"Q-value for eac state action pair"
Qvalue = defaultdict(dict)

"Eligibility traces"
eligibilityTraces = defaultdict(dict)

"Actions available"
actionAvailable = ["bet", "pass"]

def initialCapital(initialMoney):
    Observe.setCapital(initialMoney)


def cardInit():
    global card
    card = None

"To set the default value in a dictionary"
def setDefaultQvalue(money, Card):
    global card
    for cards in list(set(env.cardsAvailable) - set(card)):
        Qvalue[(money,Card)][cards]=defaultdict(dict)
        Qvalue[(money, Card)][cards].setdefault("count",0)
        for possActions in possibleActions:
            Qvalue[(money, Card)][cards].setdefault(possActions,0)
    # print "Qvalue in set default = ", Qvalue

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


"Initialize eligibility traces"
def etInit():
    eligibilityTraces = defaultdict(dict)

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














