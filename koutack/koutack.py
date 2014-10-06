'''NAMES OF THE AUTHOR(S): Alexandre Girard, Guillaume Croteau'''

from search import *
import copy

######################  Implement the search #######################

class Koutack(Problem):

    def __init__(self,init):
        self.initial = [line.split() for line in open(init)]
        self.height = len(self.initial)
        self.width = len(self.initial[0]) 
        self.explored_states = {}
        ll = {}
        for i in range(self.height):
            for j in range(self.width):
                if self.initial[i][j] != '.':
                    ll[i*self.width + j] = tuple(self.initial[i][j])

        self.initial = ll
        #print(self.initial)
        #exit()
        ## Sum of piles = 1
        self.goal = 1
    
    def goal_test(self, state):
        return self.get_number_pile(state) == 1

    def successor(self, state):
        for i in range(self.height):
            for j in range(self.width):
                if(self.is_empty(state, i, j)):
                    if self.can_merge(state, i, j):
                        newState = self.merge(state, i, j)
                        if not self.is_similar_to_previously_explored_states(newState):
                            #print(len(self.explored_states))
                            self.explored_states[self.get_number_pile(newState)].append(newState)
                            yield None, newState
                        #else:
                            #print("SAME STATE!!")

    def is_similar_to_previously_explored_states(self, state):
            is_similar = False
            number_piles = self.get_number_pile(state)
            if number_piles not in self.explored_states:
                self.explored_states[number_piles] = []
            for explored_state in self.explored_states[number_piles]:
                is_similar = explored_state.keys() == state.keys()
                if is_similar:
                    is_similar = all(len(explored_state[pos]) == len(state[pos]) for pos in state)
                if is_similar:
                    #print("state:")
                    #print(state)
                    #print("explored:")
                    #print(explored_state)
                    #input()
                    return True
            return False

    def get_number_pile(self, state):
        # return len([for pos in state if len()])
        #return len(list(filter(len, state)))
         return len(state)

    def is_empty(self, state, x, y):
        return (x * self.width + y) not in state

    def count_adjacent_piles(self, state, x, y):
        count = 0
        if x > 0:
            if ((x-1)*self.width + y) in state:
                count +=1
        if x < self.height-1:
            if ((x+1)*self.width + y) in state:
                count +=1
        if y > 0:
            if (x*self.width + y-1) in state:
                count +=1
        if y < self.width-1:
            if (x*self.width + y+1) in state:#not 
                count +=1
        # print(count)
        # if x == 1 and y == 0:
        #     exit(0)
        return count

    def can_merge(self, state, x, y):
        return self.count_adjacent_piles(state, x, y) >= 2

    def merge(self, state, x, y):
        newState = deepish_copy(state)
        newState[x * self.width + y] = ()
        if x > 0:
            if not self.is_empty(state, x-1, y):
                newState[x * self.width + y] += state[(x-1) * (self.width) + y]
                newState.pop((x-1) * (self.width) + y, None)
        if x < self.height-1:
            if not self.is_empty(state, x+1, y):
                newState[x * (self.width) + y] += state[(x+1) * (self.width) + y]
                newState.pop((x+1) * (self.width) + y, None)
        if y > 0:
            if not self.is_empty(state, x, y-1):
                newState[x * (self.width) + y] += state[x * (self.width) + (y-1)]
                newState.pop(x * (self.width) + (y-1), None)
        if y < self.width-1:
            if not self.is_empty(state, x, y+1):
                newState[x * (self.width) + y] += state[x * (self.width) + (y+1)]
                newState.pop(x * (self.width) + (y+1), None)

        return newState

    def printSolution(self, path):
        for n in path:
            #print(len(n.state))
            for x in range(self.height):
                grid = ""
                for y in range(self.width):
                    #print(n.state[i*self.width + j])

                    # print("width: {}".format(self.width))
                    # print("height: {}".format(self.height))
                    # print("{}".format(x))
                    if x * self.width + y not in n.state:
                        grid += ". "
                    else:
                        element = n.state[x * self.width + y] 
                        if len(element) == 0:
                           grid += ". "
                        elif len(element) == 1:
                           grid += element[0] + " "
                        else:
                           grid += "["
                           for i in range(len(element)):
                               grid += element[i]
                               if i != len(element) - 1:
                                   grid += ","
                           grid += "] "
                print(grid)
            print("")

def unshared_copy(inList):
    if isinstance(inList, list):
        return list( map(unshared_copy, inList) )
    return inList

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
if __name__ == '__main__':
    problem=Koutack(sys.argv[1])

    node=breadth_first_tree_search(problem)
    path=node.path()
    path.reverse()

    problem.printSolution(path)