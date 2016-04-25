"""
Reinforcement Learning in Artificial Intelligence Final Project.

Created on 04/13/2016
@author     : Manish Kumar, Prateek Bhat and Ritesh Agarwal
@desc       : Define the Opponent for Kuhn Poker
@version    : uses Python 2.7
"""
from __future__ import division
import random as rand
import numpy as np


def decideonBluff(prob):
   p = [prob, 1 - prob]
   return np.where(np.random.multinomial(1,p))[0][0]


def initialCapital(initialMoney):
    global capital
    global startCapital
    startCapital = initialMoney
    capital = initialMoney

def cardInit():
    global card
    card = None

def takeFirstAction(minBet, agentAction):
    global capital

    if card == "A":
        action = "bet"

    elif card == "K":
        bluffwhenKing = capital/200
        # print "Prob of bluff when King", bluffwhenKing
        # print "capital = ", capital
        flag = decideonBluff(bluffwhenKing)

        if flag == 0:
            action = "bet"
        else:
            action = "pass"
    else:
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

    # print "Car in hand = ", card
    # print "Capital = ", capital

    return action, minBet
