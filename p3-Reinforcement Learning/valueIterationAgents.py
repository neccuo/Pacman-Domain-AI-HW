# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0

        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        self.it()
        
    
    def it(self):
        mdp = self.mdp
        states = mdp.getStates()
        for i in range(1, self.iterations+1):
            valuePointer = self.values.copy()
            for state in states:
                pair = self.getBestValueAndAction(state)

                if pair != None:
                    valuePointer[state] = pair[0]
            self.values = valuePointer


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        # Q(s, a) = for s' in S T(s, a, s') * ( R(s, a, s') + discount * V*(s') )
        mdp = self.mdp
        stateProbPairList = mdp.getTransitionStatesAndProbs(state, action)
        sum = 0
        for nextStateProb in stateProbPairList:
            nextState = nextStateProb[0]
            prob = nextStateProb[1]
            sum += prob * (mdp.getReward(state, action, nextState) + self.discount * self.values[nextState])
        return sum

    def getBestValueAndAction(self, state):
        mdp = self.mdp
        actions = mdp.getPossibleActions(state)
        if len(actions) == 0:
            return None
        maxValue = -999999
        bestAction = None
        for action in actions:
            qVal = self.computeQValueFromValues(state, action)
            if qVal > maxValue:
                maxValue = qVal
                bestAction = action
        return (maxValue, bestAction)

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        valueActionPair = self.getBestValueAndAction(state)
        if valueActionPair == None: # if terminal
            return None
        return valueActionPair[1]

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
