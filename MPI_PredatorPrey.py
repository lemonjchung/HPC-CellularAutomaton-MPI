import random
import sys
import math
import time
import copy
from mpi4py import MPI
import numpy
import itertools

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()
stat = MPI.Status()

# Initialize Grid and Generation
NX = 80
NY_TOTAL = 80
NY = NY_TOTAL//size+2
generations = 100

if size > NY:
    print("Not enough ROWS")
    exit()

# MPI core functions
def msgUp(subGrid):
	# Sends and Recvs rows with Rank+1
    comm.send(subGrid[NY-2],dest=rank+1)
    subGrid[NY-1]=comm.recv(source=rank+1)
    return 0

def msgDn(subGrid):
	# Sends and Recvs rows with Rank-1
    comm.send(subGrid[1],dest=rank-1)
    subGrid[0] = comm.recv(source=rank-1)
    return 0
    
Predator_prob=0.25
Prey_prob=0.25
Empty_prob = random.random()

# Probability  'X':Prey, 'Y': Predator, 'Z': Empty
# Fill         '~':Prey, '@': Predator, ' ': Empty 
def computeGridPoints(subGrid):
    t = copy.deepcopy(subGrid)
    for i in range(1,NY-1):
        for j in range(1,NX-1):
            # Z+X --> 2X
            if t[i][j]== '~':
                for li in range(-1,2):
                    for lj in range(-1,2):
                        if not (li == 0 and lj == 0):
                            if subGrid[i+li][j+lj] == ' ':
                                if Prey_prob < random.random():
                                    subGrid[i+li][j+lj] = '~'
                                    subGrid[i][j] = '~'
            # X+Y --> 2Y
            if t[i][j] == '~' :
                for li in range(-1,2):
                    for lj in range(-1,2):
                        if not (li == 0 and lj == 0):
                            if t[i+li][j+lj] == '@':
                                if Predator_prob < random.random():
                                    subGrid[i+li][j+lj] = '@'
                                    subGrid[i][j] = '@'
            # Y --> Z
            if t[i][j] == '@':
                if Empty_prob < random.random():
                    subGrid[i][j] = ' '
    return subGrid    

#==== init first array
# '~':Prey, '@': Predator, ' ': Empty 
prey = [['~' for col in range(NX)] for row in range(NY)]
for i in range(-3, 5):
    prey[NY//2+i][NX//2+i] = ' '
for i in range(-3, 5):
    prey[NY//2+i][NX//2] = '@'
#==== init first array

def printf(format, *args):
    sys.stdout.write(format % args)
    
def showpredatorprey(nx,ny,arr):
    for i in range(len(arr)):
        for j in range(nx-1):
            if arr[i][j] == '@':
                printf('\033[41m'"%c "'\033[0m',arr[i][j])
            elif arr[i][j] == '~':
                printf('\033[33m'"%c "'\033[0m',arr[i][j])
            elif arr[i][j] == ' ':
                printf('\033[47m'"%c "'\033[0m',arr[i][j])
            else:
                printf('\033[0m'"%c "'\033[0m',arr[i][j])
        printf("\n")
    printf('\x1b[2J\x1b[H')
    time.sleep(1)


subGrid = prey
for step in range(generations):
    # add predator-prey rules
    computeGridPoints(subGrid)
    # mpi core code
    if rank == 0:
        msgUp(subGrid)
    elif rank == size-1:
        msgDn(subGrid)
    else:
        msgUp(subGrid)
        msgDn(subGrid)
    tempGrid=comm.gather(subGrid[1:NY-1],root=0)
    
    if rank == 0:
        newGrid=list(itertools.chain.from_iterable(tempGrid))
        if step%5 ==0: 
            print("-----------Generation:", step, "---------------")
            showpredatorprey(NX, NY, newGrid)
        