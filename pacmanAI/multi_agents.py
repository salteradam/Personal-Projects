from __future__ import print_function

# multi_agents.py
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


from builtins import range
from util import manhattan_distance
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


    def get_action(self, game_state):
        """
        You do not need to change this method, but you're welcome to.

        get_action chooses among the best options according to the evaluation function.

        Just like in the previous project, get_action takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legal_moves = game_state.get_legal_actions()

        # Choose one of the best actions
        scores = [self.evaluation_function(game_state, action) for action in legal_moves]
        best_score = max(scores)
        best_indices = [index for index in range(len(scores)) if scores[index] == best_score]
        chosen_index = random.choice(best_indices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legal_moves[chosen_index]

    def evaluation_function(self, current_game_state, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (new_food) and Pacman position after moving (new_pos).
        new_scared_times holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successor_game_state = current_game_state.generate_pacman_successor(action)
        new_pos = successor_game_state.get_pacman_position()
        new_food = successor_game_state.get_food()
        new_ghost_states = successor_game_state.get_ghost_states()
        new_scared_times = [ghost_state.scared_timer for ghost_state in new_ghost_states]

        "*** YOUR CODE HERE ***"
        # Intialize a base score
        score = current_game_state.get_score()

        # Calculate the distance from Pac-Man to each piece of food
        # Find the minimum distance to food
        # Calculate a score
        distanceToFood = []
        foodList = new_food.as_list()
        for food in foodList:
          distances = manhattan_distance(new_pos, food)
          distanceToFood.append(distances)
        if distanceToFood: # if list isn't empty, get the min distance and calculate the score
          minDistanceToFood = min(distanceToFood)
          score += 1.0 * (1 / (minDistanceToFood + 1))
        else: # for when list is empty to avoid - ValueError: min() arg is an empty sequence
          minDistanceToFood = 0
          score += 100 # big incentive for grabbing food

        # Calculate the distance from Pac-Man to each ghost
        # If a ghost is not scared, penalty for being too close
        # If a ghost is scared, encourage Pac-Man to chase it
        for i, ghost in enumerate(new_ghost_states):
          ghostPosition = ghost.get_position()
          scaredTimer = new_scared_times[i]
          distanceFromGhost = manhattan_distance(new_pos, ghostPosition)
          if scaredTimer == 0 and distanceFromGhost < 10:
            score -= 6 * (1.0 / (distanceFromGhost + 1))
          if scaredTimer > 0 and distanceFromGhost < 10:
            score += 6 * (1.0 / (distanceFromGhost + 1))

        # Get a remaining food count
        # The fewer the food, the closer to completion 
        remainingFood = len(foodList)
        score += max(100 - remainingFood, 0) 

        # Get position of capsules from successor game state
        capsulePosition = successor_game_state.get_capsules() 
        capsuleDistances = [] # Stores capsules

        # Loop through the capsules, get the distance from Pacman to capsules
        for capsule in capsulePosition:
          distanceToCapsule = manhattan_distance(new_pos, capsule)
          capsuleDistances.append(distanceToCapsule)
        
        # If theres are capsules, find the max distance to it and increase score
        if capsuleDistances:
          maxDistanceToCapsule = max(capsuleDistances)
          score += 2.0 * (1 / (maxDistanceToCapsule + 1))
        # No capsules left (we are at the capsule), high score for grabbing the capsule
        else:
          maxDistanceToCapsule = 0
          score += 200

        # Return a final score 
        return score

def score_evaluation_function(current_game_state):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return current_game_state.get_score()

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

    def __init__(self, eval_fn = 'score_evaluation_function', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluation_function = util.lookup(eval_fn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def get_action(self, game_state):
      """
        Returns the minimax action from the current game_state using self.depth
        and self.evaluation_function.

        Here are some method calls that might be useful when implementing minimax.

        game_state.get_legal_actions(agent_index):
          Returns a list of legal actions for an agent
          agent_index=0 means Pacman, ghosts are >= 1

        game_state.generate_successor(agent_index, action):
          Returns the successor game state after an agent takes an action

        game_state.get_num_agents():
          Returns the total number of agents in the game
      """
      "*** YOUR CODE HERE ***"
      # start the recursion 
      value, move = self.max_value(game_state, self.depth, 0)
      return move  

    def max_value(self, game_state, depth, agent_index):
      # check for terminal state
      if depth == 0 or game_state.is_win() or game_state.is_lose():
        return self.evaluation_function(game_state), None
      
      highScore = float("-inf")
      bestAction = None

      # loop through all legal actions
      for action in game_state.get_legal_actions(agent_index):

        # for each action generate successor state
        successorState = game_state.generate_successor(agent_index, action)

        # recursively calculate the score using min-value for next agent
        currScore, move = self.min_value(successorState, depth, 1)

        # keep track of highest score
        if currScore > highScore:
          highScore, bestAction = currScore, action

      # return highest score and 
      return highScore, bestAction
            
    def min_value(self, game_state, depth, agent_index):
      # check for terminal state
      if game_state.is_win() or game_state.is_lose():
        return self.evaluation_function(game_state), None
          
      lowScore = float("inf")
      bestAction = None

      # loop through all legal actions
      for action in game_state.get_legal_actions(agent_index):
        # for each action generate successor state
        successorState = game_state.generate_successor(agent_index, action)

        # determine if it's the last ghost's turn:
        # if so, call max-value for Pac-Mans next move
        if agent_index == game_state.get_num_agents() - 1:
          currScore, move = self.max_value(successorState, depth - 1, 0)

        # if not, recursively call min_value for the next ghost
        else:
          currScore, move = self.min_value(successorState, depth, agent_index + 1)

        # keep track of lowest score
        if currScore < lowScore:
          lowScore, bestAction = currScore, action

      # return lowest score
      return lowScore, bestAction

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def get_action(self, game_state):
      """
        Returns the minimax action using self.depth and self.evaluation_function
      """
      "*** YOUR CODE HERE ***"
      # Initialize alpha and beta
      alpha = float("-inf")
      beta = float("inf")
      
      # Root evaluation, start the recursion
      bestAction = None
      highestValue = float("-inf")
      value = float("-inf")
      
      # iterate over all possible actions (successors)
      for action in game_state.get_legal_actions(self.index): # current agents index
        successorState = game_state.generate_successor(self.index, action)
        value = self.min_value(successorState, self.depth, 1, alpha, beta) # Pac-Mans turn, so go to next agent_index

        # if value is greater than highestValue, update the highestValue and bestAction, alpha is the max of best_value or alpha
        if value > highestValue:
          highestValue = value
          bestAction = action
          alpha = max(alpha, highestValue)

      return bestAction 

      
    # max-value function
    def max_value(self, game_state, depth, agent_index, alpha, beta):
      if depth == 0 or game_state.is_win() or game_state.is_lose():
        return self.evaluation_function(game_state)
      value = float("-inf")

      # iterate over all possible actions (successors)
      for action in game_state.get_legal_actions(agent_index): 
        successorState = game_state.generate_successor(agent_index, action)

        # call min-value function on each successor, passing current alpha and beta values
        value = max(value, self.min_value(successorState, depth, 1, alpha, beta)) 

        # if returned value is greater than beta, prune the remaining successor and return the value
        if value > beta: 
          return value
        
        # otherwise, update alpha to the maximum of its current value and the returned value
        alpha = max(alpha, value)

      return value
        
    # min-value function
    def min_value(self, game_state, depth, agent_index, alpha, beta):
      if game_state.is_win() or game_state.is_lose():
        return self.evaluation_function(game_state)
      value = float("inf")

      # iterate over all possible actions (successors)
      for action in game_state.get_legal_actions(agent_index): 
        successorState = game_state.generate_successor(agent_index, action)

        # call the max-value function on each successor, passing the current alpha and beta values
        if agent_index == game_state.get_num_agents() - 1:
          value = min(value, self.max_value(successorState, depth - 1, 0, alpha, beta))
        else:
          value = min(value, self.min_value(successorState, depth, agent_index + 1, alpha, beta)) 

        # if returned value is less than alpha, prune the remaining successors and return the value
        if value < alpha:
          return value
        
        # otherwise update beta to the minimum of its current value and the returned value
        beta = min(beta, value)

      return value

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def get_action(self, game_state):
        """
          Returns the expectimax action using self.depth and self.evaluation_function

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        # Root case, starts the recursion
        # Need to get the best action by getting the best expected value from all legal actions (successors)
        bestAction = None
        highestValue = float("-inf")

        for action in game_state.get_legal_actions(self.index):
          successorState = game_state.generate_successor(self.index, action)
          value = self.expected_value(successorState, self.depth, 1)

          if value > highestValue:
            highestValue = value
            bestAction = action 

        return bestAction
    
    # Same max_value function from minimax but returns a high score, not a high score best move pair
    def max_value(self, game_state, depth, agent_index):
      if depth == 0 or game_state.is_win() or game_state.is_lose():
        return self.evaluation_function(game_state)
      
      bestMove = None
      highScore = float("-inf")

      for action in game_state.get_legal_actions(agent_index):

        successorState = game_state.generate_successor(agent_index, action)
        
        # Get the expected value from the ghosts 
        currScore = self.expected_value(successorState, depth, 1)

        if currScore > highScore:
          highScore = currScore
        
      return highScore

    def expected_value(self, game_state, depth, agent_index):

      # check if game is terminal state
      if game_state.is_win() or game_state.is_lose():
        return self.evaluation_function(game_state)

      # intialize varaiables to store a sum of scores and number of actions
      sumOfScores = 0
      numberOfAgents = game_state.get_num_agents()

      # iterate over legal actions
      for action in game_state.get_legal_actions(agent_index):

        # generate successors for current action
        successorState = game_state.generate_successor(agent_index, action)

        # check if current agent is the last ghost
        # sum up the scores
        if agent_index == numberOfAgents - 1:
          # accumulate the returned score
          sumOfScores += self.max_value(successorState, depth - 1, 0)
      
        # if not last ghost, call expected_value on next ghost
        # sum up the scores
        else:
          # accumulate the returned score
          sumOfScores += self.expected_value(successorState, depth, agent_index + 1)
      
        # calculate expected value (sum of scores / number of agents)
        expectedValue = float(sumOfScores) / float(numberOfAgents)
      
      return expectedValue
    


