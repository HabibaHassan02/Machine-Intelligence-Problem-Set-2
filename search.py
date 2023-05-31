from typing import Tuple
from game import HeuristicFunction, Game, S, A
from helpers.utils import NotImplemented

#TODO: Import any modules you want to use
import math

# All search functions take a problem, a state, a heuristic function and the maximum search depth.
# If the maximum search depth is -1, then there should be no depth cutoff (The expansion should not stop before reaching a terminal state) 

# All the search functions should return the expected tree value and the best action to take based on the search results

# This is a simple search function that looks 1-step ahead and returns the action that lead to highest heuristic value.
# This algorithm is bad if the heuristic function is weak. That is why we use minimax search to look ahead for many steps.
def greedy(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    agent = game.get_turn(state)
    
    terminal, values = game.is_terminal(state)
    if terminal: return values[agent], None

    actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]
    value, _, action = max((heuristic(game, state, agent), -index, action) for index, (action , state) in enumerate(actions_states))
    return value, action

# Apply Minimax search and return the game tree value and the best action
# Hint: There may be more than one player, and in all the testcases, it is guaranteed that 
# game.get_turn(state) will return 0 (which means it is the turn of the player). All the other players
# (turn > 0) will be enemies. So for any state "s", if the game.get_turn(s) == 0, it should a max node,
# and if it is > 0, it should be a min node. Also remember that game.is_terminal(s), returns the values
# for all the agents. So to get the value for the player (which acts at the max nodes), you need to
# get values[0].
def minimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #TODO: ADD YOUR CODE HERE
    agent = game.get_turn(state)
    if (agent==0):  #max turn
        terminal,values = game.is_terminal(state) #check if this state is the terminal state or not
        if terminal: 
            return values[0],None #return the value of the termianl state and None as action
        elif max_depth==0:      #we can also stop the game according to a certain depth, so if the max_depth became 0 then stop 
            value=heuristic(game,state,0) #and return the heuristic value of the current state with Nona as action
            return value,None
        value=-math.inf  #becuase this is max turn, then initialise the value with negative infinity
        for action in game.get_actions(state):  #loop over actions of the current state
            child=game.get_successor(state,action)  #get succssors of the current state applying on it the action 
            #call the function recursively on the new state and subtract 1 from the depth because calling the function means that we are going down
            # the tree. Take the returned value and ignore the action returned
            value1,_=minimax(game,child,heuristic,max_depth-1) 
            value1=max(value,value1) #get the maximum of the returned value and the old value and save it in value1
            #if value1=value, that means that no changes have occured, the returned value is the same as the old one (max(9,9)=9 so no change)
            #so do not update the variable to save the first one that got the max value with its action 
            #eg: action A has value 6 and action B has value 6 also, so do not update the value and action because I want the first one who got this value
            #if they are not equal that means that the value returned is the maximum one so update value variable to be used in comaprisons later
            if value1!= value: 
                value=value1
                act=action
        return value,act #by the end of the for loop return the max value with its action
    else:     #min turn
        terminal,values = game.is_terminal(state)
        #the terminal condition and the max_depth is the same as in max turn
        if terminal:  
            return values[0],None
        elif max_depth==0:
            value=heuristic(game,state,0)
            return value,None
        value=math.inf  #because we are in min turn do initialise the value with infinity
        for action in game.get_actions(state): #loop over every action
            child=game.get_successor(state,action) #get the next state according to the current state and tthe action given
            #call the function recursively on the new state and subtract 1 from the depth because calling the function means that we are going down
            # the tree. Take the returned value and ignore the action returned
            value1,_=minimax(game,child,heuristic,max_depth-1)
            #same condition of values as in max turn but here get the min of values
            value1=min(value,value1)
            if value1!= value:
                value=value1
                act=action
        return value,act


