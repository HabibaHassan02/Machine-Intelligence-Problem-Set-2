from typing import Any, Dict, List, Optional
from CSP import Assignment, BinaryConstraint, Problem, UnaryConstraint
from helpers.utils import NotImplemented
from heapq import *
import copy

# This function should apply 1-Consistency to the problem.
# In other words, it should modify the domains to only include values that satisfy their variables' unary constraints.
# Then all unary constraints should be removed from the problem (they are no longer needed).
# The function should return False if any domain becomes empty. Otherwise, it should return True.
def one_consistency(problem: Problem) -> bool:
    #TODO: ADD YOUR CODE HERE
    #define a list that will hold the constraints by the end of the loop without the unary constraints
    constr_without_unary=[]  
    for constr in problem.constraints:
        if constr.__class__ is UnaryConstraint:  #checking that this constraint is unary to be able to work on
            var=constr.variable
            a=dict() 
            s=problem.domains[var]
            bol=0
            new_set=set()
            for i in s:
                #writing the assignment of the value to the variable to be sent to the function is_satisfied
                # to check if this assignment satisfies the constraint or not
                a[var]=i 
                bol=constr.is_satisfied(a)
                if bol!=0: 
                    new_set.add(i)  #defining a new set that holds the values of the domain of this variable that satisfies the constraint only
            problem.domains[var]=new_set #changing the domain of the variable in the main problem to hold the values that satisfies the constraint only
        else:
            constr_without_unary.append(constr)  #if the constraint is not unary add it to the list of constraints without unary
    problem.constraints=constr_without_unary #update the list of constraints of the main problem to hold constraints without unary constraints
    dom_flag=True
    dom_lis=problem.domains.values() #get all the sets of values in the problem
     #if one set is empty update the flag, this flag is returned, which will return false if any domain after updates became empty,
     # if all domains hold at least one value then return true
    for dom in dom_lis:
        if len(dom)==0:
            dom_flag=False
    return dom_flag

# This function should implement forward checking
# The function is given the problem, the variable that has been assigned and its assigned value and the domains of the unassigned values
# The function should return False if it is impossible to solve the problem after the given assignment, and True otherwise.
# In general, the function should do the following:
#   - For each binary constraints that involve the assigned variable:
#       - Get the other involved variable.
#       - If the other variable has no domain (in other words, it is already assigned), skip this constraint.
#       - Update the other variable's domain to only include the values that satisfy the binary constraint with the assigned variable.
#   - If any variable's domain becomes empty, return False. Otherwise, return True.
# IMPORTANT: Don't use the domains inside the problem, use and modify the ones given by the "domains" argument 
#            since they contain the current domains of unassigned variables only.
def forward_checking(problem: Problem, assigned_variable: str, assigned_value: Any, domains: Dict[str, set]) -> bool:
    #TODO: ADD YOUR CODE HERE

    #no need to check if the constraint is binary or not because we already removed all unary constraints in the one_consistency function
    for constr in problem.constraints:
        #checking if the assigned variable is one of the 2 variables in the constraint
            if constr.variables[0]==assigned_variable or constr.variables[1]==assigned_variable:
                othervar=constr.get_other(assigned_variable) #getting the other variable in the constraint
                keys=domains.keys()
                if othervar in keys:  #checking that the other variable has domian (not assigned yet)
                    s=domains[othervar]
                    a=dict()
                    bol=0
                    new_set=set()
                    for i in s:
                        #adding the assigned variable with its assigned value and the other variable with one of its
                        #values from the domain to an assignment dictionary to check if constraint is satisfied or not
                        a[assigned_variable]=assigned_value
                        a[othervar]=i
                        bol=constr.is_satisfied(a)
                        #if this value satisfies constraint, then add it to a new set of domains 
                        if bol!=0:
                            new_set.add(i)  
                    #assign this new set that holds only the values that satisfy the constraint
                    # to the domain of the variable in the main problem
                    domains[othervar]=new_set 
    #checking if any domain of any variable after updates became empty then return false, else return true (same as one consistensy function)
    dom_flag=True
    dom_lis=domains.values()
    for dom in dom_lis:
        if len(dom)==0:
            dom_flag=False
    return dom_flag

