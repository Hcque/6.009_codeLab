"""6.009 Lab 5 -- Boolean satisfiability solving"""

import sys
sys.setrecursionlimit(10000)
# NO ADDITIONAL IMPORTS

# Helper function
def simplify(formula, assignments):
    """Simplify formula for given assignments
    Return:
        formula: simplified
        assignments: may add new assignments
    """
    is_new_assign = True
    while is_new_assign:
        is_new_assign = False
        # update
        formula, assignments, is_new_assign =\
        inner_loop(formula, assignments, is_new_assign) 
    return formula, assignments
# End helper function

def satisfying_assignment(formula):
    """Find a satisfying assignment for a given CNF formula.
    Returns that assignment if one exists, or None otherwise.

    >>> satisfying_assignment([])
    {}
    >>> sa = satisfying_assignment([[('a', True), ('b', False), ('c', True)]])
    >>> ('a' in sa and sa['a']) or ('b' in sa and not sa['b']) or ('c' in sa and sa['c'])
    True
    >>> satisfying_assignment([[('a', True)], [('a', False)]]) is None
    True
    """
    # base case
    if formula == []:
        return {}
    # assign first variable
    new_lit = formula[0][0][0]
    formula_t, assign_t = simplify(formula, {new_lit:True})
    formula_f, assign_f = simplify(formula, {new_lit:False})
#    print('------------------------')
#    print('formula_t: ', formula_t)
#    print('formula_f', formula_f)
    
    # depth first search
    if formula_t is not None and satisfying_assignment(formula_t) is not None:
        return {**assign_t, **satisfying_assignment(formula_t)}
    elif formula_f is not None and satisfying_assignment(formula_f) is not None:
        return {**assign_f, **satisfying_assignment(formula_f)}   
    else:
        return None

def simplify_formula(formula, assignments):
    '''
      Input: a boolean formula in the CNF format described above.
            a set of assignments to boolean variables represented as a dictionary
            from variables to boolean values.
      Output: a pair (Formula, Changed), where Formula is
      the new simplified formula, and Changed is a boolean
      that determines whether or not the simplification added new
      assignments. If the assignment causes the formula to
      evaluate to False, you should return (None, False).
      Effects: the operation potentially adds new assignments to
      assignments. However, the operation should NOT modify
      the input formula when creating the output (although it is ok
        for the output formula to share unchanged clauses with the input formula).

      Note that when the simplification creates new assignments,
      those assignments may themselves enable further simplification.
      You should make sure all those newly enabled simplifications
      are performed as well.

      It is advised that you write your own tests for this function.
    '''
    is_new_assign = True
    cnt = 0
    while is_new_assign:
        is_new_assign = False
        # update
        formula, assignments, is_new_assign =\
        inner_loop(formula, assignments, is_new_assign)
        cnt = cnt + 1
    # formula is false in given assignments
    if formula is None: 
        return None, False
    
    if cnt > 1:# check if assigned new varibale
        assign_global = True
    else:
        assign_global = False
    return formula, assign_global

# Helper function
def inner_loop(formula, assignments, is_new_assign):
    """Simplify formula for given assignments
    Args:
        formula (nested list)
        assignments (dict)
        is_new_assign (bool) : initially False
    Return:
        fin_formula (nested list)
        assignments (dict)
        is_new_assign (bool) : assign True if adding new assignments
    """
    is_new_assign = is_new_assign
    # initial
    del_lit = [[] for i in formula]
    del_cla = []
    # walk through
    for i, clause in enumerate(formula):
        n = len(clause)
        for j, t in enumerate(clause):
            lit, bool = t
            if lit in assignments:
                if assignments[lit] == bool: # lit value is true
                    del_cla.append(i) # collect del cluase idx
                    break # del clause in outer loop
                else: # delete lit
                    del_lit[i].append(j) # collect del idx
        # check if del all
        if len(del_lit[i]) == n:
            return None, assignments, False # formular is False

        # do the deletion
        # 1. delete clause
        new_formula = del_via_idx(formula, del_cla)
        # 2. delete lit
        new_del_lit = del_via_idx(del_lit, del_cla)
        fin_formula = [del_via_idx(cla, idx_L) for idx_L, cla in\
                       zip(new_del_lit, new_formula)]

    # see if one element in clause
    # seek opportunity for new assignment
    for clause in fin_formula:
        if len(clause) == 1 and clause[0] not in assignments:
            # new assign
            is_new_assign = True
            # add to assign dict
            assignments[clause[0][0]] = clause[0][1]

    return fin_formula, assignments, is_new_assign

def del_via_idx(L, idx_L):
    """
    Input:
        idx_L (list) : contain index of L needed to be deleted
        L (list) 
    Return:
        ans (list) : a new list with some keys deleted
    """        
    ans = [ele for i, ele in enumerate(L) if i not in idx_L]
    return ans  
# End helper function
    
