####          High Performance Computing Project - Cellular Automaton
#1. Purpose
# Before running Parallel Programming, find a cellular automaton model and run with a single process.

#2. The model  
# http://iopscience.iop.org/article/10.1088/1751-8113/40/5/002/meta
# Title : The threshold of coexistence and critical behaviour of a predator–prey cellular automaton
#
# We assume that each individual of each species population can reside on the sites of a regular
# square lattice which represents their habitat. A site in the lattice can be in one of three states:
# occupied by a prey individual (X); occupied by a predator individual (Y) or empty (Z). The
# predator–prey probabilistic cellular automaton comprehends the following processes:
#    Z + X → 2X, (1)
#    X + Y → 2Y, (2)
#    Y → Z. (3)

from collections import namedtuple
import random
import sys
import math
import time
import copy

def printf(format, *args):
    sys.stdout.write(format % args)

# Initialize font and background color
def showpredatorprey(nx,ny,t):
    for i in range(ny):
        for j in range(nx):
            if tnew[i][j].STATE == '@':
                printf('\033[41m'"%c "'\033[0m',tnew[i][j].STATE)
            elif tnew[i][j].STATE == '~':
                printf('\033[33m'"%c "'\033[0m',tnew[i][j].STATE)
            elif tnew[i][j].STATE == ' ':
                printf('\033[47m'"%c "'\033[0m',tnew[i][j].STATE)
            else:
                printf('\033[0m'"%c "'\033[0m',tnew[i][j].STATE)
        printf("\n")
    printf('\x1b[2J\x1b[H')
    time.sleep(1)

# Initialize Grid and Generation
NX = 40
NY = 40
generations = 100

# X: Prey, Y: Predator, Z: Empty
Predatorprey = namedtuple('PredatorPrey', 'STATE X Y Z')
tnew = []

for i in range(NY):
    new = []
    for j in range(NX):
        Node = Predatorprey(' ',0.25,0.25,random.random())
        new.append(Node)
    tnew.append(new)

# Fill Prey:'~', Predator:'@', Empty:' ' 
Dinit = 1
for i in range(1,NY-1):
    for j in range(1,NX-1):
        if Dinit - tnew[i][j].Y > 0:
            tnew[i][j] = tnew[i][j]._replace(STATE='~')

# Initialize a first Generation: Start a few Predators and Empties in middle of grid
for i in range(0, 4):
    tnew[NY//2+i][NX//2+i] = tnew[NY//2+i][NX//2+i]._replace(STATE = ' ');
for i in range(-1, 5, 2):
    tnew[NY//2+i][NX//2+3] = tnew[NY//2+i][NX//2+3]._replace(STATE = '@');

# Probability  'X':Prey, 'Y': Predator, 'Z': Empty
# Fill         '~':Prey, '@': Predator, ' ': Empty 
for step in range(generations):
    t = copy.deepcopy(tnew)
    for i in range(1,NY-1):
        for j in range(1,NX-1):
            # Z+X --> 2X
            if t[i][j].STATE == ' ':
                for li in range(-1,2):
                    for lj in range(-1,2):
                        if not (li == 0 and lj == 0):
                            if t[i+li][j+lj].STATE == '~':
                                if t[i+li][j+lj].X < random.random():
                                    tnew[i+li][j+lj] = tnew[i+li][j+lj]._replace(STATE='~')
                                    tnew[i][j] = tnew[i][j]._replace(STATE='~')
            # X+Y --> 2Y
            if t[i][j].STATE == '@':
                for li in range(-1,2):
                    for lj in range(-1,2):
                        if not (li == 0 and lj == 0):
                            if t[i+li][j+lj].STATE == '~':
                                if t[i+li][j+lj].Y < random.random():
                                    tnew[i+li][j+lj] = tnew[i+li][j+lj]._replace(STATE='@')
                                    tnew[i][j] = tnew[i][j]._replace(STATE='@')
            # Y --> Z
            if t[i][j].STATE == '@':
                if t[i][j].Z < random.random():
                    tnew[i][j] = tnew[i][j]._replace(STATE=' ')
 
    if step % 2 == 0:
        showpredatorprey(NX,NY,tnew)
