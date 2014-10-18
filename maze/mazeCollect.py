# -*- coding: utf-8 -*-

"""NAMES OF THE AUTHOR(S): Alexandre Girard, Guillaume Croteau"""

from search import *
import copy
import functools

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
        with open(init, 'r') as content_file:
            self.initial_file = content_file.read()
        lines = [line.strip('\n') for line in open(init)]
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
        self.initial_number_of_money = len(moneyPos)

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
        newState = State(state.maze, state.currentPos, state.chestPos, state.moneyPos.copy(), state.wallPos, state.height, state.width)
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

    def h(self, node):
        state = node.state

        heuristics = []
        dist_current_chest = self.manathan_distance(state.currentPos, state.chestPos)

        if len(state.moneyPos) > 0:
            #dist_current_money = map(functools.partial(self.manathan_distance, state.currentPos), state.moneyPos)
            #dist_chest_money = map(functools.partial(self.manathan_distance, state.chestPos), state.moneyPos)
            #dist_money_money = [self.manathan_distance(p1, p2) for p1 in state.moneyPos for p2 in state.moneyPos if p1 != p2]

            # heuristics.append(max(dist_current_money))
            # heuristics.append(len(state.moneyPos))
            # heuristics.append(min(dist_chest_money))
            # heuristics.append(dist_current_chest)
            heuristics.append(self.min_spanning_tree_total_length(state))
            #if len(state.moneyPos) > 1:
            #    heuristics.append(max(dist_money_money))
        else:
            #heuristics.append(self.min_spanning_tree_total_length(state))
            heuristics.append(dist_current_chest)
            #heuristics.append(self.min_spanning_tree_total_length(state))

        return max(heuristics)

    def min_spanning_tree_total_length(self, state):
        edges = [] #(p1, p2, length)

        for money in state.moneyPos:
            edges.append((state.currentPos, money, self.manathan_distance(state.currentPos, money)))
            edges.append((state.chestPos, money, self.manathan_distance(state.chestPos, money)))
            for other_money in state.moneyPos:
                if other_money != money:
                    edges.append((other_money, money, self.manathan_distance(other_money, money)))

        if len(state.moneyPos) == 0:
            edges.append((state.currentPos, state.chestPos, self.manathan_distance(state.currentPos, state.chestPos)))
        edges.sort(key=lambda tup: tup[2])

        s = {}

        for money in state.moneyPos:
            s[money] = set([money])

        s[state.currentPos] = set([state.currentPos])
        s[state.chestPos] = set([state.chestPos])

        length = 0
        for e in edges:
            if e[1] not in s[e[0]]:
                s[e[0]] |= s[e[1]]

                for connected_nodes in s[e[0]]:
                    s[connected_nodes] |= s[e[0]]
                length += e[2]

        return length

    def manathan_distance(self, p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

    def print_solution(self, path):
        """
        Input: In order path to the solution
        Output: Print the solution
        """
        print(self.initial_file)
        for n in path[1:]:
            state = n.state
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
            print("")

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
if __name__ == "__main__":
    problem=MazeCollect(sys.argv[1])
    node=astar_graph_search(problem, problem.h)
    path=node.path()
    path.reverse()

    problem.print_solution(path)