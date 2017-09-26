""" 
Program is organized as follows:

Part 1) Import of libraries and input files
Part 2) Simulated Annealing
"""

"""
Part 1
"""

# Imports libs from python
import random
import time
import math
import numpy as np
import numexpr

# Asks for input of the user and stores in variable var
var = raw_input("Enter the instance name (e.g. nl8): ")

# Transforms var into a string
file = str(var)+".txt"
file2 = "Solution_"+str(var)+".txt"

# Variables for Simulated Annealing, set manually
maxP = 1000
maxC = 1000
maxR = 10
T = float(400)
beta = 0.999       
weight = 4000
teta = 1.04

# Open input file
with open(file) as f:
    distance_matrix = []
    for line in f:
        line = line.split()                     # Breaks elements of line whenever there's a space 
        if line:                                # If line is not blank
            line = [int(i) for i in line]       # Turns each element of line into an integer and
            distance_matrix.append(line)        # adds to bidimensional array

# Number of teams will be length of distance_matrix  
numberOfTeams = len(distance_matrix)

# Defines number of rounds
numberOfRounds = 2*(numberOfTeams - 1)

# Converts array into a numpy array for faster computation. And changes type of variable to float.
distance_matrix = np.array(distance_matrix, dtype=float)

# Open file with solution
with open(file2) as f:
    initialS = []
    for line in f:
        line = line.split()                      
        if line:                                
            line = [int(i) for i in line]
            initialS.append(line)

initialS = np.array(initialS, dtype=int)            

"""
Part 2
"""

