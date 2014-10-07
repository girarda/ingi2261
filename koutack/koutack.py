# -*- coding: utf-8 -*-

"""NAMES OF THE AUTHOR(S): Alexandre Girard, Guillaume Croteau"""

from search import *
import copy

######################  Implement the search #######################

class State:
    def __init__(self, piles, mergeables):
        """
        Input: piles: map of position -> tiles, mergeables: set of mergeable positions
        """
        self.piles = piles
        self.mergeables = mergeables

    def __hash__(self):
        """
        Hash the State using its piles and mergeables
        """
        return hash(frozenset(self.piles) + frozenset(self.mergeables))

    def __eq__(self, other):
        """
        Input: other: another State
        Output: boolean representing whether the two states are equal

        Two states are equal if for every position on the board, they have the same number of tiles
        """
        if isinstance(other, self.__class__):
            is_similar = False
            number_piles = len(self.piles)
            is_similar = other.piles.keys() == self.piles.keys()
            if is_similar:
                is_similar = all(len(other.piles[pos]) == len(self.piles[pos]) for pos in self.piles)
            if is_similar:
                return True
        return False

class Koutack(Problem):

    def __init__(self,init):
        """
        Input: init file

        Initialize a Koutack problem from a file
        The file must follow the following format:
        . a . . . .
        . b . c . .
        d . . e . .
        f . . g h .
        . i j . . .

        From this file, a State consisting of a map of the tiles and mergeable positions is generated.
        """
        self.initial = tuple([line.split() for line in open(init)])
        self.height = len(self.initial)
        self.width = len(self.initial[0])
        piles = {}
        empties = set()
        mergeables = set()
        self.number_explored_nodes = 0
        for i in range(len(self.initial)):
            for j in range(len(self.initial[0])):
                if self.initial[i][j] == '.':
                    empties.add((i,j))
                else:
                    piles[(i, j)] = tuple(self.initial[i][j])
        
        for empty_position in empties:
            if self.can_merge(piles, empty_position[0], empty_position[1]):
                mergeables.add(empty_position)

        self.initial = State(piles, mergeables)

        ## Sum of piles = 1
        self.goal = 1

    def goal_test(self, state):
        """
        Input: state
        Output: boolean representing whether the state is the goal state
        """
        return self.get_number_pile(state.piles) == 1

    def successor(self, state):
        """
        Input: state
        Output: states reachable from state

        We only need to iterate through the mergeable positions and try to merge them
        """
        for mergeable_position in state.mergeables:
            newState = self.merge(state, mergeable_position[0], mergeable_position[1])
            self.number_explored_nodes+=1
            yield None, newState

    def get_number_pile(self, piles):
        """
        Input: piles
        Output: number of piles on the board
        """
        return len(piles)

    def is_empty(self, piles, x, y):
        return (x, y) not in piles

    def count_adjacent_piles(self, piles, x, y):
        """
        Input: piles, position to merge
        Output: number of neighbors with tiles around the position
        """
        count = 0
        if (x-1, y) in piles:
            count +=1
        if (x+1, y) in piles:
                count +=1
        if (x, y-1) in piles:
                count +=1
        if (x,y+1) in piles:
                count +=1
        return count

    def can_merge(self, piles, x, y):
        """
        Input: piles, position to merge
        Output: boolean representing whether it is possible to merge to the position
        """
        return self.count_adjacent_piles(piles, x, y) >= 2

    def merge(self, state, x, y):
        """
        Input: State, position where to merge the tiles
        Precondition: The position must be empty and have more than one adjacent tile
        Output: New state with applied merge
        """
        newState = State(deepish_copy(state.piles), copy.copy(state.mergeables))
        
        newState.piles[x,y] = ()

        # For each neighbors, move tiles to merged position and remove neighbor from tiles map
        if x > 0:
            if not self.is_empty(state.piles, x-1, y):
                newState.piles[x, y] += state.piles[x-1, y]
                newState.piles.pop((x-1, y))
        if x < self.height-1:
            if not self.is_empty(state.piles, x+1, y):
                newState.piles[x, y] += state.piles[x+1, y]
                newState.piles.pop((x+1, y))
        if y > 0:
            if not self.is_empty(state.piles, x, y-1):
                newState.piles[x, y] += state.piles[x, y-1]
                newState.piles.pop((x, y-1))
        if y < self.width-1:
            if not self.is_empty(state.piles, x, y+1):
                newState.piles[x, y] += state.piles[x, y+1]
                newState.piles.pop((x, y+1))

        # For each neighbors, if it is a mergeable position, add it to the newState's mergeable map
        if x > 0:
            if self.can_merge(newState.piles, x-1, y):
                newState.mergeables.add((x-1,y))
        if x < self.height-1:
            if self.can_merge(newState.piles, x+1, y):
                newState.mergeables.add((x+1,y))
        if y > 0:
            if self.can_merge(newState.piles, x, y-1):
                newState.mergeables.add((x,y-1))
        if y < self.width-1:
            if self.can_merge(newState.piles, x, y+1):
                newState.mergeables.add((x,y+1))

        # Make sure every mergeable positions are still mergeable
        for m in state.mergeables:
            if not self.can_merge(newState.piles, m[0], m[1]):
                newState.mergeables.remove(m)
    
        return newState

    def print_solution(self, path):
        """
        Input: In order path to the solution
        Output: Print the solution
        """
        for n in path:
            grid = ""

            for i in range(self.height):
                for j in range(self.width):
                    element = ""
                    if (i,j) in n.state.piles:
                        if len(n.state.piles[(i,j)]) > 1:
                            print("[", end="")
                            for k in n.state.piles[(i,j)]:
                                print(k, end="")
                                if k != n.state.piles[(i,j)][-1]:
                                    print(",", end="")
                            print("]", end="")
                        else:
                            print(n.state.piles[(i,j)][0], end="")
                    else:
                        print(".", end="")
                    if j < self.width-1:
                        print(" ", end="")
                    else:
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
problem=Koutack(sys.argv[1])
node=breadth_first_graph_search(problem)
path=node.path()
path.reverse()

problem.print_solution(path)