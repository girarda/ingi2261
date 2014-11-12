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
        return depth >= 2 or state[0].is_finished() 

    def evaluate(self, state):
        """The evaluate function must return an integer value
        representing the utility function of the board.
        """
        import zombies

        board = state[0]

        surundingNecromencerWeight = 100

        weightPieces = {zombies.NECROMANCER:50, zombies.HUGGER:10, zombies.JUMPER:20, zombies.CREEPER:5, zombies.SPRINTER:20}

        movesScoreP1 = 0
        movesScoreP2 = 0

        scoreOfPiecesP1 = 0
        scoreOfPiecesP2 = 0

        for position in board.pieces:
            piece = board.pieces[position]

            if type(piece) is list:
                piece = piece[-1]

            pieceID = abs(piece)

            moves = []

            if piece == zombies.NECROMANCER:
                moves = board.get_necromancer_moves(position)
            elif piece == zombies.HUGGER:
                moves = board.get_hugger_moves(position)
            elif piece == zombies.JUMPER:
                moves = board.get_jumper_moves(position)
            elif piece == zombies.CREEPER:
                moves = board.get_creeper_moves(position)
            elif piece == zombies.SPRINTER:
                moves = board.get_sprinter_moves(position)
            else:
                continue

            pieceScore = weightPieces[pieceID]
            print("Piece score {}".format(pieceScore))
            if piece > 0:
                movesScoreP2 += pieceScore * len(moves)
                scoreOfPiecesP2 += pieceScore
            else:
                movesScoreP1 += pieceScore * len(moves)
                scoreOfPiecesP1 += pieceScore

        movesScore = 0
        if self.player == zombies.PLAYER1:
            print("Moves score {}".format(movesScoreP1))
            movesScore = movesScoreP1 #- movesScoreP2
            scoreOfPiece = scoreOfPiecesP1
        else:
            movesScore = movesScoreP2 #- movesScoreP1
            print("Moves score {}".format(movesScoreP2))
            scoreOfPiece = scoreOfPiecesP2

        movesWeight = 0.1

        moveValue = movesWeight * movesScore

        score = surundingNecromencerWeight * board.get_score(self.player) + moveValue * 0.3 + scoreOfPiece * 0.8
        print(moveValue)
        return score

    def play(self, board, player, step, time_left):
        """This function is used to play a move according
        to the board, player and time left provided as input.
        It must return an action representing the move the player
        will perform.
        """
        import minimax
        self.player = player
        self.time_left = time_left
        state = (board, player, step)
        return minimax.search(state, self)


if __name__ == "__main__":
    zombies.agent_main(Agent())
