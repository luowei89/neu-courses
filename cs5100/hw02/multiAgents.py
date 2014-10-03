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
    remaining food (oldFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.
    
    Print out these variables to see what you're getting, then combine them
    to create a masterful evaluation function.
    """
    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    oldFood = currentGameState.getFood()
    newGhostStates = successorGameState.getGhostStates() 
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    
    "*** YOUR CODE HERE ***"
    value = 0
    
    scared_ghosts, ghosts = list(), list()
    for ghostState in newGhostStates:
        if ghostState.scaredTimer > 2:
            scared_ghosts.append(ghostState.getPosition())
        else:
            ghosts.append(ghostState.getPosition())

    ghost_distances = [manhattanDistance(g, newPos) for g in ghosts]
    # two successors' distance is at most 2
    for gd in ghost_distances:
      if gd < 2: value -= 4 - gd
    
    food_list = oldFood.asList() + currentGameState.getCapsules() + scared_ghosts
    
    food_distances = [manhattanDistance(f, newPos) for f in food_list]
    if len(food_distances) > 0: value -= min(food_distances)
    
    return value


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
      
      Directions.STOP:
        The stop direction, which is always legal
      
      gameState.generateSuccessor(agentIndex, action): 
        Returns the successor game state after an agent takes an action
      
      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    "*** YOUR CODE HERE ***"
    legalMoves = gameState.getLegalActions(0)
    successorStates = [gameState.generateSuccessor(0, action) for action in legalMoves]
    scores = [self.minmax(state, 1, self.depth) for state in successorStates]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best
    return legalMoves[chosenIndex]

  def minmax(self, gameState, agentIndex, depth):
    num_agents = gameState.getNumAgents()
    if agentIndex == num_agents:
      depth -= 1
      agentIndex = 0
    if depth == 0 and agentIndex == 0:
      return self.evaluationFunction(gameState)
    
    legalMoves = gameState.getLegalActions(agentIndex)
    if len(legalMoves) == 0: return self.evaluationFunction(gameState)
    
    successorStates = [gameState.generateSuccessor(agentIndex, action) for action in legalMoves]
    scores = [self.minmax(state, agentIndex+1, depth) for state in successorStates]
    if agentIndex == 0:
      return max(scores)
    else:
      return min(scores)

class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """
    
  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"
    legalMoves = gameState.getLegalActions(0)
    self.root_values = list()
    bestScore = self.minmax(gameState, 0, self.depth, -999999, 999999)
    scores = self.root_values
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best
    return legalMoves[chosenIndex]
  
  def minmax(self, gameState, agentIndex, depth, alpha, beta):
    num_agents = gameState.getNumAgents()
    if agentIndex == num_agents:
      depth -= 1
      agentIndex = 0
    if depth == 0 and agentIndex == 0:
      return self.evaluationFunction(gameState)
    legalMoves = gameState.getLegalActions(agentIndex)
    if len(legalMoves) == 0: return self.evaluationFunction(gameState)
    #max-player
    if agentIndex == 0:
      value = -999999
      for action in legalMoves:
        state = gameState.generateSuccessor(agentIndex, action)
        successor_value = self.minmax(state, agentIndex+1, depth, alpha, beta)
        if depth == self.depth: self.root_values.append(successor_value)
        value = max(value, successor_value)
        if value > beta: return value
        alpha = max(alpha, value)
      return value
    #min-player
    else:
      value = 999999
      for action in legalMoves:
        state = gameState.generateSuccessor(agentIndex, action)
        value = min(value, self.minmax(state, agentIndex+1, depth, alpha, beta))
        if value < alpha: return value
        beta = min(beta, value)
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
    legalMoves = gameState.getLegalActions(0)
    successorStates = [gameState.generateSuccessor(0, action) for action in legalMoves]
    scores = [self.expmax(state, 1, self.depth) for state in successorStates]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best
    return legalMoves[chosenIndex]
  
  def expmax(self, gameState, agentIndex, depth):
    num_agents = gameState.getNumAgents()
    if agentIndex == num_agents:
      depth -= 1
      agentIndex = 0
    if depth == 0 and agentIndex == 0:
      return self.evaluationFunction(gameState)
    
    legalMoves = gameState.getLegalActions(agentIndex)
    if len(legalMoves) == 0: return self.evaluationFunction(gameState)
    
    successorStates = [gameState.generateSuccessor(agentIndex, action) for action in legalMoves]
    scores = [self.expmax(state, agentIndex+1, depth) for state in successorStates]
    if agentIndex == 0:
      return max(scores)
    else:
      return sum(scores)/len(scores)


def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).
    
    DESCRIPTION: <write something here so we know what you did>
  """
  "*** YOUR CODE HERE ***"
  if currentGameState.isWin():
    return float("inf")
  if currentGameState.isLose():
    return - float("inf")
  score = currentGameState.getScore()
  pacman_pos = currentGameState.getPacmanPosition()
  foods = currentGameState.getFood().asList()
  capsules = currentGameState.getCapsules()
  ghostStates = currentGameState.getGhostStates()

  scared_ghosts, ghosts = list(), list()
  for ghostState in ghostStates:
    if ghostState.scaredTimer > 1:
      scared_ghosts.append((ghostState.getPosition(),ghostState.scaredTimer))
    else:
      ghosts.append(ghostState.getPosition())
  
  ghost_distances = [manhattanDistance(g, pacman_pos) for g in ghosts]
  ghost_value = 0 #no ghost
  for gd in ghost_distances:
    if gd == 0: ghost_value -= 4
    if gd == 1: ghost_value -= 2

  food_distances = [manhattanDistance(f, pacman_pos) for f in foods]
  nearest_food = 0 #no food
  if len(food_distances) > 0: nearest_food = min(food_distances)
  food_value = - nearest_food

  capsule_value = - 20 * len(capsules)

  s_ghost_distances = {manhattanDistance(g[0], pacman_pos):g[1] for g in scared_ghosts}
  nearest_s_ghost = 0 #no scared ghost
  s_ghost_value = 0
  for sgd in s_ghost_distances:
    if sgd == 0: s_ghost_value += 2
    if sgd == 1: s_ghost_value += 1
  value = score + ghost_value + food_value + capsule_value + s_ghost_value
  return value

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """
    
  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.
      
      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

