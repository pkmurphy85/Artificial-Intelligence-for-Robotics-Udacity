# ----------
# User Instructions:
#
# Define a function, search() that returns a list
# in the form of [optimal path length, row, col]. For
# the grid shown below, your function should output
# [11, 4, 5].
#
# If there is no valid path from the start point
# to the goal, your function should return the string
# 'fail'
# ----------

# Grid format:
#   0 = Navigable space
#   1 = Occupied space

grid = [[0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 0]]
init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1]
cost = 1

delta = [[-1, 0], # go up
         [ 0,-1], # go left
         [ 1, 0], # go down
         [ 0, 1]] # go right

delta_name = ['^', '<', 'v', '>']

def add_list_elements(a, b):
    return [x+y for x,y in zip(a, b)]

def search(grid,init,goal,cost):
    # ----------------------------------------
    # insert code here
    # ----------------------------------------


    open_list = [ [0, init[0], init[1]] ]
    visited = []

    current_item = open_list[0]
    current_space = [current_item[1], current_item[2]]
    del(open_list[0])

    while current_space != goal:
        visited.append(current_space)
        print current_item
        print visited
        for move in delta:
            next_space = add_list_elements(current_space, move)

            if (next_space[0] >= 0 and next_space[0] <= len(grid)-1) and (next_space[1] >= 0 and next_space[1] <= len(grid[0])-1) :  # check if still in grid (non-circular)
                if next_space not in visited: # check that we have not visited space
                    if grid[next_space[0]][next_space[1]] == 0: # check if space available
                        print "\t {}".format(next_space)
                        open_list.append([current_item[0]+1, next_space[0], next_space[1]])
                        open_list.sort()

                # else:
                #     print next_space
        #print "\t\t {}".format(open_list)
        if len(open_list):
            current_item = open_list[0]
            current_space = [current_item[1], current_item[2]]
            del(open_list[0])
        else:
            return "fail"

    path = current_item
    return path

print search(grid,init,goal,cost)
