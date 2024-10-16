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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

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

        successorGameState = currentGameState.generatePacmanSuccessor(action)
        currentFood = currentGameState.getFood()
        newPos = successorGameState.getPacmanPosition()
        ghostPositions = successorGameState.getGhostPositions()

        # Iterate through each possible ghost position.
        for pos in ghostPositions:

            # Check if a ghost is at the new position or adjacent to it using manhattan distance. Don't move.
            if pos == newPos or util.manhattanDistance(pos, newPos) == 1:
                return(float('-inf'))

            # Check if there is food in the new position. Consume the dot if no ghost is nearby.
            elif currentFood[newPos[0]][newPos[1]]:
                return float('inf')
        
        # Estimate the next food position for the agent.
        minDist = float('inf')
        foodList = currentFood.asList()
        for food in foodList:
            dist = util.manhattanDistance(food, newPos)
            if dist < minDist:
                minDist = dist
        
        # Return a state that is closest to a food.
        return -minDist

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

        # Retrieve all legal actions as well as set a default maxRes and maxAction.
        legalActions = gameState.getLegalActions(0)
        maxRes = float('-inf')
        maxAction = None

        # Iterate through all legal actions to find the max score.
        for action in legalActions:
            # Generate the successor state after Pacman's action.
            successor = gameState.generateSuccessor(0, action)

            # Calculate the minimum value for the successor state, considering the next agent (ghosts).
            currentRes = self.minValue(successor, 0, 1)

            # Update maxAction if needed.
            if currentRes > maxRes:
                maxRes = currentRes
                maxAction = action
        return maxAction

    def minValue(self, gameState, currDepth, currAgent):
        """
          Returns the minimum value for a given game state and current agent.
        """

        # Check if the game is over or we've reached the maximum depth.
        if gameState.isWin() or gameState.isLose() or currDepth == self.depth:
            return self.evaluationFunction(gameState)

        legalActions = gameState.getLegalActions(currAgent)
        successors = [gameState.generateSuccessor(currAgent, action) for action in legalActions]
        agents = gameState.getNumAgents()

        if currAgent < agents - 1:
            # There are still some ghosts to choose their moves, so increase the agent index and call minValue again.
            return min([self.minValue(s, currDepth, currAgent + 1) for s in successors])
        else:
            # Depth is increased when it is max's turn.
            return min([self.maxValue(s, currDepth + 1) for s in successors])
    
    def maxValue(self, gameState, currDepth):
        """
        Returns the maximum value for a given game state for Pacman.
        """

        # Check if the game is over or we've reached the maximum depth.
        if gameState.isWin() or gameState.isLose() or currDepth == self.depth:
            return self.evaluationFunction(gameState)

        legalActions = gameState.getLegalActions(0)
        successors = [gameState.generateSuccessor(0, action) for action in legalActions]

        # Pacman plays next, we compute the maximum value of the successor states.
        return max([self.minValue(s, currDepth, 1) for s in successors])

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

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
        util.raiseNotDefined()

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