# This function should return the domain of the given variable order based on the "least restraining value" heuristic.
# IMPORTANT: This function should not modify any of the given arguments.
# Generally, this function is very similar to the forward checking function, but it differs as follows:
#   - You are not given a value for the given variable, since you should do the process for every value in the variable's
#     domain to see how much it will restrain the neigbors domain
#   - Here, you do not modify the given domains. But you can create and modify a copy.
# IMPORTANT: If multiple values have the same priority given the "least restraining value" heuristic, 
#            order them in ascending order (from the lowest to the highest value).
# IMPORTANT: Don't use the domains inside the problem, use and modify the ones given by the "domains" argument 
#            since they contain the current domains of unassigned variables only.
def least_restraining_values(problem: Problem, variable_to_assign: str, domains: Dict[str, set]) -> List[Any]:
    #TODO: ADD YOUR CODE HERE

    pri_domain=dict()
    retdomain=[]
    for constr in problem.constraints:
        if constr.__class__ is BinaryConstraint:
            if constr.variables[0]==variable_to_assign or constr.variables[1]==variable_to_assign:
                othervar=constr.get_other(variable_to_assign)
                if othervar in domains.keys():
                    s1=domains[variable_to_assign] #set of domains of variable to assign
                    s2=domains[othervar]           #set of domains of the other variable in constraint
                    a=dict()
                    for i in s1:
                        new_set=set()
                        a[variable_to_assign]=i  
                        #trying every value in the domain of the variable to assign with all values in the other variable domain
                        for j in s2:
                            a[othervar]=j
                            bol=constr.is_satisfied(a)
                            if bol!=0:
                               new_set.add(j)
                        if "domain element"+str(i) not in pri_domain.keys():
                           pri_domain["domain element"+str(i)]=len(s2)-len(new_set)  #saving the number of changes that this value caused to the domain of the other value
                        else:  #if this value was already available in the dictionary then add its value to the number of changes calculated lately
                            pri_domain["domain element"+str(i)]=pri_domain["domain element"+str(i)]+len(s2)-len(new_set)
    # order the values according to their restrictions ascendingly, the least restricting is the first 
    sorted_domain=sorted(pri_domain.items(),key=lambda items:items[1]) 
    for val in sorted_domain:
        if int(val[0][14]) not in retdomain:
            retdomain.append(int(val[0][14]))
    #modified after q5 
    #check if all the values have the same restrictions, then the returned values of domain should be ordered
    res=True
    test_val = list(pri_domain.values())[0]
    for ele in pri_domain:
        if pri_domain[ele] != test_val:
            res = False
            break
    if res:
        retdomain.sort()
    #########################
    return retdomain

# This function should return the variable that should be picked based on the MRV heuristic.
# IMPORTANT: This function should not modify any of the given arguments.
# IMPORTANT: Don't use the domains inside the problem, use and modify the ones given by the "domains" argument 
#            since they contain the current domains of unassigned variables only.
# IMPORTANT: If multiple variables have the same priority given the MRV heuristic, 
#            order them in the same order in which they appear in "problem.variables".
def minimum_remaining_values(problem: Problem, domains: Dict[str, set]) -> str:
    #TODO: ADD YOUR CODE HERE

    size_dic=dict()
    for variable in domains:
        size_dic[variable]=len(domains[variable])  #saving the lengths of all domains in the dictionary (variable: length)
    #sort the dictionary ascendingly according to lengths and return them as list of tuples [(variable, length)]
    sorted_size=sorted(size_dic.items(),key=lambda items:items[1]) 
    return sorted_size[0][0]  #return the variable in the first tuple (first[0] addresses the first tuple in the list, second [0] addresses the variable in the tuple )

# This function should solve CSP problems using backtracking search with forward checking.
# The variable ordering should be decided by the MRV heuristic.
# The value ordering should be decided by the "least restraining value" heurisitc.
# Unary constraints should be handled using 1-Consistency before starting the backtracking search.
# This function should return the first solution it finds (a complete assignment that satisfies the problem constraints).
# If no solution was found, it should return None.
# IMPORTANT: To get the correct result for the explored nodes, you should check if the assignment is complete only once using "problem.is_complete"
#            for every assignment including the initial empty assignment, EXCEPT for the assignments pruned by the forward checking.
#            Also, if 1-Consistency deems the whole problem unsolvable, you shouldn't call "problem.is_complete" at all.
def solve(problem: Problem) -> Optional[Assignment]:
    #TODO: ADD YOUR CODE HERE
    
    #adjust all domains of variables that have one consistency and remove the unary constraints from the problem
    unary_bol=one_consistency(problem) 
    if unary_bol==True:  #if no domains became empty, start backtracking
        a=dict() #start backtracking with an empty assignemnt
        res=backtrack(a,problem,problem.domains)
        return res
    else:
        return None  #if one domain or more became empty after the one_consistency function then return None
    
def backtrack(assig:Assignment,problem:Problem,domains: Dict[str, set]) ->Optional[Assignment]:
    if problem.is_complete(assig) : #if the assignment is complete then return the assignment
        return assig
    var=minimum_remaining_values(problem,domains) #get the MRV variable 
    if len(domains[var])==1 :  #if the variable has one value in the domain only then save this value in values set 
       values=domains[var]
    else:
        #if the variable has many values then get the least restraining values 
       values=least_restraining_values(problem,var,domains) 
    dummy_domains=copy.deepcopy(domains)  #deeply copy the initial domains before changes 
    del domains[var] #remove the domain of the variable to be assigned from the domains
    for val in values:
        assig[var]=val #assigning value to the variable
        forw_bol=forward_checking(problem,var,val,domains)  #forward checking this assignment
        #if the returned value of the forward checking is true then keep moving in the backtrack function
        #and assign new variable with new value as long as the forward checking is true 
        #if the forward checking is false then try assigning another value to the same variable (looping over values)
        if forw_bol==True:  
            result=backtrack(assig,problem,domains)
            if result!=None: #if the returned value from the backtrack is an assignemnt not None then return it
                return result
            #if the returned value from the backtrack is None that means that the forward_checking failed 
            # at a certain variable, so we need to return back to the domain that we deeply copied before changes 
            domains=dummy_domains #so return the domains to its initial copy before changes and if the variable to be assigned is in thsi domain remove it 
            if var in domains.keys():
                del domains[var]
    return None  #if all values failed in the forwrad checking then return None