# Apply Alpha Beta pruning and return the tree value and the best action
# Hint: Read the hint for minimax.
def alphabeta(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #TODO: ADD YOUR CODE HERE
    value,action=alphabetasearch(game,state,heuristic,-math.inf,math.inf,max_depth) #initialize the value of alpha=-infinity and beta=infinity
    return value,action #return the final value and action 

#hint: non commented parts are the same as minimax, so go back to minimnax and check the comments 
def alphabetasearch(game: Game[S, A], state: S, heuristic: HeuristicFunction, alpha,beta,max_depth: int = -1):
    agent = game.get_turn(state)
    if (agent==0): #max turn
        terminal,values = game.is_terminal(state)
        if terminal: 
            return values[0],None
        elif max_depth==0:
            value=heuristic(game,state,0)
            return value,None
        value=-math.inf
        for action in game.get_actions(state):
            child=game.get_successor(state,action)
            value1,_=alphabetasearch(game,child,heuristic,alpha,beta,max_depth-1)
            value1=max(value,value1)
            if value1!= value: #if the value is updated we need to check on the beta condition 
                value=value1
                act=action
                if value>=beta: #if the updated value is greater than or equal beta return, else update alpha with the max of alpha and value
                    return value,act
                alpha=max(alpha,value)
        return value,act
    else:
        terminal,values = game.is_terminal(state)
        if terminal: 
            return values[0],None
        elif max_depth==0:
            value=heuristic(game,state,0)
            return value,None
        value=math.inf
        for action in game.get_actions(state):
            child=game.get_successor(state,action)
            value1,_=alphabetasearch(game,child,heuristic,alpha,beta,max_depth-1)
            value1=min(value,value1)
            if value1!= value: #if the value is updated check on the alpha condition
                value=value1
                act=action
                if value<=alpha: #if the value is less than or equal alpha then return, else update beta with the min of beta and value
                    return value,act
                beta=min(beta,value)
        return value,act

# Apply Alpha Beta pruning with move ordering and return the tree value and the best action
# Hint: Read the hint for minimax.
def alphabeta_with_move_ordering(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #TODO: ADD YOUR CODE HERE

    #same as alpha beta regardless the ordering condition, so the uncommented parts return to alpha beta and minimax
    value,action=alphabeta_ordering_search(game,state,heuristic,-math.inf,math.inf,max_depth)
    return value,action

def alphabeta_ordering_search(game: Game[S, A], state: S, heuristic: HeuristicFunction, alpha,beta,max_depth: int = -1):
    agent = game.get_turn(state)
    if (agent==0): #max turn
        terminal,values = game.is_terminal(state)
        if terminal: 
            return values[0],None
        elif max_depth==0:
            value=heuristic(game,state,0)
            return value,None
        value=-math.inf
        #get all the actions and for each action get its successor and hence get its heauristic value and save them in list of tuples
        #that looks liks that[(heur value,action)]
        sorted_actions=[(heuristic(game,game.get_successor(state,action),0),action) for action in game.get_actions(state) ] 
        sorted_actions.sort(key=lambda i:i[0],reverse=True) #sort the list of tuples according to the heuristic values in descending order 
        for heur,action in sorted_actions: #loop over the sorted actions and apply the same steps as in alpha beta
            child=game.get_successor(state,action)
            value1,_=alphabeta_ordering_search(game,child,heuristic,alpha,beta,max_depth-1)
            value1=max(value,value1)
            if value1!= value:
                value=value1
                act=action
                if value>=beta:
                    return value,act
                alpha=max(alpha,value)
        return value,act
    else:
        terminal,values = game.is_terminal(state)
        if terminal: 
            return values[0],None
        elif max_depth==0:
            value=heuristic(game,state,0)
            return value,None
        value=math.inf
         #get all the actions and for each action get its successor and hence get its heauristic value and save them in list of tuples
        #that looks liks that[(heur value,action)]
        sorted_actions=[(heuristic(game,game.get_successor(state,action),0),action) for action in game.get_actions(state) ]
        sorted_actions.sort(key=lambda i:i[0])  #sort the list of tuples according to the heuristic values in ascending order 
        for heur,action in sorted_actions: #loop over the sorted actions and apply the same steps as in alpha beta
            child=game.get_successor(state,action)
            value1,_=alphabeta_ordering_search(game,child,heuristic,alpha,beta,max_depth-1)
            value1=min(value,value1)
            if value1!= value:
                value=value1
                act=action
                if value<=alpha:
                    return value,act
                beta=min(beta,value)
        return value,act
# Apply Expectimax search and return the tree value and the best action
# Hint: Read the hint for minimax, but note that the monsters (turn > 0) do not act as min nodes anymore,
# they now act as chance nodes (they act randomly).
def expectimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #TODO: ADD YOUR CODE HERE

    #the uncommented parts are the same as minimax, so return to it
    agent = game.get_turn(state)
    if (agent==0):  #max turn 
        terminal,values = game.is_terminal(state)
        if terminal: 
            return values[0],None
        elif max_depth==0:
            value=heuristic(game,state,0)
            return value,None
        value=-math.inf
        for action in game.get_actions(state):
            child=game.get_successor(state,action)
            value1,_=expectimax(game,child,heuristic,max_depth-1)
            value1=round(max(value,value1),3)  #rounding the values because sometimes the chance node returns values with many decimal places that may be rounded to a near value
            if value1!= value:
                value=value1
                act=action
        return value,act
    else:  #chance node turn
        terminal,values = game.is_terminal(state)
        if terminal: 
            return values[0],None
        elif max_depth==0:
            value=heuristic(game,state,0)
            return value,None
        value=0  #value is the variable that will be used to calculate the expectation, so initialize with zero
        no_of_children=len(game.get_actions(state)) #get number of nodes of this  state
        prob=1/no_of_children #all the children have the same probability so the probability of one node=1/no of children
        for action in game.get_actions(state):
            child=game.get_successor(state,action)
            #for every action and current state get the next state and calculate its value by calling the function recursively
            value1,_=expectimax(game,child,heuristic,max_depth-1)  
            value+=value1*prob #expectation= summation of every value * its probability
        return value,None