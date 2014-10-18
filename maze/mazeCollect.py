# -*- coding: utf-8 -*-

"""NAMES OF THE AUTHOR(S): Alexandre Girard, Guillaume Croteau"""

from search import *
import copy

######################  Implement the search #######################

class State:
    def __init__(self, maze, currentPos, chestPos, moneyPos, wallPos, height, width):
        """
        """
        self.maze = maze
        self.currentPos = currentPos
        self.chestPos = chestPos
        self.moneyPos = moneyPos
        self.wallPos = wallPos
        self.height = height
        self.width = width

    def __hash__(self):
        """
        """
        return hash(self.currentPos * 11 + self.chestPos * 13)

    def __eq__(self, other):
        """
        Input: other: another State
        Output: boolean representing whether the two states are equal

        Two states are equal if for every position on the board, they have the same number of tiles
        """
        return self.maze == self.maze and self.currentPos == other.currentPos and self.moneyPos == other.moneyPos

class MazeCollect(Problem):

    def __init__(self,init):
        """
        Input: init file

        Initialize a MazeCollect problem from a file
        The file must follow the following format:
        ###       #    # ## 
          ###   #    # ##   
        # ### # ## # #  ##  
          # # ######   #  # 
         #  ##### ### #  # #
           #  #    # #  # # 
             #   $       #  
        #####  #$  #    $   
        ###    ## # ###     
        # ####    #  # #  ##
          ####  #    ###  ##
         #  # #@    #$##  ##
        ##    # # #   #    #
         ##### #####     #  
           #   ##        #  
             #  ##  # #$ #  
         # #  ## #   # $#  #
        #    #   ##   # # ##
          ####  ## # # #  # 
         #   #   # $ ####  +
        """
        self.number_explored_nodes = 0

        lines = [line for line in open(init)]
        maze = []

        currentPos = (0,0)
        chestPos = (0,0)
        moneyPos = set()
        wallPos = set()
        height = len(lines)
        width = len(lines[0])

        for row, line in enumerate(lines):
            maze.append([])
            for col, char in enumerate(line):
                maze[-1].append(char)
                if char is '@':
                    currentPos = (row, col)
                elif char is '+':
                    chestPos = (row, col)
                elif char is '$':
                    moneyPos.add((row, col))
                elif char is '#':
                    wallPos.add((row, col))
        self.initial = State(maze, currentPos, chestPos, moneyPos, wallPos, height, width)

    def goal_test(self, state):
        """
        Input: state
        Output: boolean representing whether the state is the goal state
        """
        return len(state.moneyPos) == 0 and state.currentPos == state.chestPos

    def successor(self, state):
        """
        Input: state
        Output: states reachable from state

        We only need to iterate through the mergeable positions and try to merge them
        """
        for adjacent_position in self.find_adjacent_empty_positions(state):
            newState = self.move(state, adjacent_position)
            self.number_explored_nodes+=1
            yield None, newState

    def move(self, state, adjPos):
        """
        Assume can move there
        """
        newState = State(state.maze, state.currentPos, state.chestPos, state.moneyPos.copy(), state.wallPos.copy(), state.height, state.width)
        newState.currentPos = adjPos
        if adjPos in newState.moneyPos:
            newState.moneyPos.remove(adjPos)
            # print(newState.moneyPos)
            # print("{}     {} ".format(state.currentPos, adjPos))
        return newState

    def find_adjacent_empty_positions(self, state):
        currentPos = state.currentPos
        adjPos = []

        if currentPos[0] > 0:
            if (currentPos[0]-1, currentPos[1]) not in state.wallPos:
                adjPos.append((currentPos[0]-1, currentPos[1]))
        if currentPos[0] < state.height -1:
            if (currentPos[0]+1, currentPos[1]) not in state.wallPos:
                adjPos.append((currentPos[0]+1, currentPos[1]))
        if currentPos[1] > 0:
            if (currentPos[0], currentPos[1]-1) not in state.wallPos:
                adjPos.append((currentPos[0], currentPos[1]-1))
        if currentPos[1] < state.width - 1:
            if (currentPos[0], currentPos[1]+1) not in state.wallPos:
                adjPos.append((currentPos[0], currentPos[1]+1))
        return adjPos

    def h(self, state):
        return 42

    def print_solution(self, path):
        """
        Input: In order path to the solution
        Output: Print the solution
        """
        for n in path:
            state = n.state
            print(state.currentPos)
            for i in range(state.height):
                for j in range(state.width):
                    if (i,j) in state.moneyPos:
                        print("$", end='')
                    elif i == state.currentPos[0] and j == state.currentPos[1]:
                        print("@", end='')
                    elif i == state.chestPos[0] and j == state.chestPos[1]:
                        print("+", end='')
                    elif (i,j) in state.wallPos:
                        print("#", end='')
                    else:
                        print(" ", end='')
                print("")
            print("==============")

def deepish_copy(org):
    """
    much, much faster than deepcopy, for a dict of the simple python types.
    """
    out = dict().fromkeys(org)
    for k,v in org.items():
        try:
            out[k] = v.copy()   # dicts, sets
        except AttributeError:
            try:
                out[k] = v[:]   # lists, tuples, strings, unicode
            except TypeError:
                out[k] = v      # ints
 
    return out

###################### Launch the search #########################
problem=MazeCollect(sys.argv[1])
node=astar_graph_search(problem, problem.h)
path=node.path()
path.reverse()

problem.print_solution(path)