def simulated_annealing(maxP,maxC,maxR,T,beta,weight,teta):
    
    # Starts from solution of the approximation algorithm
    S = initialS
    
    # No need to calculate violations, since initial solution is feasible         
    # To calculate total distance, sets total distance to 0
    totaldistance = 0
    
    # Makes a copy of the solution
    distanceS = np.copy(S)
                
    for x in range(numberOfTeams):
        
        # If the entry is positive, team x is playing at home. So make the entry equal to team x. Else, take the absolute of the entry in the schedule.
        distanceS[x] = [x + 1 if i > 0 else abs(i) for i in distanceS[x]]
        
        # Starts by adding distance from team x to first entry in the schedule. If first entry is team x, you're playing at home and the distance added is 0.
        totaldistance += distance_matrix[x][distanceS[x][0]-1]
    
        for y in range(numberOfRounds - 1):
            
            # Then it adds distance from entry 1 to entry 2, entry 2 to entry 3, and so on.
            totaldistance += distance_matrix[distanceS[x][y]-1][distanceS[x][y + 1]-1]
        
        # Finally, it adds distance from last entry to team x. If you're playing the last game at home, the distance added is 0.
        totaldistance += distance_matrix[distanceS[x][-1] - 1][x]
                    
    costS = totaldistance

        
    # Sets best feasible solution so far to cost of initial solution
    bestFeasible = costS
    nbf = costS
    
    # Sets best infeasible solution so far to cost of initial solution
    bestInfeasible = costS
    nbi = costS
    
    reheat = 0
    counter = 0
    
    # While system has not reheated maxR times without improving the solution
    while reheat <= maxR:
        
        phase = 0
        
        # While system has not decreased the temperature maxP times without improving the solution
        while phase <= maxP:
            
            counter = 0
            
            # While system has not rejected maxC moves
            while counter <= maxC:
                
                # Choose random move
                chooseMove = random.randint(0,4)
                
                if chooseMove == 0:     # Swap Homes
                    
                    newS = np.copy(S)   # The new solution is a copy of the current one
                    
                    teamA = random.randint(0,numberOfTeams - 1)         # Choose random team A
                    teamB = random.randint(0,numberOfTeams - 1)         # Choose random team B
                    
                    for i in range(numberOfRounds):
                        
                        # When team A and team B play each other
                        if abs(S[teamA][i]) == teamB + 1:
                            
                            # Invert the signs (swap homes)
                            newS[teamA][i] = - S[teamA][i]
                            newS[teamB][i] = - S[teamB][i]
    
                
                elif chooseMove == 1:   # Swap Rounds
                    
                    newS = np.copy(S)
                    
                    roundAindex = random.randint(0,numberOfRounds - 1)  # Choose random round A
                    roundBindex = random.randint(0,numberOfRounds - 1)  # Choose random round B
                    
                    # Swap columns of array (swap rounds)
                    newS[:,[roundAindex,roundBindex]] =  newS[:,[roundBindex,roundAindex]]
                    
                    
                elif chooseMove == 2:   # Swap Teams
                    
                    newS = np.copy(S)
                    
                    teamA = random.randint(0,numberOfTeams - 1)         # Choose random team A
                    teamB = random.randint(0,numberOfTeams - 1)         # Choose random team B
    
                    for i in range(numberOfRounds):
        
                        if abs(S[teamA][i]) <> teamB + 1:               # If team A and team B are not playing each other in round i
                            
                            newS[[teamA,teamB],i] =  newS[[teamB,teamA],i]      # Swap their values (swap their opponents)
                            
                            formerAdversaryTeamA = abs(S[teamA][i]) - 1         # Gets former opponent of team A
                            formerAdversaryTeamB = abs(S[teamB][i]) - 1         # Gets former opponent of team B
                            
                            # Now the former opponent of team A plays B at home or away
                            if S[formerAdversaryTeamA][i] > 0:
            
                                newS[formerAdversaryTeamA][i] = teamB + 1       
            
                            else:
                
                                newS[formerAdversaryTeamA][i] = -(teamB + 1)
                            
                            # Now the former opponent of team B plays A at home or away
                            if S[formerAdversaryTeamB][i] > 0:
            
                                newS[formerAdversaryTeamB][i] = teamA + 1
            
                            else:
                
                                newS[formerAdversaryTeamB][i] = -(teamA + 1)
                    
                
                elif chooseMove == 3:   # Partial Swap Rounds
                    
                    newS = np.copy(S)
                    
                    team = random.randint(0,numberOfTeams - 1)          # Choose random team
                    roundAindex = random.randint(0,numberOfRounds - 1)  # Choose random round A
                    roundBindex = random.randint(0,numberOfRounds - 1)  # Choose random round B
                    
                    startCircuit = abs(S[team][roundAindex])
                    finishCircuit = abs(S[team][roundBindex])
      
                    currentTeam = startCircuit
                    currentRound = roundBindex
                    
                    # Swaps values of Round A and B for the chosen team
                    newS[team,[roundAindex,roundBindex]] =  newS[team,[roundBindex,roundAindex]]
                    
                    # Now you must figure out the other teams that you have to swap to fix the schedule, and swap their values
                    while currentTeam <> finishCircuit:
                        
                        index = currentTeam - 1
                        
                        newS[index,[roundAindex,roundBindex]] =  newS[index,[roundBindex,roundAindex]]
                        
                        currentTeam = abs(S[currentTeam - 1][currentRound])
        
                        if currentRound == roundBindex:
            
                            currentRound = roundAindex
            
                        else:
            
                            currentRound = roundBindex
                    
                    index = currentTeam - 1
                    
                    newS[index,[roundAindex,roundBindex]] =  newS[index,[roundBindex,roundAindex]]
                    
                    
                elif chooseMove == 4:   # Partial Swap Teams
                    
                    newS = np.copy(S)
                    
                    round = random.randint(0,numberOfRounds - 1)
                    teamA = random.randint(0,numberOfTeams - 1)
                    teamB = random.randint(0,numberOfTeams - 1)
                    
                    adversaryA = S[teamA][round]
                    adversaryB = S[teamB][round]
                    
                    # If team A and B are not playing each other, execute the swap
                    if abs(adversaryB) <> teamA + 1:
                        
                        # Swap the teams in the selected round
                        newS[[teamA,teamB],round] =  newS[[teamB,teamA],round]
                        
                        affectedTeamA = abs(adversaryA)
                        affectedTeamB = abs(adversaryB)
                            
                        oppositeA = S[affectedTeamA - 1][round]
                        oppositeB = S[affectedTeamB - 1][round]
                        
                        # Fix the problem you created (e.g. the opponent of A now plays B)
                        if oppositeA > 0:
                                
                            newS[affectedTeamA - 1][round] = abs(oppositeB)
            
                        else:
                                
                            newS[affectedTeamA - 1][round] = - abs(oppositeB)
            
                        if oppositeB > 0:
                                
                            newS[affectedTeamB - 1][round] = abs(oppositeA)
                
                        else:
                                
                            newS[affectedTeamB - 1][round] = - abs(oppositeA)
                        
                        
                        currentAdversaryB = adversaryB
                        
                        # Look for problems you generated thoroughout the schedule, and swap them as well
                        while currentAdversaryB <> adversaryA:
        
                            currentAdversaryA = currentAdversaryB
                            
                            # e.g. after doing the first swap, now team A plays team 6 at home twice. So you have to find where A played 6 at home before and swap that entry.
                            i = np.nonzero(S[teamA] == currentAdversaryA)[0][0]
                                    
                            currentAdversaryB = S[teamB][i]
                            
                            newS[[teamA,teamB],i] =  newS[[teamB,teamA],i]
                        
                            affectedTeamA = abs(currentAdversaryA)
                            affectedTeamB = abs(currentAdversaryB)
                            
                            oppositeA = S[affectedTeamA - 1][i]
                            oppositeB = S[affectedTeamB - 1][i]
                            
                            # Fix the problem you created (e.g. the opponent of A now plays B)
                            if oppositeA > 0:
                                
                                newS[affectedTeamA - 1][i] = abs(oppositeB)
            
                            else:
                                
                                newS[affectedTeamA - 1][i] = - abs(oppositeB)
            
                            if oppositeB > 0:
                                
                                newS[affectedTeamB - 1][i] = abs(oppositeA)
                
                            else:
                                
                                newS[affectedTeamB - 1][i] = - abs(oppositeA)
                                    
                
                # Now that you have a new solution, get the number of violations
                numberOfViolations = 0

                for i in range(numberOfTeams):
    
                    count = 0

                    for k in range(1,numberOfRounds):
        
                        if (newS[i][k] > 0 and newS[i][k-1] > 0) or (newS[i][k] < 0 and newS[i][k-1] < 0):
        
                            count += 1
            
                        else:
            
                            count = 0
            
                        if count > 2:
            
                            numberOfViolations += 1
            
                        if abs(newS[i][k]) == abs(newS[i][k-1]):
            
                            numberOfViolations += 1
                
                
                violationsNewS = numberOfViolations
                
                # And get the total distance
                totaldistance = 0
                distanceNewS = np.copy(newS)
                
                for x in range(numberOfTeams):
                    
                    distanceNewS[x] = [x + 1 if i > 0 else abs(i) for i in distanceNewS[x]]
    
                    totaldistance += distance_matrix[x][distanceNewS[x][0]-1]
    
                    for y in range(numberOfRounds - 1):
        
                        totaldistance += distance_matrix[distanceNewS[x][y]-1][distanceNewS[x][y + 1]-1]
        
                    totaldistance += distance_matrix[distanceNewS[x][-1] - 1][x]
                    
                costNewS = totaldistance
                
                # If the solution is infeasible, penalize it.
                if violationsNewS <> 0:
                
                    costNewS = math.sqrt((costNewS**2) + (weight*(1 + math.sqrt(violationsNewS)*math.log(violationsNewS/float(2))))**2)
                
                # If the new solution improves the current solution, or the best feasible solution so far, or the best infeasible solution so far
                if costNewS < costS or (violationsNewS == 0 and costNewS < bestFeasible) or (violationsNewS > 0 and costNewS < bestInfeasible):
                    
                    accept = 1
                    
                # Else, accept with a probability given by exp(-delta/T)    
                else:
                    
                    delta = float(costNewS - costS)
                    probability = math.exp(-(delta/T))
                    chance = random.random()
                
                    if chance < probability:
                    
                        accept = 1
                
                    else:
                    
                        accept = 0
                    
                # If you accepted the solution
                if accept == 1:
                    
                    S = newS
                    
                    violationsS = violationsNewS
                    
                    costS = costNewS
                    
                    # If the new solution is feasible
                    if violationsS == 0:
                        
                        # The new best feasible will be the minimum between the new solution and the best feasible
                        nbf = min(costS, bestFeasible)
                    
                    else:
                        
                        nbi = min(costS, bestInfeasible)
                    
                    # If the new solution is the best feasible or the best infeasible
                    if nbf < bestFeasible or nbi < bestInfeasible:
                        
                        bestTime = time.clock()
                        print str(nbf)+" at "+str(bestTime)     # Print the cost and the time
                        
                        # Reset variables to zero.
                        reheat = 0
                        counter = 0
                        phase = 0
                        
                        # Best temperature will be the current temperature. So when the system reheats, the temperature will be 2*bestTemperature
                        bestTemperature = T
                        
                        # Update best feasible and infeasible costs
                        bestFeasible = nbf
                        bestInfeasible = nbi
                        
                        # Strategic oscilation:
                        # If the new solution is feasible, decrease the weight
                        if violationsS == 0:
                            
                            weight = weight/teta
                        
                        # Else, increase it.
                        else:
                            
                            weight = weight*teta
              
                
                # If you rejected the move, increment counter.
                else:
                        
                    counter += 1
                
            # If counter exceeded maxC, increment phase    
            phase += 1
            
            # and decrease temperature
            T = T*beta
            
            print "Cooling "+str(phase)+" "+str(T)+" "+str(nbf)+" at "+str(bestTime)
        
        
        # When phase exceeds maxP, reheat the system bringing its temperature back to two times the current best temperature
        reheat += 1
        
        T = 2*bestTemperature
        
        print "Reheating"
        
    
# Starts clock
time.clock()

# Calls function
simulated_annealing(maxP,maxC,maxR,T,beta,weight,teta)


            