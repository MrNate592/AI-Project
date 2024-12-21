from pyamaze import maze, COLOR, agent,textLabel
import random
from queue import PriorityQueue
import time

# Manhattan Distance Heuristic Function
def h(cell, goal):
    return abs(cell[0] - goal[0]) + abs(cell[1] - goal[1])

# A* Algorithm Implementation taken from https://github.com/khaledkamr/Maze-solver-using-A-star/blob/main/Maze%20solver.py
def aStar(m, start, goal):
    # Initialize g_score and f_score for each cell in the maze
    g_score = {cell: float('inf') for cell in m.grid}
    g_score[start] = 0
    f_score = {cell: float('inf') for cell in m.grid}
    f_score[start] = h(start, goal)

    # Priority queue to store open cells, ordered by f_score
    open = PriorityQueue()
    open.put((f_score[start], start))
    aPath = {}
    visited_nodes = []

    while not open.empty():
        currCell = open.get()[1]
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
                
                temp_g_score = g_score[currCell] + 1
                temp_f_score = temp_g_score + h(childCell, goal)

                # If this path is better, update g_score, f_score and add to open list
                if temp_f_score < f_score[childCell]:
                    g_score[childCell] = temp_g_score
                    f_score[childCell] = temp_f_score
                    open.put((temp_f_score, childCell))
                    aPath[childCell] = currCell

    # Reconstruct the path from start to goal
    path = []
    cell = goal
    while cell != start:
        path.append(cell)
        cell = aPath.get(cell)
    path.append(start)
    path.reverse()  # Reversed to start from the start point
    
    optimal_path_length = len(path)
    visited_nodes_count = len(visited_nodes)
    efficiency = optimal_path_length / visited_nodes_count if visited_nodes_count else 0

    return path, visited_nodes, g_score[goal], efficiency

# Function to generate the maze
def generate_maze(size):
    used_positions = set()

    for i in range(3):  # Generate and solve 3 mazes
        start = (random.randint(1, size), random.randint(1, size))
        while start in used_positions:
            start = (random.randint(1, size), random.randint(1, size))
        used_positions.add(start)

        goal = (random.randint(1, size), random.randint(1, size))
        while goal in used_positions or goal == start:
            goal = (random.randint(1, size), random.randint(1, size))
        used_positions.add(goal)
        
        m = maze(size, size)
        m.CreateMaze(goal[0], goal[1], loopPercent=100)
        
        start_time = time.perf_counter()
        path, visited_nodes, path_cost, efficiency = aStar(m, start, goal)
        end_time = time.perf_counter()

        time_taken = end_time - start_time
        visited_nodes_count = len(visited_nodes)
        
        print(f"\nMaze {i + 1}:")
        print(f"- Start Position: {start}")
        print(f"- Goal Position: {goal}")
        print(f"- Time Taken: {time_taken:.4f} seconds")
        print(f"- Total Nodes Visited: {visited_nodes_count}")
        print(f"- Path Cost: {path_cost+1}")
        print(f"- Optimal Path: {path}")
        print(f"- Efficiency: {efficiency:.2%}")

        player_agent = agent(m, x=start[0], y=start[1], color=COLOR.red, filled=True, footprints=True, shape="arrow")
        m.tracePath({player_agent: path}, delay=20)          
        
        m.run()

def main():
    size = 12 
    generate_maze(size)

if __name__ == "__main__":
    main()
