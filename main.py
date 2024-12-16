from pyamaze import maze, COLOR, agent
import random

# Generates maze of given size
def generate_maze(size):
    m = maze(size, size)
    
    start = (random.randint(1, size), random.randint(1, size))
    goal = (random.randint(1, size), random.randint(1, size))
    
    m.CreateMaze(*goal, loopPercent=22)    # Run the maze simulation
    a=agent(m)
    a.position = (start)

    print(m.maze_map)
    m.run()

generate_maze(12)