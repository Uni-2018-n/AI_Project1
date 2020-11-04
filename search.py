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
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    visited = [] #used to store the visited nodes
    fringe = util.Stack() #stack because we are building DFS
    fringe.push(problem.getStartState()) #initialize fringe
    relationships = {} #dictionary to store the relationships with the node and the child so we can back trace the path
    while not fringe.isEmpty():
        node = fringe.pop() #pop it
        if node in visited: #check if we already visited(so we wont do circles)
            continue
        visited.append(node) #if not add it to visited so we wont revisit it
        if problem.isGoalState(node): # check if its the goal
            break #if yes then node found, time to backtrace the path
        for child in problem.getSuccessors(node): # if not we need to get all the successors
            if child[0] not in visited: # that are not into visited
                fringe.push(child[0]) #and add them to the stack so we can run the algorithm with them
                relationships[child[0]] = (node, child[1]) #and finally add the relationship to the dictionary so we have a (more precise) view of who is next to who

    #node == goal
    path = [] #initialize final list
    while node != problem.getStartState(): # now we need to go from the goal to the start state via the relationship dictionary
        path.append(relationships[node][1]) #add the node to the path
        node = relationships[node][0] #and now set as new node the node's child so we can run it as "parent"

    path.reverse() #because we go from goal to start we need to reverse it
    #print(path)
    return path
    #util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    visited = []
    fringe = util.Queue() #same logic but with queue cause we use BFS
    fringe.push(problem.getStartState())
    relationships = {}
    while not fringe.isEmpty():
        node = fringe.pop()
        if node in visited:
            continue
        visited.append(node)
        if problem.isGoalState(node):
            break
        for child in problem.getSuccessors(node):
            if child[0] not in visited:
                fringe.push(child[0])
                if child[0] not in relationships.keys(): #added this because sometimes the "next step" has a successor same as the prev step
                    relationships[child[0]] = (node, child[1])

    #node == goal
    path = []
    while node != problem.getStartState():
        path.append(relationships[node][1])
        node = relationships[node][0]

    path.reverse()
    #print(path)
    return path
    #util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    visited = []
    fringe = util.PriorityQueue()
    fringe.push(problem.getStartState(), 0)
    relationships = {}
    relationships[problem.getStartState()] = (problem.getStartState(), problem.getStartState(), 0)
    while not fringe.isEmpty():
        node = fringe.pop()
        if node in visited:
            continue
        visited.append(node)
        if problem.isGoalState(node):
            break
        for child in problem.getSuccessors(node):
            if child[0] not in visited:
                fringe.push(child[0], relationships[node][2] + child[2])
                if child[0] not in relationships.keys():
                    relationships[child[0]] = (node, child[1], relationships[node][2]+child[2])
                else:
                    if relationships[child[0]][2] > relationships[node][2]+child[2]:
                        relationships[child[0]] = (node, child[1], relationships[node][2]+child[2])
    #node == goal
    path = []
    while node != problem.getStartState():
        path.append(relationships[node][1])
        node = relationships[node][0]

    path.reverse()
    #print(path)
    return path
    #util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    visited = []
    fringe = util.PriorityQueue()
    fringe.push(problem.getStartState(), heuristic(problem.getStartState(), problem))
    relationships = {}
    relationships[problem.getStartState()] = (problem.getStartState(), problem.getStartState(), heuristic(problem.getStartState(), problem))
    while not fringe.isEmpty():
        node = fringe.pop()
        if node in visited:
            continue
        visited.append(node)
        if problem.isGoalState(node):
            break
        for child in problem.getSuccessors(node):
            if child[0] not in visited:
                fringe.push(child[0], relationships[node][2] + child[2] + heuristic(child[0], problem))
                if child[0] not in relationships.keys():
                    relationships[child[0]] = (node, child[1], relationships[node][2]+child[2])
                else:
                    if relationships[child[0]][2] > relationships[node][2]+child[2]:
                        relationships[child[0]] = (node, child[1], relationships[node][2]+child[2])
    #node == goal
    path = []
    while node != problem.getStartState():
        path.append(relationships[node][1])
        node = relationships[node][0]

    path.reverse()
    #print(path)
    return path
    #util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
