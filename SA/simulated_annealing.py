# A previous version of the code was broken down into many different functions and files. It was better organized and easier to understand.
# But function calls are expensive in Python: they take a lot of time. So the current version is not as clean as the other one, but it's faster.

""" 
Program is organized as follows:

Part 1) Import of libraries and input file
Part 2) Definition of function to generate canonical pattern and initial solution
Part 3) Simulated Annealing
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


# Variables for Simulated Annealing, set manually
maxP = 1250
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

"""
Part 2
"""

# Function to create canonical pattern or 1-factorization
def findCanonicalPattern(numberOfTeams, numberOfRounds): 
       
    x = numberOfRounds/2
    y = numberOfTeams/2
    z = 2    
    
    # Creates 3-dimensional array. For example, for 4 teams: x = 2, y = 3, z = 2. So E = [[[0,0],[0,0]],[[0,0],[0,0]],[[0,0],[0,0]]]
    E = np.zeros((x,y,z)) 
    
    for i in range(numberOfRounds/2): 
        
        E[i][0][:]=[numberOfTeams,i + 1]        # The first edge of a round is the last team (e.g. team 4) playing team i + 1 
        
        for k in range(numberOfTeams/2-1):      # Then to fill the last edges, use functions F1 and F2
            
            E[i][k+1][:]=[F1(i + 1, k + 1, numberOfTeams), F2(i + 1, k + 1, numberOfTeams)] 
         
    return(E) 

    
# Defines F1 used to find the canonical pattern   
def F1(i,k,numberOfTeams):
    
    if i + k < numberOfTeams:
        
        return(i + k)
        
    else:
        
        return(i + k - numberOfTeams + 1)
    
    
# Defines F2 used to find the canonical pattern     
def F2(i,k,numberOfTeams):
    
    if i - k > 0:
        
        return(i - k)
        
    else:
        
        return(i - k + numberOfTeams - 1)
        

# Defines function to get initial solution for Simulated Annealing
def getInitialSolution(numberOfTeams):
    
    # The solution will be a 2-dimensional array (a.k.a. the schedule)
    solution = np.zeros((numberOfTeams,numberOfRounds), dtype=int)
    
    # Finds canonical pattern to creat a feasible single round robin schedule
    games = findCanonicalPattern(numberOfTeams, numberOfRounds)
    
    # Creates first half of the tournament
    for i in range(numberOfRounds/2):
        
        for k in range(numberOfTeams/2):
            
            # Every edge of the canonical pattern is a game between the two nodes
            edge = games[i][k]
            
            teamA = int(edge[0])
            teamB = int(edge[1])
            
            # One team plays at home, one team plays away
            solution[teamA - 1][i] = teamB
            solution[teamB - 1][i] = - teamA
    
    # To create second half, mirror the first half inverting the signs
    temp = solution.copy()
    temp = -1*np.roll(temp, numberOfRounds/2, axis=1)
    solution = solution+temp

    return(solution)

"""
Part 3
"""
               
# Defines function for Simulated Annealing
def simulated_annealing(maxP,maxC,maxR,T,beta,weight,teta):
    
    # Generates a initial solution
    S = getInitialSolution(numberOfTeams)
    S = np.array(S)
    
    # To calculate number of violations, sets number of violations to 0
    numberOfViolations = 0

    for i in range(numberOfTeams):
    
        count = 0

        for k in range(1,numberOfRounds):
            
            # If you play two consecutive games at home or aways, increment count by 1. Else, make it 0.
            if (S[i][k] > 0 and S[i][k-1] > 0) or (S[i][k] < 0 and S[i][k-1] < 0):
        
                count += 1
            
            else:
            
                count = 0
            
            # If count is bigger than 2, you're playing more than three consecutive games away or at home. So increments number of violations by 1.
            if count > 2:
            
                numberOfViolations += 1
            
            # If you're playing the same team in two consecutive rounds, increment number of violations by 1.
            if abs(S[i][k]) == abs(S[i][k-1]):
            
                numberOfViolations += 1
    
    violationsS = numberOfViolations
    
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
            
    # If solution is infeasible, penalize it by increasing its cost
    if violationsS <> 0:
                
        costS = math.sqrt((costS**2) + (weight*(1 + math.sqrt(violationsS)*math.log(violationsS/float(2))))**2)
        
    # Sets best feasible solution so far to a very high number
    bestFeasible = 9999999
    nbf = 9999999
    
    # Sets best infeasible solution so far to a very high number
    bestInfeasible = 9999999
    nbi = 9999999
    
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
                        print "Cost = "+str(nbf)+" at "+str(bestTime)+" seconds"     # Print the cost and the time
                        
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
            
            print "Cooling "+str(phase)+" T = "+str(T)+" Cost = "+str(nbf)+" at "+str(bestTime)+" seconds"
        
        
        # When phase exceeds maxP, reheat the system bringing its temperature back to two times the current best temperature
        reheat += 1
        
        T = 2*bestTemperature
        
        print "Reheating"
        
    
# Starts clock
time.clock()

# Calls function
simulated_annealing(maxP,maxC,maxR,T,beta,weight,teta)


            