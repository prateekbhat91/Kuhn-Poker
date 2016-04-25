"""
Reinforcement Learning in Artificial Intelligence Final Project.

Created on 04/13/2016
@author     : Manish Kumar, Prateek Bhat and Ritesh Agarwal
@desc       : Define the environment for Kuhn Poker
@version    : uses Python 2.7
"""
from __future__ import division
import random
from collections import defaultdict
import math

import Agent as AG
import opponent as OP
import expectedSARSA as ALGO


"Deck of three cards"
cardsAvailable = ["A", "K", "Q"]
First = ""
Second = ""
Third = ""
Reward = ""
Opp_card = ""

minBet = 2

"Initialize Environment for a game"
def potInit():
    global pot
    pot = 0

"Deal cards to agent and opponent"
def dealcards():
    agentCard = random.choice(cardsAvailable)
    opponentCard = random.choice(list(set(cardsAvailable)-set([agentCard])))
    return agentCard, opponentCard

"Decides whose card is bigger"
def decideWinner(agentCard,opponentCard):
    agent_ind = cardsAvailable.index(agentCard)
    opp_ind = cardsAvailable.index(opponentCard)
    if agent_ind < opp_ind:
        winner = "agent"
    else:
        winner = "opponent"
    return  winner

"Showdown result"
def showDown(first, second, third, agentCard, opponentCard):
    show = False
    if first == second or third == second:
        winner = decideWinner(agentCard,opponentCard)
        show = True
    elif first == "bet" and second == "pass":
        winner = "agent"
    elif third == "pass":
        winner = "opponent"

    if winner == "agent":
        AG.Observe.capital += pot
        reward = 1
    else:
        OP.capital += pot
        reward = 0

    # print "Winner = ",winner
    return  reward,show

"Play a round"
def playGame(gameCount):
    global pot

    "Play a game"
    potInit()
    OP.cardInit()
    AG.cardInit()

    "Deal card from environment"
    AG.card, OP.card = dealcards()
    AG.setDefaultQvalue(AG.Observe.capital,AG.card )
    if gameCount != 1:
        ALGO.update(AG.card)

    "Minimum bets from both agent and opponent towards pot"
    pot = 2 * minBet

    AG.Observe.capital -= minBet
    OP.capital -= minBet




    "First action by agent"
    firstAction, firstbetAmount = AG.takeAction(minBet,1)
    secondAction, secondbetAmount = OP.takeFirstAction(minBet, firstAction)

    if firstAction == "pass" and secondAction == "bet":
        thirdAction, thirdbetAmount = AG.takeAction(minBet,2)
    else:
        thirdAction = None
        thirdbetAmount = 0

    pot += (firstbetAmount+secondbetAmount+thirdbetAmount)

    # print "Agent card = ", AG.card
    # print "Opponent card = ", OP.card
    # print "First Action = ", firstAction
    # print "Second Action = ", secondAction
    # print "Third Action = ", thirdAction


    reward,show = showDown(firstAction,secondAction, thirdAction, AG.card , OP.card )
    # raw_input()
    Opp_card = OP.card if show == True else None
    AG.Observe.updateObservation(reward,(firstAction,secondAction,thirdAction),firstbetAmount+thirdbetAmount+minBet,Opp_card,AG.card)








