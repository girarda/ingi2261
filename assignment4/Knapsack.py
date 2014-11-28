# -*- coding: utf-8 -*-

"""NAMES OF THE AUTHOR(S): Alexandre Girard, Guillaume Croteau"""

from search import *
import copy
import functools

######################  Implement the search #######################

class Item:
    def __init__(self, weight, value):
        self.weight = weight
        self.value = value

    def __repr__(self):
        return "(w: {}, v: {})".format(self.weight, self.value)

class State:
    def __init__(self, items, capacity):
        self.items = items
        self.capacity = capacity

    def __hash__(self):
        return hash(self.capacity) + hash(sum([i.value for i in self.items]) * 13) + hash(sum([i.weight for i in self.items]) * 37)

    def __eq__(self, other):
        return self.items == other.items and self.capacity == other.capacity

    def addItem(self, newItem):
        self.items.add(newItem)

    def removeItem(self, item):
        self.items.remove(item)

    def replaceItem(self, oldItem, newItem):
        self.items.remove(oldItem)
        self.items.add(newItem)

    def getWeight(self):
        return sum([item.weight for item in self.items])

    def getValue(self):
        return sum([item.value for item in self.items])

    def isConsistent(self):
        return self.getWeight() <= self.capacity

    def __repr__(self):
        return str(self.items)

class Knapsack(Problem):

    def __init__(self,f):
        lines = [line.strip('\n') for line in open(f)]

        N = int(lines[0])
        capacity = int(lines[-1])
        self.items = set([Item(int(line.split()[1]), int(line.split()[2])) for line in lines[1:-1]])

        self.initial = self.constructInitialState(capacity)


    def goal_test(self, state):
        return state.getWeight() <= state.capacity

    def addItem(self, state, item):
        newState = State(state.items.copy(), state.capacity)
        if item not in newState.items:
            newState.addItem(item)
            return newState
        return None

    def removeItem(self, state, item):
        newState = State(state.items.copy(), state.capacity)
        if item in newState.items:
            newState.removeItem(item)
            return newState
        return None

    def replaceItem(self, state, oldItem, newItem):
        newState = State(state.items.copy(), state.capacity)
        if oldItem in newState.items and newItem not in newState.items:
            newState.replaceItem(oldItem, newItem)
            return newState
        return None

    def successor(self, state):
        batshitlist = []
        addItems = map(functools.partial(self.addItem, state), self.items)
        addItems = [state for state in addItems if state is not None and state.isConsistent()]
        batshitlist += addItems

        removeItems = map(functools.partial(self.removeItem, state), self.items)
        removeItems = [state for state in removeItems if state is not None and state.isConsistent()]
        batshitlist += removeItems

        replaceItems = [self.replaceItem(state, oldItem, newItem) for oldItem in self.items for newItem in self.items]
        replaceItems = [state for state in replaceItems if state is not None and state.isConsistent()]
        batshitlist += addItems


        for state in batshitlist:
            print(state)

        for state in batshitlist:
            yield None, state

    def constructInitialState(self, capacity):
        itemsSortedByWeight = list(self.items)
        itemsSortedByWeight.sort(key=lambda x: x.weight)

        knapsack = State(set(), capacity)
        for item in itemsSortedByWeight:
            if knapsack.getWeight() + item.weight < knapsack.capacity:
                knapsack.addItem(item)
            else:
                break
        return knapsack

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

    def value(self, state):
        return state.getValue()

    def print_solution(self, path):
        """
        Input: In order path to the solution
        Output: Print the solution
        """
        # print(self.initial_file)
        # for n in path[1:]:
        #     state = n.state
        #     for i in range(state.height):
        #         for j in range(state.width):
        #             if (i,j) in state.moneyPos:
        #                 print("$", end='')
        #             elif i == state.currentPos[0] and j == state.currentPos[1]:
        #                 print("@", end='')
        #             elif i == state.chestPos[0] and j == state.chestPos[1]:
        #                 print("+", end='')
        #             elif (i,j) in state.wallPos:
        #                 print("#", end='')
        #             else:
        #                 print(" ", end='')
        #         print("")
        #     print("")

###################### Launch the search #########################
if __name__ == "__main__":
    problem=Knapsack(sys.argv[1])
    node = random_walk(problem)
    # node=astar_graph_search(problem, problem.h)
    # path=node.path()
    # path.reverse()
    print(node.state.getValue())
    print(node.state)

    # problem.print_solution(path)