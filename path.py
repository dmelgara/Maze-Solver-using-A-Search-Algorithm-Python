"""Support for path tracing. A path is just a list of states.

Diego Melgara, 2025
"""
import copy
from typing import List, Any, Callable, Optional

def create_path(first_state = None):
    """Create a new empty or singleton path. If first_state has a value, it
    becomes the first state in the path."""
    if first_state is None:
        return []
    return [first_state]

def add_state_to_path(path, state):
    """Paths should be immutable, so this method performs a deep copy of
    the given path, appends the state to the copy, and returns the copy"""
    new_path = copy.deepcopy(path)
    new_path.append(state)
    return new_path

def print_path(path, print_state):
    """Relies on a print_state method to pretty-print a path."""
    for state in path:
        print_state(state)
    print(len(path)-1,"moves")