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
    """Search the deepest nodes in the search tree first."""

    # Create the initial state and path.
    state = problem.getStartState()
    path = []

    # If the starting point is the goal, return the path.
    if problem.isGoalState(state):
        return path

    # Create a Stack and push the initial start state.
    frontier = util.Stack()
    frontier.push((state, path))

    # Create a set of visited states.
    visited = set()

    # Continuosly search for the next possible successor until a goal state is found.
    while not frontier.isEmpty():
        state, path = frontier.pop()

        # If the current state is the goal, return the path.
        if problem.isGoalState(state):
            return path

        # Add the current state to the set.
        visited.add(state)

        # Check for each possible successor given the current state.
        for successor in problem.getSuccessors(state):

            # Set state and path for the current successor.
            successor_state, successor_path = successor[0], (path + [successor[1]])

            # If the successor has not been visited, push it to the frontier.
            if successor_state not in visited:
                frontier.push((successor_state, successor_path))

    # Return an empty path if no goal state is found.
    return []

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""

    # Create the initial state and path.
    state = problem.getStartState()
    path = []

    # If the starting point is the goal, return the path.
    if problem.isGoalState(state):
        return path

    # Create a Queue and push the initial start state.
    frontier = util.Queue()
    frontier.push((state, path))

    # Create a set of visited states.
    visited = set()

    # Continuosly search for the next possible successor until a goal state is found.
    while not frontier.isEmpty():
        state, path = frontier.pop()

        # If the current state is the goal, return the path.
        if problem.isGoalState(state):
            return path

        # Add the current state to the set.
        visited.add(state)

        # Add every state in the frontier/queue to a list.
        states_in_queue = []
        for s in frontier.list:
            states_in_queue.append(s[0])

        # Check for each possible successor given the current state.
        for successor in problem.getSuccessors(state):

            # Set state and path for the current successor.
            successor_state, successor_path = successor[0], (path + [successor[1]])

            # If the successor has not been visited, push it to the frontier.
            if successor_state not in visited and successor_state not in states_in_queue:
                frontier.push((successor_state, successor_path))

    # Return an empty path if no goal state is found.
    return []

def uniformCostSearch(problem):
    """Search the node of least total cost first."""

    # Create the initial state and path.
    state = problem.getStartState()
    path = []

    # If the starting point is the goal, return the path.
    if problem.isGoalState(state):
        return path

    # Create a PriorityQueue and push the initial start state.
    frontier = util.PriorityQueue()
    frontier.push((state, path), 0)

    # Create a set of visited states.
    visited = set()

    # Continuosly search for the next possible successor until a goal state is found.
    while not frontier.isEmpty():
        state, path = frontier.pop()

        # If the current state is the goal, return the path.
        if problem.isGoalState(state):
            return path

        # Add the current state to the set.
        visited.add(state)

        # Add every state in the frontier/priority queue to a list.
        states_in_priority_queue = []
        for s in frontier.heap:
            states_in_priority_queue.append(s[2][0])

        # Check for each possible successor given the current state.
        for successor in problem.getSuccessors(state):

            # Set state, path, and cost for the current successor.
            successor_state, successor_path = successor[0], (path + [successor[1]])
            path_cost = problem.getCostOfActions(successor_path)

            # If the successor has not been visited, push it to the frontier.
            if successor_state not in visited and successor_state not in states_in_priority_queue:
                frontier.push((successor_state, successor_path), path_cost)

            # If the state has already been visited, compare and update the costs of its path.
            else:
                # Loop through the PriorityQueue list until the current successor is found inside it.
                for i in range(len(states_in_priority_queue)):
                    if successor_state == states_in_priority_queue[i]:
                        stored_cost = frontier.heap[i][0]

                        # If the current path cost is less, update the tuple and the current successor in the frontier.
                        if path_cost <= stored_cost:
                            frontier.heap[i] = (stored_cost, frontier.heap[i][1] , (successor_state, successor_path) )
                            frontier.update((successor_state, successor_path), path_cost)

    # Return an empty path if no goal state is found.
    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""

    # Create the initial state and path.
    state = problem.getStartState()
    path = []

    # If the starting point is the goal, return the path.
    if problem.isGoalState(state):
        return path

    # Calculate the combined cost and heuristic of the initial state.
    heuristic_cost = problem.getCostOfActions(path) + heuristic(state, problem)

    # Create a PriorityQueue and push the initial start state.
    frontier = util.PriorityQueue()
    frontier.push((state, path), heuristic_cost)

    # Create a set of visited states.
    visited = set()

    # Continuosly search for the next possible successor until a goal state is found.
    while not frontier.isEmpty():
        state, path = frontier.pop()

        # If the current state is the goal, return the path.
        if problem.isGoalState(state):
            return path

        # Add the current state to the set.
        visited.add(state)

        # Add every state in the frontier/priority queue to a list.
        states_in_priority_queue = []
        for s in frontier.heap:
            states_in_priority_queue.append(s[2][0])

        # Check for each possible successor given the current state.
        for successor in problem.getSuccessors(state):

            # Set state and path for the current successor.
            successor_state, successor_path = successor[0], (path + [successor[1]])
            
            # Calculate the combined cost and heuristic of the successor.
            successor_heuristic_cost = problem.getCostOfActions(successor_path) + heuristic(successor_state, problem)

            # If the successor has not been visited, push it to the frontier.
            if successor_state not in visited and successor_state not in states_in_priority_queue:
                frontier.push((successor_state, successor_path), successor_heuristic_cost)

            # If the state has already been visited, compare and update the costs of its path.
            else:
                # Loop through the PriorityQueue list until the current successor is found inside it.
                for i in range(len(states_in_priority_queue)):
                    if successor_state == states_in_priority_queue[i]:
                        stored_cost = frontier.heap[i][0]

                        # If the current path cost is less, update the tuple and the current successor in the frontier.
                        if successor_heuristic_cost <= stored_cost:
                            frontier.heap[i] = (stored_cost, frontier.heap[i][1] , (successor_state, successor_path) )
                            frontier.update((successor_state, successor_path), successor_heuristic_cost)

    # Return an empty path if no goal state is found.
    return []

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
