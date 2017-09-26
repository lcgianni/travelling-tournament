""" 
Program is organized as follows:

Part 1) Import of libraries and user input
Part 2) Use of LKH solver to solve the Traveling Salesman Problem
Part 3) Adaptation of the TSP solution given the Star Weight of each team
Part 4) Using the TSP solution to generate a schedule for the TTP
Part 5) Printing results to user
"""

"""
Part 1
"""

# Imports libs from Python
import subprocess
import time
import numpy as np
import math

# Asks for input of the user
var = raw_input("Enter the instance name (e.g. nl8): ")
numberOfTeams = int(raw_input("Enter the number of teams (e.g. 8): "))

# Transforms var into a string and file name
file = str(var)+".txt"
file2 = str(var)+"_distance.txt"

# The AtMost constraint is 3
K = 3

"""
Part 2
"""

# Edits parameter file for LKH
with open("parameters.txt", "a") as f:
    f.truncate()
    f.write("PROBLEM_FILE = "+file+"\n")
    f.write("OUTPUT_TOUR_FILE = output.txt")

program = 'lkh.exe'
argument = 'parameters.txt'

# Calls lkh.exe with argument
subprocess.call([program, argument])

# After LKH is terminated, looks for output file with Traveling Salesman tour and reads it
with open('output.txt') as f:
    tour = []
    for line in f:
        line = line.split()                      
        if line:                                
            tour.append(line)

# Cleans array tour to make sure the only thing left is the TSP tour
for i in range(6):
    delete = tour.pop(0)
    
for i in range(2):
    delete = tour.pop(-1)

real_tour = []

for i in range(len(tour)):
    real_tour.append(tour[i][0])
    real_tour[i] = int(real_tour[i])

# Array with TSP tour. For example, for 4 teams, [1 3 2 4]
TSP = real_tour

"""
Part 3
"""

# Reads input file for the TTP with distance matrix
with open(file2) as f:
    distanceMatrix = []
    for line in f:
        line = line.split()                      
        if line:                                
            line = [int(i) for i in line]
            distanceMatrix.append(line)

distanceMatrix = np.array(distanceMatrix, dtype=float)

# Calculates star weight for each team
starWeight = np.zeros(numberOfTeams)

for i in range(numberOfTeams):
    
    for j in range(numberOfTeams):
        starWeight[i] += distanceMatrix[i][j]

minimumStarWeight = min(starWeight)

# Reorders TSP tour so it ends in the Team with minimum star weight
while starWeight[TSP[-1] - 1] <> minimumStarWeight:
    temp = np.zeros(numberOfTeams)
    
    for k in range(len(TSP)):
        temp[k - 1] = TSP[k]
        
    TSP = temp

"""
Part 4
"""

# Creates nodes to generate schedule
L1 = np.zeros((numberOfTeams - 2)/2)
L2 = np.zeros((numberOfTeams - 2)/2)
L3 = np.zeros(1)
L4 = np.zeros(1)

counter = 0

# Fills nodes with the teams, following the results from the reordered TSP tour, in a clockwise direction, always skipping one node.
for i in range((numberOfTeams - 2)/2):
    
    if 2*i <= len(L1) - 1:
        L1[2*i] = TSP[i]
        
    else:
        L2[len(L2) - 1 - 2*i] = TSP[i]
    
    counter += 1
    
L3[0] = TSP[counter]    # Team that faces the team with minimum star weight in the first round

counter += 1

for i in range((numberOfTeams - 2)/2):
    
    if 2*i + 1 <= len(L1) - 1:
        L1[2*i + 1] = TSP[counter]
        
    else:
        L2[len(L2) - 1 - 2*i - 1] = TSP[counter]
    
    counter += 1
    
L4[0] = TSP[counter]    # Last team of the TSP tour a.k.a. team with minimum star weight


L1 = np.append(L1,L2)
L1 = L1.reshape(-1, (numberOfTeams - 2)/2)

S1 = np.zeros(K)        # Three downward arrows
S2 = np.ones(K)         # Three upward arrows

current = S1

# Sequence of edges a.k.a. arrows
HAP = np.array([])

