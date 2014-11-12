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
import random 

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
        import random
        actions = state[0].get_actions(state[1], state[2])
        r = random.uniform(0,1)
        if actions and r > 0.5:
            random.shuffle(actions)
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
        return depth >= 2 or state[0].is_finished() or (self.time_left - self.previous_time) > 3

    def evaluate(self, state):
        """The evaluate function must return an integer value
        representing the utility function of the board.
        """
        import zombies

        board = state[0]

        weightPieces = {zombies.NECROMANCER:50, zombies.HUGGER:50, zombies.JUMPER:20, zombies.CREEPER:50, zombies.SPRINTER:2}
        moveFunctionsMao = {zombies.NECROMANCER:board.get_necromancer_moves, zombies.HUGGER:board.get_hugger_moves, zombies.JUMPER:board.get_jumper_moves, zombies.CREEPER:board.get_creeper_moves, zombies.SPRINTER:board.get_sprinter_moves}


        scoreWeight = 1000
        score = board.get_score(self.player)

        piecesValue = 0
        piecesValueWeight = 10

        huggedValue = 0
        huggedWeight = 1

        numberMovesWeight = 0.1

        enemyNecroPosition = None

        for position in board.pieces:
            piece = board.pieces[position]
            if type(piece) is list:
                pass
            else:
                if piece * self.player < 0:
                    piece_type = abs(piece)
                    if piece_type == zombies.NECROMANCER:
                        enemyNecroPosition = position
                        

        emptyNeighbors = []

        if enemyNecroPosition:
            emptyNeighbors = board.get_neighbouring_tiles(enemyNecroPosition)
            emptyNeighbors = [n for n in emptyNeighbors if board.pieces[n] == zombies.EMPTY]


        if enemyNecroPosition:
            if len(board.get_non_empty_neighbours(enemyNecroPosition)) == 6:
                print("SUP")
                return 999999999999
            # elif len(board.get_non_empty_neighbours(enemyNecroPosition)) == 5:
            #     score = 99999999

        for position in board.pieces:
            piece = board.pieces[position]
            if type(piece) is list:
                for p in piece:
                    if p * self.player > 0:
                        pieceType = p * self.player
                        piecesValue += weightPieces[pieceType]

                        print(piece_type)
                        if pieceType == 1:#zombies.NECROMANCER:
                            print(len(board.get_non_empty_neighbours(position)))
                            if len(board.get_non_empty_neighbours(position)) == 6:
                                print("DUMBASS")
                                return -1
                    else:
                        pieceType = abs(p)
                        huggedValue += weightPieces[pieceType]
            else:
                if piece * self.player > 0:
                    pieceType = piece * self.player
                    piecesValue += weightPieces[pieceType]

                    # if enemyNecroPosition:
                    #     dists = [d for d in map(len, board.find_all_paths(position, enemyNecroPosition, position))]
                    #     if len(dists) > 0:
                    #         dist = min(dists)
                    #         if dist != 1:
                    #             print("duh")
                    #             piecesValue -= (dist * 1000)

                    # for neighbor in emptyNeighbors:
                    #     numberOfPath = len(board.find_all_paths(position, neighbor, position))
                    #     piecesValue += numberOfPath / 50


        # for position in board.pieces:

        value = score  * scoreWeight + piecesValue * piecesValueWeight + huggedValue * huggedWeight

        print("value: {}".format(value))
        return value

    def play(self, board, player, step, time_left):
        """This function is used to play a move according
        to the board, player and time left provided as input.
        It must return an action representing the move the player
        will perform.
        """
        import minimax
        self.player = player

        if self.previous_time:
            self.previous_time = self.time_left
        else:
            self.previous_time = time_left
        state = (board, player, step)
        return minimax.search(state, self)


if __name__ == "__main__":
    zombies.agent_main(Agent())
