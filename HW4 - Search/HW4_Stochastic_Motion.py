# --------------
# USER INSTRUCTIONS
#
# Write a function called stochastic_value that
# returns two grids. The first grid, value, should
# contain the computed value of each cell as shown
# in the video. The second grid, policy, should
# contain the optimum policy for each cell.
#
# --------------
# GRADING NOTES
#
# We will be calling your stochastic_value function
# with several different grids and different values
# of success_prob, collision_cost, and cost_step.
# In order to be marked correct, your function must
# RETURN (it does not have to print) two grids,
# value and policy.
#
# When grading your value grid, we will compare the
# value of each cell with the true value according
# to this model. If your answer for each cell
# is sufficiently close to the correct answer
# (within 0.001), you will be marked as correct.

delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>'] # Use these when creating your policy grid.

# ---------------------------------------------
#  Modify the function stochastic_value below
# ---------------------------------------------

def stochastic_value(grid,goal,cost_step,collision_cost,success_prob):
    failure_prob = (1.0 - success_prob)/2.0 # Probability(stepping left) = prob(stepping right) = failure_prob
    value = [[collision_cost for col in range(len(grid[0]))] for row in range(len(grid))]
    policy = [[' ' for col in range(len(grid[0]))] for row in range(len(grid))]

    change = True

    while change:
        change = False

        for x in range(len(grid)):
            for y in range(len(grid[0])):
                if goal[0] == x and goal[1] == y:
                    if value[x][y] > 0:
                        value[x][y] = 0
                        policy[x][y] = "*"

                        change = True

                elif grid[x][y] == 0:
                    potential_costs = []
                    for a in range(len(delta)):
                        x2 = x + delta[a][0]
                        y2 = y + delta[a][1]

                        x_right = x + delta[(a-1)][0]
                        y_right = y + delta[(a-1)][1]
                        # print delta[a-1][0]
                        # print delta[a-1][1]
                        x_left = x + delta[(a+1) % len(delta)][0]
                        y_left = y + delta[(a+1) % len(delta)][1]

                        #print [x, y, x2, y2, x_right, y_right, x_left, y_left, a]
                        if x2 < 0 or x2 >= len(grid) or y2 < 0 or y2 >= len(grid[0]):
                            cost2 = collision_cost
                        else:
                            cost2 = value[x2][y2]

                        if x_left < 0 or x_left >= len(grid) or y_left < 0 or y_left >= len(grid[0]):
                            cost_left = collision_cost
                        else:
                            cost_left = value[x_left][y_left]

                        if x_right < 0 or x_right >= len(grid) or y_right < 0 or y_right >= len(grid[0]):
                            cost_right = collision_cost
                        else:
                            cost_right = value[x_right][y_right]

                        #direction = delta_name[a]

                        potential_costs.append(cost2*success_prob + cost_left*failure_prob + cost_right*failure_prob + cost_step)

                    #print [ x, y, potential_costs]
                    v2,idx = min( (potential_costs[i],i) for i in xrange(len(potential_costs)) )
                    direction = delta_name[idx]
                        #if x2 >= 0 and x2 < len(grid) and y2 >= 0 and y2 < len(grid[0]) and grid[x2][y2] == 0:
                        #    v2 = value[x2][y2]*success_prob + cost_left*failure_prob + cost_right*failure_prob + cost_step

                    if v2 < value[x][y]:
                        change = True
                        value[x][y] = v2
                        policy[x][y] = direction
                        # for row in value:
                        #     print row
                        # for row in policy:
                        #     print row
                        # print "\n"

    return value, policy

# ---------------------------------------------
#  Use the code below to test your solution
# ---------------------------------------------

grid = [[0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 1, 1, 0]]
goal = [0, len(grid[0])-1] # Goal is in top right corner
cost_step = 1
collision_cost = 100
success_prob = 0.5

value,policy = stochastic_value(grid,goal,cost_step,collision_cost,success_prob)
for row in value:
    print row
for row in policy:
    print row


# Expected outputs:
#
# [57.9029, 40.2784, 26.0665,  0.0000]
# [47.0547, 36.5722, 29.9937, 27.2698]
# [53.1715, 42.0228, 37.7755, 45.0916]
# [77.5858, 100.00, 100.00, 73.5458]
#
# ['>', 'v', 'v', '*']
# ['>', '>', '^', '<']
# ['>', '^', '^', '<']
# ['^', ' ', ' ', '^']
