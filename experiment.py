import environment as env
import Agent as AG
import opponent as OP

"Initial capital to start with"
initialCapital = 100

'initialize both agents here, play till any one of the agents looses all the capital.'

numExperiments = 1000000



for _ in range(numExperiments):
    "Initialize agent and opponent"
    AG.initialCapital(initialCapital)
    OP.initialCapital(initialCapital)
    AG.etInit()
    gameCount = 1

    "Agent and Opponent can only play a game of they have capital = minimum bet"
    while(AG.Observe.capital >= env.minBet and OP.capital >= env.minBet):

        env.playGame(gameCount)
        gameCount += 1
    AG.episodeEnd()
    print "\n"
    print "Agent capital = ", AG.Observe.capital
    print "Oponent captital = ", OP.capital
    print "Qvalue = ", AG.Qvalue
    raw_input()

