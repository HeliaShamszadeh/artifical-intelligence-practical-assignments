# empty_cells_count = len(np.where(board == 0)[0])
# nonzero_positions = np.transpose(np.nonzero(board))
# max_tile = np.max(board)

import numpy as np

import game_functions as gf


def most_same_neighbor_block(board: np.ndarray, i , j, same_neighbor_score):
    # Check right neighbor
    if j < 3 and board[i][j + 1] != 0:
        same_neighbor_score -= abs(board[i][j] - board[i][j + 1])
    
    # Check down neighbor
    if i < 3 and board[i + 1][j] != 0:
        same_neighbor_score -= abs(board[i][j] - board[i + 1][j])

def most_sorted_board(board: np.ndarray, i, j, sorted_board_score):
    # Check right neighbor
    if j < 3 and board[i][j] >= board[i][j + 1]:
        sorted_board_score += board[i][j + 1] - board[i][j]
    if j < 3 and board[i][j] < board[i][j + 1]:
        sorted_board_score += board[i][j] - board[i][j + 1]
    
    # Check down neighbor
    if i < 3 and board[i][j] >= board[i + 1][j]:
        sorted_board_score += board[i + 1][j] - board[i][j]
    if i < 3 and board[i][j] < board[i + 1][j]:
        sorted_board_score += board[i][j] - board[i + 1][j]

def evaluate_state(board: np.ndarray) -> float:
    """
    Returns the score of the given board state.
    :param board: The board state for which the score is to be calculated.
    :return: The score of the given board state.
    """
    # TODO: Complete evaluate_state function to return a score for the current state of the board
    # Hint: You may need to use the np.nonzero function to find the indices of non-zero elements.
    # Hint: You may need to use the gf.within_bounds function to check if a position is within the bounds of the board.
    
    same_neighbor_score = 0
    sorted_board_score = 0
    total = 0 
    nonzero_positions = np.transpose(np.nonzero(board))

    for i, j in nonzero_positions:
        factor = 0
        if (j % 2 == 1):
            factor = (i + (4 * j)) * 20
        else:
            factor = ((3 - i) + (4 * j)) * 20
        total += board[i][j] * factor

        most_same_neighbor_block(board, i, j, same_neighbor_score)
        most_sorted_board(board, i, j, sorted_board_score)


    return total + same_neighbor_score + sorted_board_score

    # raise NotImplementedError("Evaluation function not implemented yet.")


def maximizer_node(self, board: np.ndarray, depth: int):
        """
        Returns the best move for the given board state and turn.
        ...
        :type depth: int
        :type board: np.ndarray
        :param board: The board state for which the best move is to be found.
        :param depth: Depth to which agent takes actions for each move
        :return: Returns the move with highest score, for the given board state.
        """
        
        # TODO: Complete maximizer_node function to return the move with highest score, for the given board state.
        # Hint: You may need to use the gf.get_moves function to get all possible moves.
        # Hint: You may need to use the gf.add_new_tile function to add a new tile to the board.
        # Hint: You may need to use the np.copy function to create a copy of the board.
        # Hint: You may need to use the np.inf constant to represent infinity.
        # Hint: You may need to use the max function to get the maximum value in a list.
        best_score = -np.inf
        best_action = None

        moves = gf.get_moves()
        for move in moves:

            new_board, new_move_made, new_score = move(np.copy(board))

            if new_move_made:
                if move != gf.move_left and move != gf.move_up:
                    new_score += self.expectimax(new_board, depth - 1, 0)[0]

                    if new_score > best_score:
                        best_score = new_score
                        best_action = move
                else:
                    if (move != gf.move_left):
                        new_score += self.expectimax(new_board, depth - 1, 0)[0]

                        if new_score > best_score:
                            best_score = new_score
                            best_action = move
                    else:
                        if best_action is None:
                            score, _ = self.expectimax(new_board, depth - 1, 0)
                            best_score = score
                            best_action = move
        return best_score, best_action


        raise NotImplementedError("Maximizer node not implemented yet.")