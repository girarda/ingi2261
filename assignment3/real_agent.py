#!/usr/bin/env python3
"""
Zombies agent.
Copyright (C) 2014, <<<<<<<<<<< YOUR NAMES HERE >>>>>>>>>>>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, see <http://www.gnu.org/licenses/>.

"""

import zombies
import minimax

class Agent(zombies.Agent, minimax.Game):
    """This is the skeleton of an agent to play the Zombies game."""

    def __init__(self, name="Agent"):
        self.name = name
        self.player = zombies.PLAYER1
        self.time_left = 0
        self.previous_time = None

    def successors(self, state):
        """The successors function must return (or yield) a list of
        pairs (a, s) in which a is the action played to reach the
        state s; s is the new state, i.e. a triplet (b, p, st) where
        b is the new board after the action a has been played,
        p is the player to play the next move and st is the next
        step number.
        """
        actions = state[0].get_actions(state[1], state[2])
        for a in actions:
            newState = self.apply_action(state, a)
            yield a, newState

    def apply_action(self, state, action):
        import zombies

        newBoard= state[0].clone()
        
        if action[0] == 'P':
            newBoard.place_piece(action[1], action[2], state[1])
        elif action[0] == 'M':
            newBoard.move_piece(action[1], action[2], state[1])
        else:
            pass

        if state[1] is zombies.PLAYER1:
            newPlayer = zombies.PLAYER2
        else:
            newPlayer = zombies.PLAYER1
        newStep = state[2]+1

        return (newBoard, newPlayer, newStep)

    def cutoff(self, state, depth):
        """The cutoff function returns true if the alpha-beta/minimax
        search has to stop; false otherwise.
        """
        cutoffTime = 5
        MAX_STEP_TIME = 60
        step = state[2]
        # print("time diff: {}".format(self.time_left - self.previous_time))
        return depth >= 2 or state[0].is_finished() or (self.time_left - self.previous_time) > 3# or time.time() - self.time > cutoffTime * MAX_STEP_TIME / step

    def evaluate(self, state):
        """The evaluate function must return an integer value
        representing the utility function of the board.
        """
        import zombies

        # print("SELF: {}".format(self.player))

        board = state[0]

        for position in board.pieces:
            if type(board.pieces[position]) is int:
                if abs(board.pieces[position]) == zombies.NECROMANCER:
                    if (board.pieces[position] > 0 and self.player < 0) or (board.pieces[position] < 0 and self.player > 0):
                        return len(board.get_non_empty_neighbours(position)) + board.get_score(self.player)

        score = board.get_score(self.player)

        return score

    def play(self, board, player, step, time_left):
        """This function is used to play a move according
        to the board, player and time left provided as input.
        It must return an action representing the move the player
        will perform.
        """
        import minimax
        self.player = player

        print("time_left: {}".format(time_left))

        if self.previous_time:
            self.previous_time = self.time_left
        else:
            self.previous_time = time_left
        self.time_left = time_left
        state = (board, player, step)

        ret = minimax.search(state, self)
        # print("ret: {}".format(ret))
        return ret


if __name__ == "__main__":
    zombies.agent_main(Agent())