def managers_for_actors(K, film_db):
    '''
    Input:
       K , number of managers available.
       film_db, a list of [actor, actor, film] triples describing that two
       actors worked together on a film.
    Output:
        A dictionary representing an assignment of actors to managers, where
        actors are identified by their numerical id in film_db and
        managers are identified by a number from 0 to K-1.
        The assignment must satisfy the constraint that
        if two actors acted together in a film, they should not have the
        same manager.
        If no such assignment is possible, the function returns None.

    You can write this function in terms of three methods:
        make_vars_for_actors: for each actor in the db, you want an indicator
        variable for every possible manager indicating whether that manager
        is the manager for that actor.

        make_one_manager_constraints: This function should create constraints that
        ensure that each actor has one and only one manager.

        make_different_constraint: This function should create constraints
        that ensure that each actor has a different manager from other actors
        in the same movie.

    '''    
    # transform data
    adj, actors = make_adj(film_db)
    # construct formula
    ind_dict, ind_list = make_vars_for_actors(actors, K)
    constraint_1 = make_one_manager_constraints(actors, ind_dict)
    constraint_2 = make_different_constraints(adj, ind_dict, actors)
    formula = ind_list + constraint_1 + constraint_2
    # solve using SAT
#    print(formula)
    assigns = satisfying_assignment(formula)  
#    print(assigns)
#    print(len(assigns))
    if assigns is None:
        return None
    # get answer
    ans = {}
    for actor_id in actors:
        for i in range(K):
            vari = str(actor_id) +'_'+ str(i)
            if assigns[vari]:
                ans[actor_id] = i
                break
    return ans
         
# Helper function
def make_adj(film_db):
    """Make adjacency lists and actor id list.
    """
    adj = {}
    for entry in film_db:
        a1, a2, _ = entry
        if a1 != a2: 
            if a1 not in adj:
                adj[a1] = [a2]
            elif a2 not in adj[a1]:
                adj[a1].append(a2)
            if a2 not in adj:
                adj[a2] = [a1]
            if a2 in adj and a1 not in adj[a2]:
                adj[a2].append(a1)
    actors = list(adj.keys())   
    return adj, actors

def make_vars_for_actors(actors, K):
    """   
    Args:
        actors list of actor ids
        K (int)
    Returns:
        ind_dict: a dict with indicator lists
        ind_list
    """
    ind_dict = {}
    ind_list = []
    for actor_id in actors:
        indicator = [(str(actor_id)+ '_' + str(i), True) for i in range(K)]
        ind_dict[actor_id] = indicator
        ind_list.append(indicator)
    return ind_dict, ind_list

def get_all_sets(indic):
    """Recursively get all possiablities
    Args:
        indic (list)
    Return:
        a iterator 
    """
    if len(indic) == 0:
        yield ()
    else:
        new_L = [(indic[0][0], True), (indic[0][0], False)]
        yield from ((j,) + i for i in get_all_sets(indic[1:]) for j in new_L) 

def get_rem_sets(indic):
    """Return a list of sets
    """
    get_name = lambda x: [i[0] for i in x]
    names = get_name(indic)
#    print(names)
    removed = []
    for i in names:
        one = (i, True) # who has not
        others = [(j, False) for j in names if j != i]
        others.append(one)
        removed.append(set(others))
    return removed

def make_one_manager_constraints(actors, ind_dict):
    """Return a CNF expression for each indicator, characterize 
    if indicator has one True.
    return form : [[.], []]
    """
    ans = []
    for k, indic in ind_dict.items():
        alls = get_all_sets(indic)
        removed = get_rem_sets(indic)
        for i in alls:
            i = set(i)
            if i not in removed:
                i = list(i)
                # reverse           
                rev_i = []
                for j in i:
                    rev_i.append((j[0], not j[1]))
                ans.append(rev_i)
    return ans

def make_different_constraints(adj, ind_dict, actors):
    """Return a CNF expression characterizing if indicatior of 
    two actors are the same.
        Notice ans : [[(,),(,)],[(,),(,)]...]
    """
    ans = []
    for id_1 in actors:
        indic_1 = ind_dict[id_1]
        for id_2 in adj[id_1]:
#            one_match = []
            indic_2 = ind_dict[id_2]
            for b1, b2 in zip(indic_1, indic_2):
                ans.append([(b1[0], False),(b2[0], False)])
#                one_match.append((b1[0], False))
#                one_match.append((b2[0], False))
            
#            ans.extend(one_match)
#            ans.append(one_match)
    return ans
# End helper function

def check_solution(sol, K, film_db):
    '''
    Input:
        K, number of managers
        flim_db, a list of [actor, actor, film] triples describing that two
        actors worked together on a film.
        sol, an assignment of actors to managers.
    Output:
        The function returns True if sol satisfies the constraint that
        if two actors acted together in a film, they should not have the
        same manager and every manager has an ID less than K.
        It returns False otherwise.
    '''
    for id_1, id_2, _ in film_db:
        if id_1 != id_2 and sol[id_1] == sol[id_2]:
            return False
    return True
        

