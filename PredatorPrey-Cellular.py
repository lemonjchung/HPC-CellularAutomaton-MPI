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

# Initialize font and background color
def showpredatorprey_persist(nx,ny,t):
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

# Initialize Grid and Generation
NX = 80
NY = 80
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