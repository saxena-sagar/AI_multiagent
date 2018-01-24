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
from decimal import _Infinity

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
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        
        "*** YOUR CODE HERE ***"
        distance_score = []
        food_locations = newFood.asList()
        utility = 0
        
        #When stop action is triggered no action is to be taken by the INteligence of pacnman so it doesnt moves
        if action == 'Stop':
            return -99999
        
        #if ghosts position and pacmans position coincides
        for ghosts in newGhostStates:
               if ghosts.getPosition() == newPos and ghosts.scaredTimer is 0:
                                                return -99999

        #if there is any food available the nearest food is searched for
        if newFood.count() > 0:
            distToFoodFromPacman = min([manhattanDistance(foodPellets,newPos) for foodPellets in newFood.asList()])
            distToGhostFromPacman = max([manhattanDistance(ghostPos.getPosition(),newPos) for ghostPos in newGhostStates]) 
        else:
            distToFoodFromPacman = 0
            distToGhostFromPacman = 999999#assumingn the ghost ot be as far as possible from the pacman
        
        #Adding weights for the correct path to be chosen by pacman and to motivate this movement its been rewarded by a weight of 1000.          
        #The pacman searches for nearest fooditem,on reaching the food item the utility is reset to the next nearest food items value and this way its always motivated to reach the nearest food item and be rewarded
        #The utility value is made to decrease(pacman penalised) if pacman moves closer to the ghost 
        utility = - distToFoodFromPacman - newFood.count()*1000 + distToGhostFromPacman
            
        return utility

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
        #Setting the bestValue to be tending toward negative infinity as any value better would have pacman motivaated
        bestAction = None
        bestValue = - 999999
        #for the first pass ,i.e,from root node leaf node.THis is the phases for building up the game tree
        for action in gameState.getLegalActions():
            value = self.minimax(gameState.generateSuccessor(0, action),self.depth,0)
            if bestValue < value:
                bestValue = value#taking the smallest value as best value and setting that as base condition to compare with other path costs
                bestAction = action
            
        return bestAction
       
        #util.raiseNotDefined()
    
    def minimax(self,gameState, remainingDepth, maximisingPLayer):#maximisingpLayer a flag value which 
        #detemrines number of agents(ghosts) in the game with pacman having 0 value also to execute
        #Max function(for pacman) or min(for ghosts)
        
        maximisingPLayer += 1
        if maximisingPLayer == gameState.getNumAgents():#if total number of agents are taken into consideration and not more
            maximisingPLayer = 0 #initialising for pacman
            remainingDepth -= 1 #decreasing the depth as one level gets covered in the the game tree
            
        if remainingDepth == 0 or gameState.isWin() or gameState.isLose():#base condition for the recursion to halt
            return self.evaluationFunction(gameState)    
            
        if maximisingPLayer == 0:
            upgradedValue = self.Maximum(gameState,remainingDepth, maximisingPLayer)#If pacman moves closer to food its awarded or its maximized
        else:
            upgradedValue = self.Minimum(gameState,remainingDepth, maximisingPLayer)#for agents or ghosts which act as minimizer reducing pacmans score
        
        return upgradedValue        
        
    def Maximum(self,gameState,remainingDepth, maximisingPLayer):
        bestValue = - 999999
        for action in gameState.getLegalActions(maximisingPLayer):#legal actions of the pacman
            value = self.minimax(gameState.generateSuccessor(maximisingPLayer, action),remainingDepth,maximisingPLayer)
            bestValue = max(bestValue,value)
        return bestValue         

    def Minimum(self,gameState,remainingDepth, maximisingPLayer):
        worstValue = 999999
        for action in gameState.getLegalActions(maximisingPLayer):
            value = self.minimax(gameState.generateSuccessor(maximisingPLayer, action),remainingDepth,maximisingPLayer)
            worstValue = min(worstValue,value)
        return worstValue 
  

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        #util.raiseNotDefined()
         #Setting the bestValue to be tending toward negative infinity as any value better would have pacman motivaated      
        bestAction = None
        alpha = -999999
        beta = 999999
        bestValue = -999999
        #for the first pass ,i.e,from root node leaf node.THis is the phases for building up the game tree
        for action in gameState.getLegalActions():
                value = self.minimax(gameState.generateSuccessor(0, action),self.depth,0, alpha, beta)
                if bestValue < value:
                    bestValue = value#taking the smallest value as best value and setting that as base condition to compare with other path costs
                    bestAction = action#choosing the best action or move for the pacman   
                alpha = max(alpha,bestValue)           
        return bestAction
       
        #util.raiseNotDefined()
    
    def minimax(self,gameState, remainingDepth, maximisingPLayer, alpha, beta):#maximisingpLayer a flag value which 
        #detemrines number of agents(ghosts) in the game with pacman having 0 value also to execute
        #Max function(for pacman) or min(for ghosts)
        
        maximisingPLayer += 1
        if maximisingPLayer == gameState.getNumAgents():#if total number of agents are taken into consideration and not more
            maximisingPLayer = 0 #initialising for pacman
            remainingDepth -= 1 #decreasing the depth as one level gets covered in the the game tree
            
        if remainingDepth == 0 or gameState.isWin() or gameState.isLose():#base condition for the recursion to halt
            return self.evaluationFunction(gameState)    
            
        if maximisingPLayer == 0:
            upgradedValue = self.Maximum(gameState, remainingDepth, maximisingPLayer, alpha, beta)#If pacman moves closer to food its awarded or its maximized
        else:
            upgradedValue = self.Minimum(gameState, remainingDepth, maximisingPLayer, alpha, beta)#for agents or ghosts which act as minimizer reducing pacmans score
        
        return upgradedValue        
        
    def Maximum(self, gameState, remainingDepth, maximisingPLayer, alpha, beta):
        
        bestValue = - 999999
        #alpha = -999999
        #bestValue = - 999999
        for action in gameState.getLegalActions(maximisingPLayer):#legal actions of the pacman
            value = self.minimax(gameState.generateSuccessor(maximisingPLayer, action), remainingDepth, maximisingPLayer,alpha, beta)
            bestValue = max(bestValue,value)
            if bestValue > beta :#condition check for pruning the invalid paths depengin on beta value for maximiszer
                 return bestValue 
            alpha = max(alpha,bestValue)
   
        return bestValue         

    def Minimum(self, gameState,remainingDepth, maximisingPLayer, alpha, beta):
        worstValue = 999999
        #beta = 999999
        for action in gameState.getLegalActions(maximisingPLayer):
            value = self.minimax(gameState.generateSuccessor(maximisingPLayer, action), remainingDepth, maximisingPLayer, alpha, beta)
            worstValue = min(worstValue,value)
            if worstValue < alpha :#condition check for pruning the invalid paths depending on alpha value for minimizer
                return worstValue 
            beta = min(beta,worstValue)
          
        return worstValue

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
        #Setting the bestValue to be tending toward negative infinity as any value better would have pacman motivaated
        bestAction = None
        bestValue = - 999999
        
        #for the first pass ,i.e,from root node leaf node.THis is the phases for building up the game tree
        for action in gameState.getLegalActions():
            value = self.expectimax(gameState.generateSuccessor(0, action),self.depth,0)
            if bestValue < value:
                bestValue = value#taking the smallest value as best value and setting that as base condition to compare with other path costs
                bestAction = action
            
        return bestAction
       
        #util.raiseNotDefined()
    
    def expectimax(self,gameState, remainingDepth, maximisingPLayer):#maximisingpLayer a flag value which 
        #detemrines number of agents(ghosts) in the game with pacman having 0 value also to execute
        #Max function(for pacman) or average(for ghosts)        
        maximisingPLayer += 1
        if maximisingPLayer == gameState.getNumAgents():#if total number of agents are taken into consideration and not more
            maximisingPLayer = 0 #initialising for pacman
            remainingDepth -= 1 #decreasing the depth as one level gets covered in the the game tree
            
        if remainingDepth == 0 or gameState.isWin() or gameState.isLose():#base condition for the recursion to halt
            return self.evaluationFunction(gameState)    
            
        if maximisingPLayer == 0:
            upgradedValue = self.Maximum(gameState,remainingDepth, maximisingPLayer)#If pacman moves closer to food its awarded or its maximized
        else:
            upgradedValue = self.Average_case(gameState,remainingDepth, maximisingPLayer)#for averaging the outcomes and getting the probabilities
        
        return upgradedValue        
        
    def Maximum(self,gameState,remainingDepth, maximisingPLayer):
        bestValue = - 999999
        for action in gameState.getLegalActions(maximisingPLayer):#legal actions of the pacman
            value = self.expectimax(gameState.generateSuccessor(maximisingPLayer, action),remainingDepth,maximisingPLayer)
            bestValue = max(bestValue,value)
        return bestValue         

    def Average_case(self,gameState,remainingDepth, maximisingPLayer):
        worstValue = 0
        action_count = len(gameState.getLegalActions(maximisingPLayer))
        for action in gameState.getLegalActions(maximisingPLayer):
            value = self.expectimax(gameState.generateSuccessor(maximisingPLayer, action),remainingDepth,maximisingPLayer)
            worstValue += value/action_count#getting average of the probable paths
        
        return worstValue
  
        

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"


    distToFoodFromPacman = 1#Assuming the pacman to be unit distance away from the food at the very onset of game
    distToGhostFromPacman = 999999
    foodList = currentGameState.getFood().asList()
    ghostStates = currentGameState.getGhostStates()
    capsuleList = currentGameState.getCapsules()
    ghostscared = 0
    pacmanPos = currentGameState.getPacmanPosition()
        

    for ghosts in ghostStates:
        if ghosts.scaredTimer is 0:
            ghostscared += 1#the scared ghost to be used in utitity to maximise the output
            continue
            
    if len(foodList) > 0:
        distToFoodFromPacman = min([manhattanDistance(foodPellets,pacmanPos) for foodPellets in foodList])
        distToGhostFromPacman = min([manhattanDistance(ghostPos.getPosition(),pacmanPos) for ghostPos in ghostStates]) 
    #Doing hit and trial to get the valid combination for the maximal utility functiom    
    utility = - 1/distToFoodFromPacman + currentGameState.getScore() - len(foodList) + distToGhostFromPacman - 20*ghostscared - len(capsuleList)*100
            
    return utility
    
    
    
# Abbreviation
better = betterEvaluationFunction

