"""
Reinforcement Learning in Artificial Intelligence Final Project.

Created on 04/13/2016
@author     : Manish Kumar, Prateek Bhat and Ritesh Agarwal
@desc       : Define the Opponent for Kuhn Poker
@version    : uses Python 2.7
"""
from __future__ import division
"Import libraries"
import random as rand
import numpy as np

"Returns an index on which it is decided either to bluff or not " \
"if returned index = 0, its a bluff otherwise not"
def decideonBluff(prob):
   p = [prob, 1 - prob]
   return np.where(np.random.multinomial(1,p))[0][0]

"Initialize the capital in hand at the beginning of each experiment  "
def initialCapital(initialMoney):
    global capital
    global startCapital
    startCapital = initialMoney
    capital = initialMoney

"Initialize the card at the start of each round"
def cardInit():
    global card
    card = None

"Our opponent can only take one action during the gameplay" \
"bet = the opponent will bet and pass = Opponent can either check or fold depending on the card in hand and action taken by the Agent  "
def takeFirstAction(minBet, agentAction):
    global capital

    "Always bet when card in hand is A "
    if card == "A":
        action = "bet"

    elif card == "K":
        "Bluff with this probability"
        bluffwhenKing = capital/200
        # print "Prob of bluff when King", bluffwhenKing
        # print "capital = ", capital
        flag = decideonBluff(bluffwhenKing)

        if flag == 0:
            action = "bet"
        else:
            action = "pass"
    else:
        "Bluff with this probability"
        bluffwhenQueen = capital/400
        # print "Prob of bluff when Queen", bluffwhenQueen
        flag = decideonBluff(bluffwhenQueen)

        if flag == 0:
            action = "bet"

        else:
            action = "pass"

    if action == "bet":
        if capital >= minBet:
            capital -= minBet

        else:
            minBet = capital
            capital -= capital
    else:
        minBet = 0

    return action, minBet
