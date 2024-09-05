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
Pacman agents (in search_agents.py).
"""

from builtins import object
import util

def tiny_maze_search(problem):
    """
    Returns a sequence of moves that solves tiny_maze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tiny_maze.
    """
    from game import Directions

    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depth_first_search(problem):
    "*** YOUR CODE HERE ***"
    # What does this function need to return?
    #     list of actions that reaches the goal
    # 
    # What data is available?
    #     start_state = problem.get_start_state() # returns a string
    # 
    #     problem.is_goal_state(start_state) # returns boolean
    # 
    #     transitions = problem.get_successors(start_state)
    #     transitions[0].state
    #     transitions[0].action
    #     transitions[0].cost
    # 
    #     print(transitions) # would look like the list-of-lists on the next line
    #     [
    #         [ "B", "0:A->B", 1.0, ],
    #         [ "C", "1:A->C", 2.0, ],
    #         [ "D", "2:A->D", 4.0, ],
    #     ]
    # 
    # Example:
    #     start_state = problem.get_start_state()
    #     transitions = problem.get_successors(start_state)
    #     return [  transitions[0].action  ]

    
    frontier = util.Stack() # A stack to expand nodes as deep as possible
    visited = set() # A set to store nodes we have reached

    # Start with intial state and empty path
    frontier.push((problem.get_start_state(), []))

    while not frontier.is_empty():

        # Nodes consist of a state, a path, and a cost (ignored for dfs)
        currentState, path = frontier.pop()

        # Gives the path to the goal 
        if problem.is_goal_state(currentState):
            return path
        
        # Check if the node is already visited
        if currentState not in visited:
            visited.add(currentState)

            # Expand the frontier by getting the successor nodes
            for next_state, action, _ in problem.get_successors(currentState):
                # We haven't reached these nodes so add them to the frontier
                if next_state not in visited:
                    # Updates the next path to take
                    nextPath = path + [action]
                    frontier.push((next_state, nextPath))

    return []

    
    util.raise_not_defined()


def breadth_first_search(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    frontier = util.Queue() # A queue to expand nodes level by level
    reached = set() # A set to store nodes we have reached

    # Start with intial state and empty path
    frontier.push((problem.get_start_state(), []))
    reached.add(problem.get_start_state()) # Need to add the intial state 

    while not frontier.is_empty():
        # Nodes consist of a state, a path, and a cost (ignored for bfs)
        currentState, path = frontier.pop()

        # Gives the path to the goal 
        if problem.is_goal_state(currentState):
            return path

        # Expand the frontier by getting the successor nodes
        for nextState, action, _ in problem.get_successors(currentState):
            # We haven't reached these nodes so add them to the frontier
            if nextState not in reached:
                # Updates the next path to take
                nextPath = path + [action]
                reached.add(nextState)
                frontier.push((nextState, nextPath))

    return []

    util.raise_not_defined()


def uniform_cost_search(problem, heuristic=None):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    initialState = problem.get_start_state()
    frontier = util.PriorityQueue() # Updated by a cost 
    reached = {} # A map to store states and the cost to reach them

    # Push the intial node and intial cost
    frontier.push((initialState, [], 0), 0) 
    # Mark intial state as reached
    reached[initialState] = 0 

    while not frontier.is_empty():
        # Nodes consist of a state, action, and cost
        currentState, currentPath, currentCost = frontier.pop()

        # Gives the path to the goal 
        if problem.is_goal_state(currentState):
            return currentPath
        
        # Expand the frontier by getting the successor nodes
        for nextState, action, actionCost in problem.get_successors(currentState):
            
            # Update the cost of the path
            nextCost = currentCost + actionCost 
            
            # Considers if the next cost is less than the cost stored at the next state
            if nextState not in reached or nextCost < reached[nextState]:
                # Updates the next path to take
                nextPath = currentPath + [action]
                # Mark next state as reached, updates it's cost 
                reached[nextState] = nextCost
                # Gives the frontier the next node and a priority
                frontier.update((nextState, nextPath, nextCost), nextCost)
    
    return []
    
    util.raise_not_defined()


def null_heuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def a_star_search(problem, heuristic=null_heuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    
    # What does this function need to return?
    #     list of actions that reaches the goal
    # 
    # What data is available?
    #     start_state = problem.get_start_state() # returns a string
    # 
    #     problem.is_goal_state(start_state) # returns boolean
    # 
    #     transitions = problem.get_successors(start_state)
    #     transitions[0].state
    #     transitions[0].action
    #     transitions[0].cost
    # 
    #     print(transitions) # would look like the list-of-lists on the next line
    #     [
    #         [ "B", "0:A->B", 1.0, ],
    #         [ "C", "1:A->C", 2.0, ],
    #         [ "D", "2:A->D", 4.0, ],
    #     ]
    # 
    # Example:
    #     start_state = problem.get_start_state()
    #     transitions = problem.get_successors(start_state)
    #     return [  transitions[0].action  ]

    initialState = problem.get_start_state()
    frontier = util.PriorityQueue() # Gives priority to a heuristic
    reached = {} # A map to store states and the cost to reach them

    # Push the intial node and intial cost
    frontier.push((initialState, [], 0), 0) 
    # Mark intial state as reached
    reached[initialState] = 0 

    while not frontier.is_empty():
        # Nodes consist of a state, action, and cost
        currentState, currentPath, currentCost = frontier.pop()

        # Gives the path to the goal 
        if problem.is_goal_state(currentState):
            return currentPath
        
        # Expand the frontier by getting the successor nodes
        for nextState, action, actionCost in problem.get_successors(currentState):
            
            # Update the cost of the path
            nextCost = currentCost + actionCost 
            
            # Considers if the next cost is less than the cost stored at the next state
            if nextState not in reached or nextCost < reached[nextState]:
                # Updates the next path to take
                nextPath = currentPath + [action]
                # Mark next state as reached, updates it's cost 
                reached[nextState] = nextCost
                # Priority queue is now updated with next cost + a heuristic
                priority = nextCost + heuristic(nextState, problem) 
                # Gives the frontier the next node and a priority
                frontier.update((nextState, nextPath, nextCost), priority)
    
# (you can ignore this, although it might be helpful to know about)
# This is effectively an abstract class
# it should give you an idea of what methods will be available on problem-objects
class SearchProblem(object):
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def get_start_state(self):
        """
        Returns the start state for the search problem.
        """
        util.raise_not_defined()

    def is_goal_state(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raise_not_defined()

    def get_successors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, step_cost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'step_cost' is
        the incremental cost of expanding to that successor.
        """
        util.raise_not_defined()

    def get_cost_of_actions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raise_not_defined()

# fallback on a_star_search
for function in [breadth_first_search, depth_first_search, uniform_cost_search, ]:
    try: function(None)
    except util.NotDefined as error: exec(f"{function.__name__} = a_star_search", globals(), globals())
    except: pass

# Abbreviations
bfs   = breadth_first_search
dfs   = depth_first_search
astar = a_star_search
ucs   = uniform_cost_search