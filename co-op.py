# Cooperative pathfinding theory https://www.davidsilver.uk/wp-content/uploads/2020/03/coop-path-AIIDE.pdf

from pyamaze import maze, COLOR, agent
import random
from queue import PriorityQueue
import time

# Manhattan Distance Heuristic Function
def h(cell, goal):
    return abs(cell[0] - goal[0]) + abs(cell[1] - goal[1])

# A* Algorithm Implementation taken from https://github.com/khaledkamr/Maze-solver-using-A-star/blob/main/Maze%20solver.py
def cooperative_a_star(m, start, goal, reservation_table, agent_id=None):
    # Initialize g_score and f_score for each cell in the maze
    g_score = {cell: float('inf') for cell in m.grid}
    g_score[start] = 0
    f_score = {cell: float('inf') for cell in m.grid}
    f_score[start] = h(start, goal)

    # Priority queue to store open cells, ordered by f_score
    open = PriorityQueue()
    open.put((f_score[start], start, 0))  # (f_score, cell, time)
    aPath = {}
    visited_nodes = []

    while not open.empty():
        curr = open.get()
        currCell, currTime = curr[1], curr[2]
        visited_nodes.append(currCell)

        if currCell == goal:
            break

        # Check adjacent cells in the maze (N, E, S, W directions)
        for d in "ESNW":
            if m.maze_map[currCell][d] == True:  # If there's a valid path in the direction
                # Calculate the child cell's coordinates based on direction
                if d == 'E':
                    childCell = (currCell[0], currCell[1] + 1)
                elif d == 'W':
                    childCell = (currCell[0], currCell[1] - 1)
                elif d == 'N':
                    childCell = (currCell[0] - 1, currCell[1])
                elif d == 'S':
                    childCell = (currCell[0] + 1, currCell[1])

                # Add path to reservation table and check if it's blocked by other agents
                # Implementation of the reservation table gathered from ChatGPT
                t = g_score[currCell] + 1
                if (childCell, t) in reservation_table:
                    print(f"Blocked cell: {childCell} at time {t}")
                    continue  # Skip this cell if it's reserved

                temp_g_score = g_score[currCell] + 1
                temp_f_score = temp_g_score + h(childCell, goal)

                # If this path is better, update g_score, f_score and add to open list
                if temp_f_score < f_score[childCell]:
                    g_score[childCell] = temp_g_score
                    f_score[childCell] = temp_f_score
                    open.put((temp_f_score, childCell, t))
                    aPath[(childCell, t)] = (currCell, currTime)

    # Reconstruct the path from start to goal
    path = []
    cell = goal
    time = max([t for (c, t) in aPath.keys() if c == cell], default=0)
    while (cell, time) in aPath:
        path.append(cell)
        cell, time = aPath[(cell, time)]
    path.append(start)
    path.reverse()  # Reversed to start from the start point

    # Add path to reservation table
    for t, cell in enumerate(path):
        reservation_table[(cell, t)] = True

    optimal_path_length = len(path)
    visited_nodes_count = len(set(visited_nodes))

    efficiency = optimal_path_length / visited_nodes_count if visited_nodes_count else 0

    return path, visited_nodes_count, optimal_path_length, efficiency


# Function to generate the maze and test the cooperative pathfinding
def generate_maze(size):
    start1 = (random.randint(1, size), random.randint(1, size))
    start2 = (random.randint(1, size), random.randint(1, size))
    goal = (random.randint(1, size), random.randint(1, size))

    # Ensure the start positions and goal are not the same
    while start1 == goal or start2 == goal or start1 == start2:
        start1 = (random.randint(1, size), random.randint(1, size))
        start2 = (random.randint(1, size), random.randint(1, size))
        goal = (random.randint(1, size), random.randint(1, size))

    for i in range(3):  # Generate and solve 3 mazes
        m = maze(size, size)
        m.CreateMaze(goal[0], goal[1], loopPercent=100)

        reservation_table = {}

        print("\nAgent 1:")
        overall_start_time = time.perf_counter()
        start_time1 = time.perf_counter()
        path1, visited1, cost1, efficiency1 = cooperative_a_star(m, start1, goal, reservation_table)
        end_time1 = time.perf_counter()

        print(f"Start: {start1}, Goal: {goal}")
        print(f"Visited Nodes: {visited1}")
        print(f"Path Cost: {cost1+1}")
        print(f"Efficiency: {efficiency1:.2%}")
        print(f"Time Taken: {end_time1 - start_time1} seconds")
        print(f"- Optimal Path: {path1}")
        
        print("\nAgent 2:")
        start_time2 = time.perf_counter()
        path2, visited2, cost2, efficiency2 = cooperative_a_star(m, start2, goal, reservation_table)
        end_time2 = time.perf_counter()
    
        overall_end_time = time.perf_counter()
        
        print(f"Start: {start2}, Goal: {goal}")
        print(f"Visited Nodes: {visited2}")
        print(f"Path Cost: {cost2+1}")
        print(f"Efficiency: {efficiency2:.2%}")
        print(f"Time Taken: {end_time2 - start_time2:.4f} seconds")
        print(f"- Optimal Path: {path2}")

        # Set up the agents' starting positions and trace paths
        agent1 = agent(m, x=start1[0], y=start1[1], color=COLOR.red, filled=False, footprints=True, shape="arrow")
        agent2 = agent(m, x=start2[0], y=start2[1], color=COLOR.blue, filled=True, footprints=True, shape="arrow")
        m.tracePath({agent1: path1, agent2: path2}, delay=100)
        print(f"Overall Time Taken: {overall_end_time - overall_start_time} seconds")

        m.run()


def main():
    size = 12
    generate_maze(size)

if __name__ == "__main__":
    main()