# Until all pairs of nodes are assigned, first use S1, then S2, then S1, and so on.
for i in range(int(math.ceil((float(numberOfTeams)/2)/K))):
    
    HAP = np.append(HAP, current)
    
    if current[0] == 0:
        current = S2
        
    else:
        current = S1

# Schedule will be a 2-dimensional array
schedule = np.zeros((numberOfTeams, 2*(numberOfTeams - 1)))

# Creates first half of the tournament. For each round:
for i in range(numberOfTeams - 1):
    
    # First schedules game involving team with minimum star weight
    # If it's a downward arrow, the node on the top is playing away
    if HAP[0] == 0:
        
        schedule[L4[0] - 1][i] = - L3[0]
        schedule[L3[0] - 1][i] = L4[0]
        
    else:
        
        schedule[L4[0] - 1][i] = L3[0]
        schedule[L3[0] - 1][i] = - L4[0]
    
    # Then schedules the remaining games
    for y in range((numberOfTeams/2) - 1):
        
        if HAP[y + 1] == 0:
            
            schedule[L1[0][y] - 1][i] = - L1[1][y]
            schedule[L1[1][y] - 1][i] = L1[0][y]
            
        else:
            
            schedule[L1[0][y] - 1][i] = L1[1][y]
            schedule[L1[1][y] - 1][i] = - L1[0][y]
    
    # Every three rounds, inverts the arrow connected to the team with minimum star weight
    if (i + 1) % 3 == 0:
        
        if HAP[0] == 0:
            
            HAP[0] = 1
            
        else:
            
            HAP[0] = 0
    
    # Moves all nodes in a counter clockwise direction, except for the team with minimum star weight
    temp = np.zeros((numberOfTeams - 2)/2)
    
    for x in range(len(L1[0])):
        
        temp[x - 1] = L1[0][x]
        
    L1[0] = temp
    
    temp = np.zeros((numberOfTeams - 2)/2)
    
    for x in range(len(L1[1]) - 1):
        
        temp[x + 1] = L1[1][x]
    
    temp[0] = L1[1][-1]
    
    L1[1] = temp
    
    temp1 = L1[0][-1]
    temp2 = L1[1][0]
    temp3 = L3[0]
    
    L3[0] = temp1
    L1[0][-1] = temp2
    L1[1][0] = temp3
    

# To obtain second half of tournament, round N + 1 will be N - 2 with opposite signs, round N + 2 will be N - 1, round N + 3 will be N,
# round N + 4 will be 1, round N + 5 will be 2, and so on. This avoids problems with the AtMost constraint.
for i in range(numberOfTeams):
    
    schedule[i][numberOfTeams - 1] = - schedule[i][numberOfTeams - 3]
    
    schedule[i][numberOfTeams] = - schedule[i][numberOfTeams - 2]
    
for y in range(numberOfTeams - 3):
    
    for i in range(numberOfTeams):
        
        schedule[i][numberOfTeams + 1 + y] = - schedule[i][y]

"""
Part 5
"""

# Calculates the number of rounds
numberOfRounds = 2*(numberOfTeams - 1)

# To calculate total distance, sets total distance to 0
totaldistance = 0
    
# Makes a copy of the solution
distanceS = np.copy(schedule)
                
for x in range(numberOfTeams):
        
    # If the entry is positive, team x is playing at home. So make the entry equal to team x. Else, take the absolute of the entry in the schedule.
    distanceS[x] = [x + 1 if i > 0 else abs(i) for i in distanceS[x]]
        
    # Starts by adding distance from team x to first entry in the schedule. If first entry is team x, you're playing at home and the distance added is 0.
    totaldistance += distanceMatrix[x][distanceS[x][0]-1]
    
    for y in range(numberOfRounds - 1):
            
        # Then it adds distance from entry 1 to entry 2, entry 2 to entry 3, and so on.
        totaldistance += distanceMatrix[distanceS[x][y]-1][distanceS[x][y + 1]-1]
        
    # Finally, it adds distance from last entry to team x. If you're playing the last game at home, the distance added is 0.
    totaldistance += distanceMatrix[distanceS[x][-1] - 1][x]


# Prints cost of TTP and final schedule to terminal.
print " "
print " "
print "Cost of TTP = "+str(totaldistance)
print " "
print "Schedule:"
print " "
print schedule
print " "
var = raw_input("Press ENTER to terminate program.")


