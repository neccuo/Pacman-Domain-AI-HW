# multiAgents.py
# --------------
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


from pacman import PacmanRules
from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

INF = 9999999

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        if action == "Stop":
          return -99999
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        currFood = currentGameState.getFood()
        currCapsule = currentGameState.getCapsules()
        #for coor in currCapsule:
        #    tempX = coor[0]
        #    tempY = coor[1]
        #    newFood[tempX][tempY] = True
        #    currFood[tempX][tempY] = True
        

        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        x = newPos[0]
        y = newPos[1]

        oldPos = currentGameState.getPacmanPosition()
        oldX = oldPos[0]
        oldY = oldPos[1]

        totPoint = 0
        # legalAdjNodes = getLegalAdjNodes(successorGameState, x, y, currentGameState)
        # print legalAdjNodes

        #adjNodesDic = getAdjNodesDic(newPos, depthMode)

        # GET CLOSEST FOOD...
        if newPos in currCapsule:
            totPoint += 300 


        isScared = True
        for scaredTime in newScaredTimes:
          if scaredTime < 1:
            isScared = False
            break

        for ghostState in newGhostStates:
          ghostPosition = ghostState.getPosition()
          if manhattanDistance(newPos, ghostPosition) < 3:
            if isScared:
              totPoint += 1000
            else:
              totPoint -= 1000
        
        if currFood[x][y] == True:
          totPoint += 250

        totPoint += getClosestFoodPoint(x, y, oldX, oldY, newFood, 7)
        
        # print "curr POS: " + str(currentGameState.getPacmanPosition())
        # print "currPOS: " + str(currentGameState.getPacmanPosition()) + " succPos: " + str(newPos) + " totPoint: " + str(totPoint)
        
        return totPoint

def getClosestFoodPoint(x, y, oldX, oldY, newFood, depth=5):
    tempX = x
    tempY = y
    for mode in range(1, depth+1):
        for i in range(4):
            try:
                if i == 0:
                    tempX = x+mode
                    tempY = y
                elif i == 1:
                    tempX = x
                    tempY = y+mode
                elif i == 2:
                    tempX = x-mode
                    tempY = y
                elif i == 3:
                    tempX = x
                    tempY = y-mode
                if (tempX, tempY) != (oldX, oldY) and newFood[tempX][tempY]:
                    return (depth)-mode
            except:
                continue
                
    return 0


def getLegalAdjNodes(state, x, y, currentGameState):
  legalActions = PacmanRules.getLegalActions(state)
  legalAdjNodes = []
  xVal = 0
  yVal = 0
  for action in legalActions:
    if action == "West":
      xVal = x-1
      yVal = y
    elif action == "East":
      xVal = x+1
      yVal = y
    elif action == "North":
      xVal = x
      yVal = y+1
    elif action == "South":
      xVal = x
      yVal = y-1
    else: # stop
      continue

    if (xVal, yVal) != currentGameState or (xVal, yVal) != state:
      legalAdjNodes.append((xVal, yVal))
    #else: # stop
    #  legalAdjNodes.append((x, y))
  return legalAdjNodes


def getAdjNodesDic(pos, depth):
  adjNodesDic = {pos: 0}
  xMod = 0
  yMod = 0
  for it in range(1, depth+1):
    for xComb in range(3):
      if xComb == 0:
        xMod = -1
      elif xComb == 1:
        xMod = 0
      elif xComb == 2:
        xMod = +1
      for yComb in range(3):
        if yComb == 0:
          yMod = -1
        elif yComb == 1:
          yMod = 0
        elif yComb == 2:
          yMod = +1

        node = getAdjNodesDicHelper(pos, it, xMod, yMod)
        adjNodesDic[node] = it
  return adjNodesDic


