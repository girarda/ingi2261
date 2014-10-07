'''NAMES OF THE AUTHOR(S): Alexandre Girard, Guillaume Croteau'''

from search import *
import copy

######################  Implement the search #######################

class State:
    def __init__(self, piles, mergeables):
        self.piles = piles
        self.mergeables = mergeables

    def __hash__(self):
        return hash(frozenset(self.piles))

    def __eq__(self, other):
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
        self.initial = tuple([line.split() for line in open(init)])
        self.height = len(self.initial)
        self.width = len(self.initial[0])
        piles = {}
        empties = set()
        mergeables = set()
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
        return self.get_number_pile(state.piles) == 1

    def successor(self, state):
        for mergeable_position in state.mergeables:
            newState = self.merge(state, mergeable_position[0], mergeable_position[1])
            yield None, newState

    def get_number_pile(self, piles):
        return len(piles)

    def is_empty(self, piles, x, y):
        return (x, y) not in piles

    def count_adjacent_piles(self, piles, x, y):
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
        return self.count_adjacent_piles(piles, x, y) >= 2

    def merge(self, state, x, y):
        newState = State(deepish_copy(state.piles), copy.copy(state.mergeables))
        
        newState.piles[x,y] = ()

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

        for m in state.mergeables:
            if not self.can_merge(newState.piles, m[0], m[1]):
                newState.mergeables.remove(m)
    
        return newState

    def printSolution(self, path):
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
    '''
    much, much faster than deepcopy, for a dict of the simple python types.
    '''
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

problem.printSolution(path)