from pyamaze import maze, COLOR, agent
import random
from queue import PriorityQueue

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

    while not open.empty():
        currCell = open.get()[1]

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

    return path

# Function to generate the maze
def generate_maze(size):
    m = maze(size, size)

    # Randomize start and goal positions
    start = (random.randint(1, size), random.randint(1, size))
    goal = (random.randint(1, size), random.randint(1, size))

    while start == goal:
        goal = (random.randint(1, size), random.randint(1, size))

    m.CreateMaze(goal[0], goal[1], loopPercent=22)
    path = aStar(m, start, goal)
    
    print("Path found by A*: ", path)

    # Visualize the path dynamically in the maze
    player_agent = agent(m, x=start[0], y=start[1], color=COLOR.blue, filled=True, footprints=True)
    m.tracePath({player_agent: path}, delay=100)  

    m.run()

def main():
    size = 12 
    generate_maze(size)

if __name__ == "__main__":
    main()
