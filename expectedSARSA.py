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

"Parameters of the game"
alpha = 0.1
gamma = 0.9
Lambda = 0.9
epsilon = 0.1

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




    # print "Start capital = ",capital
    # print "Capital after game play = ", observe.capital
    # print "state = ", state
    # print "Qvalue state= ", AG.Qvalue[state]
    # print "opponent card = ", observe.opponentCard
    # print "count = ",AG.Qvalue[state][observe.opponentCard]["count"]
    # print "\n"
    # raw_input()

    "Incremetn the count of that "
    AG.Qvalue[state][observe.opponentCard]["count"] += 1
    prob_dist = distribution(nextState)

    "Calculate the TD Error"
    tdError = observe.reward + (gamma * prob_dist - AG.Qvalue[state][observe.selectedCard][observe.actionSequence])

    # print "Regarding ET"
    # print "ET = ", AG.eligibilityTraces
    # print "State = ", state
    # print "Selected card = ", observe.selectedCard

    "Set default values in Eligibility traces"
    AG.setDefaultET((state,observe.selectedCard))

    "Update the Eligibility traces using Dutch traces"
    AG.eligibilityTraces[(state,observe.selectedCard)][observe.actionSequence] = (1-alpha)*AG.eligibilityTraces[(state,observe.selectedCard)][observe.actionSequence] +1

    " Expected SARSA Update"
    for state in AG.Qvalue.keys():
        for currCard in AG.Qvalue[state]:
            for action in AG.Qvalue[state][currCard]:
                if action != "count":
                    AG.setDefaultET(((state,currCard)))
                    # print "\n Before update "
                    # print "State = ", state
                    # print "Curr card = ", currCard
                    # print "action = ", action
                    # print AG.eligibilityTraces
                    # raw_input()
                    AG.Qvalue[state][currCard][action] += alpha*tdError*AG.eligibilityTraces[(state,currCard)][action]
                    AG.eligibilityTraces[(state, currCard)][action] = gamma * Lambda *AG.eligibilityTraces[(state,currCard)][action]