def better_evaluation_function(current_game_state):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: 
      Using current_game_state we can access Pacman's position (get_pacman_position()),
      ghost states (get_ghost_states()), location of food (get_food()), scared times for ghosts (scared_timer),
      and capsule positions so we can eat ghosts (get_capsules())

      The main idea behind this algorithm is to get scores based on how close food is, how close ghosts are,
      how much food is remaining, and how close capsules are.

      By using manhattan distances of Pacman's current_game_state we can calculate the distances to food, ghosts,
      and capsules. Based on these distances we can assign different scores for where we would like Pacman to
      go from his current state. More on this below. 

      When Pacman is close to food we use a weight of 1 and add it to the score. While collecting all food is 
      how Pacman wins, we don't want him to focus soley on that as there are other ways to increase the game score.
      When he is at a food position we give him a major score bonus so he will eat it.

      When Pacman is close to a ghost, we want him to run away so he will not lose the game. We decrease his score 
      by a weight of 6.6 so he will run away. However, if a capsule is eaten, ghosts become scared so we increase
      his score by a weight of 6.6 so he will eat the ghosts, increasing the game score, more on this shortly.

      Pacman was running into issues getting remaining food when ghosts where on the opposite sides. To counter 
      this, he will recieve an increase to his score based on food amounts decreasing. We do this by subtracting
      the remaining count of food from 100, so as less food is available, his score will increase, so he will
      gravitate towards it.

      In order to actually eat ghosts, Pacman first needs to eat a capsule. We use an a weight of 2, which is higher
      than grabbing food, as eating ghosts can give him massive bonuses to the games score.
    """
    "*** YOUR CODE HERE ***"
    score = current_game_state.get_score()

    # Current states of Pacman, ghosts, food, and capsules
    pacmanPosition = current_game_state.get_pacman_position()
    ghostStates = current_game_state.get_ghost_states()
    foodLocations =  current_game_state.get_food()
    capsulePosition = current_game_state.get_capsules()

    # Allows us to set a timer for how long ghosts are scared
    newScaredTimes = [ghostState.scared_timer for ghostState in ghostStates] 
    
    # Get distances to food, assign a score of 1 (least incentive) to go towards food
    # with a high score for eating food
    foodDistances = []
    foodList = foodLocations.as_list()

    for foodPosition in foodList:
      distanceToFood = manhattan_distance(pacmanPosition, foodPosition)
      foodDistances.append(distanceToFood)

    if foodDistances:
      maxDistanceToFood = max(foodDistances)
      score += 1.0 * (1 / (maxDistanceToFood + 1))
    else:
      maxDistanceToFood = 0
      score += 100

    # Get distances to ghosts, ghosts can either be scared on not scared
    # If a non-scared ghost is nearby, we decrease Pacman's score so he
    # will run away. If a scared ghost is nearby, we increase Pacman's 
    # score so he will eat them. These two conditions are given the highest 
    # scores as getting eaten by ghosts loses the game and eating ghosts 
    # gives us a bonus game score
    for i, ghost in enumerate(ghostStates):
      ghostPosition = ghost.get_position()
      distanceFromGhost = manhattan_distance(pacmanPosition, ghostPosition)
      scaredTimer = newScaredTimes[i]

      if scaredTimer == 0 and distanceFromGhost < 10:
        score -= 6.6 * (1 / (distanceFromGhost + 1))
      elif scaredTimer > 0 and distanceFromGhost < 10:
        score += 6.6 * (1 / (distanceFromGhost + 1))

    # When there is less food on the board we need Pacman to eat the remaining food
    # This stops his score from decreasing too much due to close proximity of ghosts
    foodRemaining = current_game_state.get_num_food()
    score += max(100 - foodRemaining, 0) 

    
    # Eating capsules allows us to eat ghosts, so this is given a higher score
    # than food to make him try and eat food, but not enough score to where 
    # he ignores non-scared ghosts 
    capsuleDistances = []

    for capsule in capsulePosition:
      distanceToCapsule = manhattan_distance(pacmanPosition, capsule)
      capsuleDistances.append(distanceToCapsule)
    
    if capsuleDistances:
      maxDistanceToCapsule = max(capsuleDistances)
      score += 2.0 * (1 / (maxDistanceToCapsule + 1))
    else:
      maxDistanceToCapsule = 0
      score += 200

    return score

# Abbreviation
better = better_evaluation_function

