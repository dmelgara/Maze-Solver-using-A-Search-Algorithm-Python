import prim_maze_generator
import time
import heapq
"""
Diego Melgara, 2025
"""
def get_start_and_goal(maze):
    """
    Determines the start and goal positions in the maze.
    Assumes that:
     -The start is a clear cell ('c') in the first row.
     -The goal is a clear cell ('c') in the last row.
    If not found, defaults are provided.
    """
    height = len(maze)
    width = len(maze[0])
    start = None
    # Search for a clear cell in the first row
    for j in range(width):
        if maze[0][j] == 'c':
            start = (0, j)
            break
    if start is None:
        start = (0, 0)

    goal = None
    # Search for a clear cell in the last row (from right to left)
    for j in range(width - 1, -1, -1):
        if maze[height - 1][j] == 'c':
            goal = (height - 1, j)
            break
    if goal is None:
        goal = (height - 1, width - 1)

    return start, goal

def cost(cell):
    """
    Computes the cost for entering a cell:
      - If the cell is 'c', cost is 1.
      - If the cell is a digit, cost is 1 plus the digit's value.
      - Otherwise, defaults to cost 1.
    """
    if cell == 'c':
        return 1
    elif isinstance(cell, str) and cell.isdigit():
        return 1 + int(cell)
    else:
        return 1

def heuristic(state, goal):
    """
    Heuristic function using Manhattan distance between the current state and the goal.
    """
    return abs(goal[0] - state[0]) + abs(goal[1] - state[1])

def a_star_search(maze, start, goal):
    """
    Executes the A* search algorithm on the maze.
    Returns a tuple (path, total_cost) if a solution is found,
    or (None, None) if no solution exists.

    The path is a list of coordinates (tuples) from the start to the goal.
    """
    height = len(maze)
    width = len(maze[0])
    open_set = []

    g = 0
    h = heuristic(start, goal)
    f = g + h
    heapq.heappush(open_set, (f, g, start, [start]))

    closed = set()

    while open_set:
        f, g, state, path = heapq.heappop(open_set)
        if state == goal:
            return path, g
        if state in closed:
            continue
        closed.add(state)

        r, c = state
        # Explore neighbors: up, down, left, right.
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < height and 0 <= nc < width:
                if maze[nr][nc] != 'w':
                    new_state = (nr, nc)
                    if new_state in closed:
                        continue
                    new_g = g + cost(maze[nr][nc])
                    new_f = new_g + heuristic(new_state, goal)
                    new_path = path + [new_state]
                    heapq.heappush(open_set, (new_f, new_g, new_state, new_path))
    return None, None

def mark_path_on_maze(maze, path):
    new_maze = [row[:] for row in maze]
    for (r, c) in path:
        new_maze[r][c] = '*'
    return new_maze

def main():
    # Request maze parameters from the user
    try:
        height = int(input("Enter maze height: "))
        width = int(input("Enter maze width: "))
        diff = float(input("Enter difficulty parameter (0.0 to 1.0): "))
    except Exception as e:
        print("Invalid input. Using default values: height=15, width=15, difficulty=0.5")
        height, width, diff = 15, 15, 0.5

    # Generate maze in multipath mode with the given difficulty parameter
    maze = prim_maze_generator.generate_maze(height, width, True, diff)
    print("\nGenerated Maze:")
    prim_maze_generator.print_maze(maze)
    print()

    # Determine the start and goal states of the maze
    start, goal = get_start_and_goal(maze)
    print("Start position:", start)
    print("Goal position:", goal)

    # Execute A* Search on the maze
    start_time = time.time()
    path_found, total_cost = a_star_search(maze, start, goal)
    end_time = time.time()

    if path_found is None:
        print("No solution found.")
    else:
        print("\nSolution found!")
        print("Path length (number of moves):", len(path_found) - 1)
        print("Total cost:", total_cost)
        print("Time taken: {:.6f} seconds".format(end_time - start_time))
        print("\nMaze with solution path:")
        maze_with_path = mark_path_on_maze(maze, path_found)
        prim_maze_generator.print_maze(maze_with_path)

if __name__ == "__main__":
    main()
