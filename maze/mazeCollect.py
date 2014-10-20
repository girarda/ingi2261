# -*- coding: utf-8 -*-

"""NAMES OF THE AUTHOR(S): Alexandre Girard, Guillaume Croteau"""

from search import *
import copy
import functools

######################  Implement the search #######################

class State:
    def __init__(self, maze, currentPos, chestPos, moneyPos, wallPos, height, width, pruned):
        """
        A state is defined as:
        - The initial maze
        - The current position (x, y)
        - The position of the chest (x, y)
        - The position of the money [(x, y)]
        - The position of the walls [(x, y)]
        - The maze's height
        - The maze's width
        - The position of the pruned's cells
        """
        self.maze = maze
        self.currentPos = currentPos
        self.chestPos = chestPos
        self.moneyPos = moneyPos
        self.wallPos = wallPos
        self.height = height
        self.width = width
        self.pruned = pruned

    def __hash__(self):
        """
        """
        return hash(self.currentPos * 11 + self.chestPos * 13) + hash(sum([m[0] + m[1]*23 for m in self.moneyPos]) * 37)

    def __eq__(self, other):
        """
        Input: other: another State
        Output: boolean representing whether the two states are equal

        Two states are equal if the initial mazes are the same, the current position is the same, and the position of the money are the same
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
        self.initial = State(maze, currentPos, chestPos, moneyPos, wallPos, height, width, set())
        self.initial_number_of_money = len(moneyPos)

    def goal_test(self, state):
        """
        Input: state
        Output: boolean representing whether the state is the goal state
        A state is the goal test if there is no more money to get and the current position == the position of the chest
        """
        return len(state.moneyPos) == 0 and state.currentPos == state.chestPos

    def successor(self, state):
        """
        Input: state
        Output: states reachable from state

        We only need to iterate through the empty cells adjacent to the current position
        """
        for adjacent_position in self.find_adjacent_empty_positions(state):
            newState = self.move(state, adjacent_position)
            self.number_explored_nodes+=1
            yield None, newState

    def move(self, state, adjPos):
        """
        Move from the state's current position to adjPos
        Prune cells to eliminate symmetrical states
        If adjPos contains money, the money is removed from the new state and the pruned cells set is emptied
        Assume can move there
        """
        newState = State(state.maze, state.currentPos, state.chestPos, state.moneyPos.copy(), state.wallPos, state.height, state.width, state.pruned.copy())

        self.prune(newState, adjPos)

        newState.currentPos = adjPos
        if adjPos in newState.moneyPos:
            newState.moneyPos.remove(adjPos)
            newState.pruned = set()

        return newState

    def prune(self, state, adjPos):
        """
        Prune cells to avoid exploring symmetrical states.
        By assuming that we will no go backwards unless there is a wall or 
        we get a money (and therefore our current goal changes), we can avoid going
        into cells that are not in the direction we are currently going.

        This is a simplification of the Jump point Search optimization (without the long jumps).
        """
        if state.currentPos[0] < adjPos[0]:
            tmp = state.currentPos
            while tmp not in state.wallPos and tmp and tmp[0] >= 0:
                state.pruned.add(tmp)
                tmp = (tmp[0]-1, tmp[1])
        if state.currentPos[0] > adjPos[0]:
            tmp = state.currentPos
            while tmp not in state.wallPos and tmp and tmp[0] < state.height:
                state.pruned.add(tmp)
                tmp = (tmp[0] + 1, tmp[1])
        if state.currentPos[1] < adjPos[1]:
            tmp = state.currentPos
            while tmp not in state.wallPos and tmp and tmp[1] >= 0:
                state.pruned.add(tmp)
                tmp = (tmp[0], tmp[1] - 1)
        if state.currentPos[1] > adjPos[1]:
            tmp = state.currentPos
            while tmp not in state.wallPos and tmp and tmp[1] < state.width:
                state.pruned.add(tmp)
                tmp = (tmp[0], tmp[1] + 1)

    def find_adjacent_empty_positions(self, state):
        """
        Return a list of the empty cells adjacent to the state's current position
        """
        currentPos = state.currentPos
        adjPos = []

        if currentPos[0] > 0:
            if (currentPos[0]-1, currentPos[1]) not in state.wallPos and (currentPos[0]-1, currentPos[1]) not in state.pruned:
                adjPos.append((currentPos[0]-1, currentPos[1]))
        if currentPos[0] < state.height -1:
            if (currentPos[0]+1, currentPos[1]) not in state.wallPos and (currentPos[0]+1, currentPos[1]) not in state.pruned:
                adjPos.append((currentPos[0]+1, currentPos[1]))
        if currentPos[1] > 0:
            if (currentPos[0], currentPos[1]-1) not in state.wallPos and (currentPos[0], currentPos[1]-1) not in state.pruned:
                adjPos.append((currentPos[0], currentPos[1]-1))
        if currentPos[1] < state.width - 1:
            if (currentPos[0], currentPos[1]+1) not in state.wallPos and (currentPos[0], currentPos[1]+1) not in state.pruned:
                adjPos.append((currentPos[0], currentPos[1]+1))
        return adjPos

    def h(self, node):
        """
        Returns the max value of the different heuristics used.
        Currently, only one heuristic is used at a given time.
        If there is still money in the maze, we use a modification of the minimum spanning tree
        If there is no more money, we use the manathan_distance between the current position and the position of the chest
        """
        state = node.state

        heuristics = []
        dist_current_chest = self.manathan_distance(state, state.currentPos, state.chestPos)

        if len(state.moneyPos) > 0:
            heuristics.append(self.min_spanning_tree_total_length(state))
        else:
            heuristics.append(dist_current_chest)

        return max(heuristics)

    def min_spanning_tree_total_length(self, state):
        """
        Returns the distance of the minimum spanning tree between all the money +
        the distance between the current position and the nearest money +
        the distance between the chest position and the money it is nearest to
        """
        edges = [] #(p1, p2, length)

        dist_current_money = map(functools.partial(self.manathan_distance, state, state.currentPos), state.moneyPos)
        dist_chest_money = map(functools.partial(self.manathan_distance, state, state.chestPos), state.moneyPos)
        for money in state.moneyPos:
            for other_money in state.moneyPos:
                if other_money != money:
                    edges.append((other_money, money, self.manathan_distance(state, other_money, money)))

        edges.sort(key=lambda tup: tup[2])

        s = {}

        for money in state.moneyPos:
            s[money] = set([money])

        MST_edges = []
        nodes = {}

        length = min(dist_current_money) + min(dist_chest_money)

        for e in edges:
            if e[1] not in s[e[0]]:
                s[e[0]] |= s[e[1]]

                for connected_nodes in s[e[0]]:
                    s[connected_nodes] |= s[e[0]]
                length += e[2]

        return length

    def manathan_distance(self, state, p1, p2):
        """
        Returns the manathan distance between two points (x, y)
        """
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

###################### Launch the search #########################
# if __name__ == "__main__":
problem=MazeCollect(sys.argv[1])
node=astar_graph_search(problem, problem.h)
path=node.path()
path.reverse()

problem.print_solution(path)