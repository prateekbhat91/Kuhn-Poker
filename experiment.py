import sys
import os
import atexit
import cPickle as pickle

"Import modules"
import environment as env
import Agent as AG
import opponent as OP

def exit_handler():
    print 'Application is ending!'
    with open('Qvalue.p', 'wb') as fp:
        pickle.dump(AG.Qvalue, fp)


def main(link):
    'initialize both agents here, play till any one of the agents looses all the capital.'
    if link !=None:
        with open(link, 'rb') as handle:
            AG.Qvalue = pickle.load(handle)

    # print "Loaded Qvalue = ", AG.Qvalue
    # raw_input()
    "Initial capital to start with"
    initialCapital = 100

    numExperiments = 10000
    agentWins = 0
    opponentWins = 0
    for i in range(numExperiments):
        "Initialize agent and opponent"
        AG.initialCapital(initialCapital)
        OP.initialCapital(initialCapital)
        gameCount = 1

        "Agent and Opponent can only play a game of they have capital = minimum bet"
        while(AG.Observe.capital >= env.minBet and OP.capital >= env.minBet):

            env.playGame(gameCount)
            gameCount += 1

        print "Done with",i+1, "experiment"


        # print "Agent capital = ", AG.Observe.capital
        # print "Oponent captital = ", OP.capital
        if AG.Observe.capital > OP.capital:
            agentWins += 1
        else:
            opponentWins += 1

        # print "Opponent wins = ", opponentWins
        # print "Agent Wins = ", agentWins
        # print "\n"

        with open("outputDynaQ+.txt", "a") as f:
            f.write("Episode = " + str(i + 1) + "\n" + "Opponent wins = " + str(opponentWins) + "\n" + "Agent wins = " + str(agentWins) + "\n" + "\n")
        f.close()

	"Delete the observe object in the agent"
        AG.episodeEnd()

        # print "Qvalue = ", AG.Qvalue
        # raw_input()

    atexit.register(exit_handler)



if __name__ == '__main__':
    try:
        print "Do you want to load any previous Qvalue ?\n"
        input = raw_input()
        if input.lower() == "yes":
            print "Provide the link of the file to be loaded\n"
            link = raw_input()
        else:
            link = None

        main(link)

    except KeyboardInterrupt:

        print '\n Keyboard Interruption'
        atexit.register(exit_handler)
