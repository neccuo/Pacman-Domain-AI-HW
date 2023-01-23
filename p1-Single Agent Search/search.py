# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
from game import Directions

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    startP = problem.getStartState()
    stack = util.Stack() # for storing the directions
    explored = [] # for memorizing the explored nodes and not have an infinite loop

    dfs_helper(problem, startP, stack, explored)

    # for returning the directions
    dirList = []
    for opt in stack.list:
        dirList.append(getDirection(opt))
    return dirList

def dfs_helper(problem, state, stack, explored): # recursive
    if state in explored:
        stack.pop()
        return False
    explored.append(state)
    if problem.isGoalState(state): # terminates the recursion when the goal state is reached
        return True

    options = problem.getSuccessors(state)
    # opt
    # 0: pos, 1: direction, 2: cost=1
    for opt in options:
        stack.push(opt[1])
        if dfs_helper(problem, opt[0], stack, explored) == True:
            return True
    stack.pop()
    return False

def breadthFirstSearch(problem):
    mainQueue = util.Queue() # (state, dirQ): (node, required directions to get to the node)
    dirQ = util.Queue() # for storing directions
    explored = [] # for memorizing the explored nodes and not have an infinite loop

    mainQueue.push((problem.getStartState(), dirQ))

    stateAndDirPointer = mainQueue.pop()
    while not problem.isGoalState(stateAndDirPointer[0]):
        if stateAndDirPointer[0] in explored:
            stateAndDirPointer = mainQueue.pop()
            continue

        explored.append(stateAndDirPointer[0])
        options = problem.getSuccessors(stateAndDirPointer[0]) # possible directions to go from that node
        dirQ = stateAndDirPointer[1] # current state's direction queue
        # option
        # 0: pos, 1: direction, 2: cost=1
        for option in options:
            # copy the current node's direction
            tempDirQ = util.Queue()
            tempDirQ.list = dirQ.list[:]
            # add the direction to the queue to get the current->next
            tempDirQ.push(getDirection(option[1]))
            # assign it to the main queue
            mainQueue.push((option[0], tempDirQ))

        # get the next (state, dirQ) in line
        stateAndDirPointer = mainQueue.pop()
    
    # return the direction queue of the goal state
    qList = stateAndDirPointer[1].list

    return qList[::-1]


def uniformCostSearch(problem): # very similar to bfs with costs in play
    pQ = util.PriorityQueue() # (state, direction queue, total cost)
    # exploredDic = {} # { state: (dirQ, cost) }
    explored = []

    dirQ = util.Queue()
    state = problem.getStartState()
    cost = 0
    pQ.push((state, dirQ, cost), cost)
    # exploredDic[state] = (dirQ, cost)

    JUMBO_POINTER = pQ.pop()
    while not problem.isGoalState(JUMBO_POINTER[0]):
        if JUMBO_POINTER[0] in explored: #exploredDic.keys():
            JUMBO_POINTER = pQ.pop()
            continue
        currState = JUMBO_POINTER[0]
        explored.append(currState)

        currStatePQ = JUMBO_POINTER[1]
        currStateCost = JUMBO_POINTER[2]
        #if currState not in exploredDic.keys() or currStateCost < exploredDic[currState][1]:
        #    exploredDic[currState] = (currStatePQ, currStateCost)

        options = problem.getSuccessors(currState)
        # option
        # 0: pos, 1: direction, 2: cost=1
        for option in options:
            nextState = option[0]
            nextStatePQ = util.Queue()
            nextStatePQ.list = currStatePQ.list[:]
            nextStatePQ.push(getDirection(option[1]))

            nextStateCost = currStateCost + option[2]

            pQ.push((nextState, nextStatePQ, nextStateCost), nextStateCost)
        JUMBO_POINTER = pQ.pop()
    
    qList = JUMBO_POINTER[1].list
    return qList[::-1]


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic): # same with ucs except the heuristics
    pQ = util.PriorityQueue()
    explored = []

    dirQ = util.Queue()
    state = problem.getStartState()
    cost = 0
    # priority queue is sorted based on the cost + heuristic.
    pQ.push((state, dirQ, cost), cost + heuristic(state, problem))

    JUMBO_POINTER = pQ.pop()
    while not problem.isGoalState(JUMBO_POINTER[0]):
        if JUMBO_POINTER[0] in explored:
            JUMBO_POINTER = pQ.pop()
            continue
        currState = JUMBO_POINTER[0]
        explored.append(currState)
        currStatePQ = JUMBO_POINTER[1]
        currStateCost = JUMBO_POINTER[2]

        options = problem.getSuccessors(currState)
        # option
        # 0: pos, 1: direction, 2: cost=1
        for option in options:
            nextState = option[0]
            nextStatePQ = util.Queue()
            nextStatePQ.list = currStatePQ.list[:]
            nextStatePQ.push(getDirection(option[1]))

            nextStateCost = currStateCost + option[2]
            # priority queue is sorted based on the cost + heuristic.
            pQ.push((nextState, nextStatePQ, nextStateCost), nextStateCost + heuristic(nextState, problem))
        JUMBO_POINTER = pQ.pop()
    
    qList = JUMBO_POINTER[1].list
    return qList[::-1]

def getDirection(inpStr):
    if inpStr == "North":
        return Directions.NORTH
    elif inpStr == "East":
        return Directions.EAST
    elif inpStr == "South":
        return Directions.SOUTH
    elif inpStr == "West":
        return Directions.WEST
    else:
        return inpStr

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
