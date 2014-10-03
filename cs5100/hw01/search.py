# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called 
by Pacman agents (in searchAgents.py).
"""

import util
from util import Stack
from util import Queue
from util import PriorityQueue

class SearchProblem:
  """
  This class outlines the structure of a search problem, but doesn't implement
  any of the methods (in object-oriented terminology: an abstract class).
  
  You do not need to change anything in this class, ever.
  """
  
  def getStartState(self):
     """
     Returns the start state for the search problem 
     """
     util.raiseNotDefined()
    
  def isGoalState(self, state):
     """
       state: Search state
    
     Returns True if and only if the state is a valid goal state
     """
     util.raiseNotDefined()

  def getSuccessors(self, state):
     """
       state: Search state
     
     For a given state, this should return a list of triples, 
     (successor, action, stepCost), where 'successor' is a 
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental 
     cost of expanding to that successor
     """
     util.raiseNotDefined()

  def getCostOfActions(self, actions):
     """
      actions: A list of actions to take
 
     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
     """
     util.raiseNotDefined()
           

def tinyMazeSearch(problem):
  """
  Returns a sequence of moves that solves tinyMaze.  For any other
  maze, the sequence of moves will be incorrect, so only use this for tinyMaze
  """
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first [p 85].
        
  Your search algorithm needs to return a list of actions that reaches
  the goal.  Make sure to implement a graph search algorithm [Fig. 3.7].
        
  To get started, you might want to try some of these simple commands to
  understand the search problem that is being passed in:
        
  print "Start:", problem.getStartState()
  print "Is the start a goal?", problem.isGoalState(problem.getStartState())
  print "Start's successors:", problem.getSuccessors(problem.getStartState())
  """
  frontier = Stack()  # A helper stack of (state,route_to_state)
  explored_set = set()  # A set of state recording the explored nodes
  
  start = problem.getStartState()
  frontier.push((start,list()))
  
  while not frontier.isEmpty():
   current_node = frontier.pop()
   if problem.isGoalState(current_node[0]): return current_node[1]
   successors = problem.getSuccessors(current_node[0])
   explored_set.add(current_node[0])
   for s in successors:
       if s[0] not in explored_set:
           current_route = list(current_node[1])
           current_route.append(s[1])
           frontier.push((s[0],current_route))
           
  print "No route found!"
  return list()
    

def breadthFirstSearch(problem):
  "Search the shallowest nodes in the search tree first. [p 81]"
  frontier = Queue()  # A helper queue of (state,route_to_state)
  frontier_set = set()
  explored_set = set()  # A set of state recording the explored nodes
  start = problem.getStartState()
  frontier.push((start,list()))
  frontier_set.add(start)
  
  while not frontier.isEmpty():
    current_node = frontier.pop()
    explored_set.add(current_node[0])
    if problem.isGoalState(current_node[0]):return current_node[1]
    successors = problem.getSuccessors(current_node[0])
    for s in successors:
      if s[0] not in explored_set.union(frontier_set):
        current_route = list(current_node[1])
        current_route.append(s[1])
        frontier.push((s[0],current_route))
        frontier_set.add(s[0])
  print "No route found!"
  return list()
      
def uniformCostSearch(problem):
  "Search the node of least total cost first. "
  start = problem.getStartState()
  frontier = PriorityQueue()  # A priority queue of (state,route_to_state,cost)
  frontier_set = set()  #A set recording what's in the frontier
  explored_set = set()  # A set of states recording the explored nodes
  frontier.push((start,list(),0),0)
  frontier_set.add(start)
  solution_node = ((0,0),list(),-1)

  while not frontier.isEmpty():
    current_node = frontier.pop()
    frontier_set.remove(current_node[0])
    if solution_node[2] == -1 or current_node[2] < solution_node[2]:
      if problem.isGoalState(current_node[0]):
        solution_node = current_node
        successors = list()
      else:
        successors = problem.getSuccessors(current_node[0])
      explored_set.add(current_node[0])
      for s in successors:
        if s[0] not in explored_set.union(frontier_set):
          current_route = list(current_node[1])
          current_route.append(s[1])
          frontier.push((s[0],current_route,current_node[2]+s[2]),current_node[2]+s[2])
          frontier_set.add(s[0])
        elif s[0] in frontier_set:
          #retrieve the frontier to see if current_node has lower cost
          found = False
          nodes = list()
          while not found:
            node = frontier.pop()
            if s[0] == node[0]:
              found = True
              if current_node[2]+s[2] < node[2]:
                current_route = list(current_node[1])
                current_route.append(s[1])
                nodes.append((s[0],current_route,current_node[2]+s[2]))
              else:
                nodes.append(node)
            else:
              nodes.append(node)
          for n in nodes:
            frontier.push(n,n[2])
  if solution_node[2] == -1:
    print "No route found!"
  return solution_node[1]

def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."
  start = problem.getStartState()
  frontier = PriorityQueue() # A priority queue of (state,route_to_state,cost)
  explored_set = set()
  frontier_set = set()  #A set recording what's in the frontier
  
  frontier.push((start,list(),0),heuristic(start,problem))
  frontier_set.add(start)
  while not frontier.isEmpty():
    current_node = frontier.pop()
    frontier_set.remove(current_node[0])
    if problem.isGoalState(current_node[0]): return current_node[1]
    explored_set.add(current_node[0])
    successors = problem.getSuccessors(current_node[0])
    for s in successors:
      if s[0] not in explored_set.union(frontier_set):
        current_route = list(current_node[1])
        current_route.append(s[1])
        current_cost = current_node[2]+s[2]
        frontier.push((s[0],current_route,current_cost),current_cost+heuristic(s[0],problem))
        frontier_set.add(s[0])
      elif s[0] in frontier_set:
        #retrieve the frontier to see if current_node has lower cost
        found = False
        nodes = list()
        while not found:
          node = frontier.pop()
          if s[0] == node[0]:
            found = True
            if current_node[2]+s[2] < node[2]:
              current_route = list(current_node[1])
              current_route.append(s[1])
              nodes.append((s[0],current_route,current_node[2]+s[2]))
            else:
              nodes.append(node)
          else:
            nodes.append(node)
        for n in nodes:
          frontier.push(n,n[2]+heuristic(n[0],problem))
  return list()

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
