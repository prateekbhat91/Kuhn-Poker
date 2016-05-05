"""
Reinforcement Learning in Artificial Intelligence Final Project.

Created on 04/24/2016
@author     : Manish Kumar, Prateek Bhat and Ritesh Agarwal
@desc       : Define the Algorithms for Kuhn Poker
@version    : uses Python 2.7
"""
"Import libraries"
import random

"Import modules created"
import Agent as AG
import environment as env
from math import sqrt


"Parameters of the game"
alpha = 0.1
gamma = 0.9
Lambda = 0.9
epsilon = 0.1
kappa = 0.00002

"observe function"
def selectMaxAction(state):
    cardList = []

    for cards in AG.Qvalue[state].keys():
        max_value = float("-inf")
        item_list = AG.Qvalue[state][cards].items()

        for item in item_list:
            if item[0] == "count":
                pass
            else:
                if item[1] >= max_value:
                    max_value = item[1]


        maxActionlist = [act[0] for act in item_list if act[1] == max_value and act[0] != "count"]
        cardList.append((cards,random.choice(maxActionlist)))


    # print "Action list = ", maxActionlist
    # print "Max action = ", max_action
    # raw_input()
    return cardList


def calculate_dist(state):
    card_list = []
    maxCardAction = selectMaxAction(state)
    for cardAction in maxCardAction:
        card = cardAction[0]
        action = cardAction[1]
        value = 0
        for item in AG.Qvalue[state][card].items():
            if item[0] != "count":
                if item[0] == action:
                    value += ((1-epsilon)+(epsilon/len(AG.possibleActions)))*item[1]
                else:
                    value += (epsilon/len(AG.possibleActions))*item[1]
        card_list.append((card,value))

    return  card_list


def distribution(state):
    tempCards = []
    for oppCard in AG.Qvalue[state].keys():
        card1 = oppCard
        num1 = AG.Qvalue[state][oppCard]["count"]
        tempCards.append((card1, num1))
    try:
        card1_avg = tempCards[0][1] / (tempCards[0][1] + tempCards[1][1])
    except:
        card1_avg = 0.5
    card1 = tempCards[0][0]

    card2_avg = 1- card1_avg

    Sarsaprob = calculate_dist(state)
    value = 0
    for item in Sarsaprob:
        if item[0]== card1:
            value += card1_avg * item[1]
        else:
            value += card2_avg * item[1]
    return value

"Update time record for each state actionSequence"
def updateTime():
    for state in AG.Model.keys():
        for opp_card in AG.Model[state].keys():
            for action in AG.Model[state][opp_card].keys():
                AG.timeRecord[state][opp_card][action] += 1 
        

"Update the Qvalue and Eligibility traces"
'Takes an argument which is equal to the next card dealt'
def update(nextCard):
    observe = AG.Observe
    sign = 1 if observe.reward == 0 else -1
    capital = observe.capital + sign * observe.betamount
    state = (capital,observe.lastCard)
    nextState = (observe.capital,nextCard)

    "When the opponent folds and the card is not shown we guess about what card the opponent might have"
    if observe.opponentCard == None:
        if observe.lastCard == "A":
            if random.random() > 0.5:
                observe.opponentCard = "K"
            else:
                observe.opponentCard = "Q"
        elif observe.lastCard == "K":
            observe.opponentCard = "Q"
        else:
            observe.opponentCard = "K"



    AG.setDefaultQvalue(capital,observe.lastCard)
    # AG.setDefaultModel(capital,observe.lastCard)
    AG.setDefaultTime(capital,observe.lastCard)
    # print "Start capital = ",capital
    # print "Capital after game play = ", observe.capital
    # print "state = ", state
    # print "Qvalue state= ", AG.Qvalue[state]
    # print "opponent card = ", observe.opponentCard
    # print "count = ",AG.Qvalue[state][observe.opponentCard]["count"]
    # print "\n"
    # raw_input()

    "Increment the count"
    # print "Qvalue = ", AG.Qvalue
    # print "State = ", state
    # print "Opp card observed = ", observe.opponentCard
    # print "\n"
    AG.Qvalue[state][observe.opponentCard]["count"] += 1
    # prob_dist = distribution(nextState)
    stateActionList = selectMaxAction(nextState)

    max_card , nextAction = random.choice(stateActionList)
    # print max_card
    # print nextAction
    AG.setDefaultQvalue(observe.capital,nextCard)
    max_actionValue = AG.Qvalue[nextState][max_card][nextAction]
    "Calculate the TD Error"
    tdError = observe.reward + (gamma * max_actionValue - AG.Qvalue[state][observe.selectedCard][observe.actionSequence])

    # print "Regarding ET"
    # print "ET = ", AG.eligibilityTraces
    # print "State = ", state
    # print "Selected card = ", observe.selectedCard

    "Set default values in Eligibility traces"
    AG.setDefaultModel(state,observe.selectedCard,observe.actionSequence)
    AG.setDefaultTime(capital,observe.lastCard)

    "update the time for each state actionSequence"
    updateTime()
    "Update the Eligibility traces using Dutch traces"
    AG.Model[state][observe.selectedCard][observe.actionSequence] = (nextState,observe.reward)

    AG.Qvalue[state][observe.selectedCard][observe.actionSequence] += alpha*tdError

    " Expected SARSA Update"
    for plan in range(100):
        random_state = random.choice(AG.Model.keys())
        random_opp_card = random.choice(AG.Model[random_state].keys())
        random_action = random.choice(AG.Model[random_state][random_opp_card].keys())
        (state_dash,rand_reward) = AG.Model[random_state][random_opp_card][random_action]
        money,card = random_state
        AG.setDefaultTime(money,card)
        rand_reward += (kappa * sqrt(AG.timeRecord[random_state][random_opp_card][random_action]))
        stateActionList = selectMaxAction(state_dash)
        rand_card , randAction = random.choice(stateActionList)
        rand_max_value = gamma * (AG.Qvalue[state_dash][rand_card][randAction])
        AG.Qvalue[random_state][random_opp_card][random_action] += (alpha * (rand_reward + rand_max_value - AG.Qvalue[random_state][random_opp_card][random_action]))