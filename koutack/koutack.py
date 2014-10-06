'''NAMES OF THE AUTHOR(S): Alexandre Girard, Guillaume Croteau'''

from search import *
import copy

######################  Implement the search #######################

class Koutack(Problem):

    def __init__(self,init):
        self.initial = [line.split() for line in open(init)]
        self.height = len(self.initial)
        self.width = len(self.initial[0]) 

        ll = []
        for i in range(self.height):
            for j in range(self.width):
                if self.initial[i][j] == '.':
                    self.initial[i ][j] = ()
                    ll.append(())
                else:
                    ll.append(tuple(self.initial[i][j]))

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
                        yield "ACTION!", self.merge(state, i, j)

    def get_number_pile(self, state):
        # return len([for pos in state if len()])
        #return len(list(filter(len, state)))
         count = 0
         for line in state:
             if len(line) > 0:
                 count+=1
         return count

    def is_empty(self, state, x, y):
        #print("{}, {}, {}".format(self.height, self.width, len(state)))
        #print("{}, {}".format(x, y))
        return len(state[x * (self.width) + y]) == 0

    def count_adjacent_piles(self, state, x, y):
        count = 0
        if x > 0:
            if not self.is_empty(state, x-1, y):
                count +=1
        if x < self.height-1:
            if not self.is_empty(state, x+1, y):
                count +=1
        if y > 0:
            if not self.is_empty(state, x, y-1):
                count +=1
        if y < self.width-1:
            if not self.is_empty(state, x, y+1):
                count +=1
        return count

    def can_merge(self, state, x, y):
        return self.count_adjacent_piles(state, x, y) >= 2

    def merge(self, state, x, y):
        newState = state[:]
        if x > 0:
            if not self.is_empty(state, x-1, y):
                newState[x * self.width + y] += state[(x-1) * (self.width) + y]
                newState[(x-1) * (self.width) + y] = ()
        if x < self.height-1:
            if not self.is_empty(state, x+1, y):
                newState[x * (self.width) + y] += state[(x+1) * (self.width) + y]
                newState[(x+1) * (self.width) + y] = ()
        if y > 0:
            if not self.is_empty(state, x, y-1):
                newState[x * (self.width) + y] += state[x * (self.width) + (y-1)]
                newState[x * (self.width) + (y-1)] = ()
        if y < self.width-1:
            if not self.is_empty(state, x, y+1):
                newState[x * (self.width) + y] += state[x * (self.width) + (y+1)]
                newState[x * (self.width) + (y+1)] = ()
        
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
###################### Launch the search #########################
if __name__ == '__main__':
    problem=Koutack(sys.argv[1])

    node=iterative_deepening_search(problem)
    path=node.path()
    path.reverse()

    problem.printSolution(path)