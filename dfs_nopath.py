"""Implementation of Depth-First Search with pruning of visited
nodes. Relies on is_goal and next_states methods that must be imported from
elsewhere.

Diego Melgara, 2025
"""
## import LifoQueue (stack)
from queue import LifoQueue

## import puzzle api
from three_puzzle import next_states, is_goal, get_start_state, get_start_state_solvable, get_start_state_handout, print_state

from path import print_path

## solver
def DFS(start_state):
    """Performs a depth-first search starting at start_state. Returns True or
    False to indicate whether a path to the goal exists. Relies on functions
    is_goal and next_states to define the goal and the search"""
    closed = []                 # init open, closed
    open = LifoQueue()
    open.put((start_state, [start_state]))

    while not open.empty():        # loop until no more open states

        state, path = open.get(False)    # get next state to expand

        if state not in closed:    # prune?

            closed.append(state)   # mark state visited (closed)

            if is_goal(state):     # success?
                return path

            for new_state in next_states(state):    # expand state
                open.put((new_state, path + [new_state])) # new states are open

    return None              # goal not found

## run the solver
from time import time
start_state = get_start_state_handout()

start = time()
solution_path = DFS(start_state)
end = time()

if solution_path is None:
    print("No solution found.")
else:
    print("Solution found!")
    # Print the path by printing each state
    for s in solution_path:
        print_state(s)
    print("Path length (number of moves):", len(solution_path) - 1)

print("Time:", end - start, "seconds")