def getAdjNodesDicHelper(pos, depth, xMod, yMod):
  newX = pos[0] + (depth*xMod)
  newY = pos[1] + (depth*yMod)
  return newX, newY

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        totalAgentCount = gameState.getNumAgents()
        depth = self.depth

        return self.getBestAction(gameState, depth, totalAgentCount)

    def getBestAction(self, state, depth, totalAgentCount):
        legalActions = state.getLegalActions(0)
        bestAction = None
        bestPoint = None
        
        for action in legalActions:
            newState = state.generateSuccessor(0, action)
            point = self.generatePoint(newState, 1, totalAgentCount, depth)
            temp = maxMinCompare(point, True, bestPoint)
            if temp != bestPoint:
                bestAction = action
                bestPoint = point
        return bestAction

    def generatePoint(self, state, itNum, totalAgentCount, depth):
        agentIndex = itNum % totalAgentCount
        actions = state.getLegalActions(agentIndex)
        itLim = (totalAgentCount*depth)-1
        isMax = isPacman(agentIndex)
        retVal = None

        if len(actions) == 0:
            return self.evaluationFunction(state)

        for action in actions:
            newState = state.generateSuccessor(agentIndex, action)
            if itNum != itLim:
                point = self.generatePoint(newState, itNum+1, totalAgentCount, depth)
            else:
                point = self.evaluationFunction(newState)
            retVal = maxMinCompare(point, isMax, retVal)
        return retVal


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        totalAgentCount = gameState.getNumAgents()
        depth = self.depth

        return self.getBestAction(gameState, depth, totalAgentCount)
    
    def getBestAction(self, state, depth, totalAgentCount, a=-INF, b=INF):
        legalActions = state.getLegalActions(0)
        bestAction = None
        bestPoint = None
        
        for action in legalActions:
            newState = state.generateSuccessor(0, action)
            point = self.generatePoint(newState, 1, totalAgentCount, depth, a, b)
            a = max(a, point)
            temp = maxMinCompare(point, True, bestPoint)
            if temp != bestPoint:
                bestAction = action
                bestPoint = point
        return bestAction

    # alpha-beta
    def generatePoint(self, state, itNum, totalAgentCount, depth, a, b):
        agentIndex = itNum % totalAgentCount
        actions = state.getLegalActions(agentIndex)
        itLim = (totalAgentCount*depth)-1
        isMax = isPacman(agentIndex)
        value = None

        if len(actions) == 0:
            return self.evaluationFunction(state)
        
        if isMax:
            value = -INF
            for action in actions:
                newState = state.generateSuccessor(agentIndex, action)
                if itLim != itNum:
                    temp = self.generatePoint(newState, itNum+1, totalAgentCount, depth, a, b)
                else:
                    temp = self.evaluationFunction(newState)
                value = max(value, temp)
                a = max(a, value)
                if a > b:
                    break

        else:
            value = INF
            for action in actions:
                newState = state.generateSuccessor(agentIndex, action)
                if itLim != itNum:
                    temp = self.generatePoint(newState, itNum+1, totalAgentCount, depth, a, b)
                else:
                    temp = self.evaluationFunction(newState)
                value = min(value, temp)
                b = min(b, value)
                if b < a:
                    break
        return value


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        totalAgentCount = gameState.getNumAgents()
        depth = self.depth

        return self.getBestAction(gameState, depth, totalAgentCount)

    def getBestAction(self, state, depth, totalAgentCount):
        legalActions = state.getLegalActions(0)
        bestAction = None
        bestPoint = None
        
        for action in legalActions:
            newState = state.generateSuccessor(0, action)
            point = self.generatePoint(newState, 1, totalAgentCount, depth)
            temp = maxMinCompare(point, True, bestPoint)
            if temp != bestPoint:
                bestAction = action
                bestPoint = point
        return bestAction

    def generatePoint(self, state, itNum, totalAgentCount, depth):
        agentIndex = itNum % totalAgentCount
        actions = state.getLegalActions(agentIndex)
        itLim = (totalAgentCount*depth)-1
        isMax = isPacman(agentIndex)
        retVal = None

        if len(actions) == 0:
            return self.evaluationFunction(state)

        if isMax:
            for action in actions:
                newState = state.generateSuccessor(agentIndex, action)
                if itNum != itLim:
                    point = self.generatePoint(newState, itNum+1, totalAgentCount, depth)
                else:
                    point = self.evaluationFunction(newState)  
                retVal = maxMinCompare(point, isMax, retVal)
        else: # random
            pointList = []
            tot = 0
            for action in actions:
                newState = state.generateSuccessor(agentIndex, action)
                if itNum != itLim:
                    point = self.generatePoint(newState, itNum+1, totalAgentCount, depth)
                else:
                    point = self.evaluationFunction(newState)
                pointList.append(float(point))
            for pt in pointList:
                tot += pt
            retVal = tot/float(len(pointList))

        return retVal

def maxMinCompare(newNum, isMax, minOrMax=None):
    if isMax:
        if minOrMax == None or newNum > minOrMax:
            return newNum
        return minOrMax
    else:
        if minOrMax == None or newNum < minOrMax:
            return newNum
        return minOrMax

def isPacman(agentIndex):
    if agentIndex == 0:
        return True
    return False

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

