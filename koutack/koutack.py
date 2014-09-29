'''NAMES OF THE AUTHOR(S): ...'''

from search import *
import copy

######################  Implement the search #######################

class Koutack(Problem):

    def __init__(self,init):
        self.initial = [line.split() for line in open(init)]
        for i in range(len(self.initial)):
            for j in range(len(self.initial[0])):
                if self.initial[i][j] == '.':
                    self.initial[i][j] = []
                else:
                    self.initial[i][j] = list(self.initial[i][j])

        ## Sum of piles = 1
        self.goal = 1
    
    def goal_test(self, state):
        return self.get_number_pile(state) == 1

    def successor(self, state):
        for i in range(len(state)):
            for j in range(len(state[0])):
                if(self.is_empty(state, i, j)):
                    if self.can_merge(state, i, j):
                        yield "ACTION!", self.merge(state, i, j)        
    def get_number_pile(self, state):
        count = 0
        for line in state:
            for c in line:
                if len(c) > 0:
                    count+=1
        return count

    def is_empty(self, state, x, y):
        return len(state[x][y]) == 0

    def count_adjacent_piles(self, state, x, y):
        count = 0
        if x > 0:
            if not self.is_empty(state, x-1, y):
                count +=1
        if x < len(state)-1:
            if not self.is_empty(state, x+1, y):
                count +=1
        if y > 0:
            if not self.is_empty(state, x, y-1):
                count +=1
        if y < len(state)-1:
            if not self.is_empty(state, x, y+1):
                count +=1
        return count

    def can_merge(self, state, x, y):
        return self.count_adjacent_piles(state, x, y) >= 2

    def merge(self, state, x, y):
        newState = copy.deepcopy(state)
        if x > 0:
            if not self.is_empty(state, x-1, y):
                newState[x][y] += state[x-1][y]
                newState[x-1][y] = []
        if x < len(state)-1:
            if not self.is_empty(state, x+1, y):
                newState[x][y] += state[x+1][y]
                newState[x+1][y] = []
        if y > 0:
            if not self.is_empty(state, x, y-1):
                newState[x][y] += state[x][y-1]
                newState[x][y-1] = []
        if y < len(state[0])-1:
            if not self.is_empty(state, x, y+1):
                newState[x][y] += state[x][y+1]
                newState[x][y+1] = []
        return newState




###################### Launch the search #########################
problem=Koutack(sys.argv[1])
#succ = problem.successor(problem.initial)
#for act, state in succ:
    #print(state, '\n')
#print(problem.initial)
#print(problem.goal_test(problem.initial))
#example of bfs search
node=depth_limited_search(problem)
#example of print
path=node.path()
path.reverse()
for n in path:
    print(n.state) #assuming that the __str__ function of states output the correct format
        
