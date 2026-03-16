"""NAMES OF THE AUTHOR(S): Alice Burlats <alice.burlats@uclouvain.be>"""

import random
from lsnode import LSNode
from atom_placement import AtomPlacement


def random_walk(problem, limit=100) -> LSNode:
    """
    Perform a random walk in the search space and returns a LSNode corresponding to the best found solution.
    """
    current = LSNode(problem, problem.init_state(), 0)
    best = current
    for step in range(limit):
        current = random.choice(list(current.expand()))
        if current.value() < best.value():
            best = current
    return best


def max_value(problem: AtomPlacement, limit=100) -> LSNode:
    """
    Perform a local search by selecting at each iteration the best neighbor of the current state.
    Returns a LSNode corresponding to the best found solution
    """
    state = LSNode(problem,problem.init_state() , 0)
    best_neighbor  = state 
    for i in range(limit):
        neighbors = list(state.expand())
        if not neighbors :
            break
        best = neighbors[0]
        for i in neighbors[1:]:
            if i.value()<best.value():
                best = i
        state = best 
        if state.value() < best_neighbor.value():
            best_neighbor= state
    return best_neighbor



def randomized_max_value(problem: AtomPlacement, limit=100) -> LSNode:
    """
    Perform a local search by randomly selecting a neighbor among the 5 bests
    at each iteration.
    Returns a LSNode corresponding to the best found solution
    """
    state = LSNode(problem,problem.init_state() , 0)
    best_neighbor  = state 
    for i in range(limit):
        neighbors = list(state.expand())
        if not neighbors :
            break
        l=neighbors[:5]
        for j  in neighbors[5:]:
            worst = l[0]
            for n in l[1:]:
                if n.value()> worst.value():
                    worst = n
            if j.value() < worst.value():
                l[l.index(worst)] =j
        state = random.choice(l)
        if state.value() < best_neighbor.value():
            best_neighbor = state
    return best_neighbor
