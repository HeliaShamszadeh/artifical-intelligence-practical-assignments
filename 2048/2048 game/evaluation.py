import math
import numpy as np
import game_functions as gf


def evaluate_state(board: np.ndarray) -> float:
    """
    Returns the score of the given board state.
    :param board: The board state for which the score is to be calculated.
    :return: The score of the given board state.
    """
    # TODO: Complete evaluate_state function to return a score for the current state of the board
    # Hint: You may need to use the np.nonzero function to find the indices of non-zero elements.
    # Hint: You may need to use the gf.within_bounds function to check if a position is within the bounds of the board.

    UNIFORMITY_WEIGHT = 2.0
    SMOOTHNESS_WEIGHT = 0.2  

    if gf.check_for_win(board):
        return np.inf
    elif gf.check_for_loss(board):
        return -10000

    weights = np.zeros((4,4))
    max_val = pow(3,25)
    for i in range(3, -1, -1):
        for j in range(3, -1, -1):
            if(i % 2 == 0):
                weights[i][j] = max_val
                max_val = max_val/3
            else:
                weights[i][3-j] = max_val
                max_val = max_val/3


    def is_power_of_two(number : int) -> bool:
        return (math.ceil(math.log2(number)) == math.floor(math.log2(number)))

    def Uniformity():
        score = 0
        for i in range(4):
            for j in range(4):
                score += board[i][j] * weights[i][j]
                
            
        for i in range(4):
            for j in range(3):
                if(board[i][j] == board[i][j+1]):
                    score += board[i][j] * 2 * pow(2,8)

        for i in range(3):
            for j in range(4):
                if(board[i][j] == board[i+1][j]):
                    score += board[i][j] * pow(2,8)

        zeros = gf.get_empty_cells(board)
        score += len(zeros) * pow(2,13)         
        return score
    

    
    def Smoothness():
        smoothness_score = 0
        count = 0
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] != 0:
                    current_tile = board[i][j]
                    if j < len(board[i]) - 1 and board[i][j - 1] != 0:
                        diff = abs(current_tile - board[i][j - 1])
                        if diff > 0:
                            if math.log2(diff) > 8:
                            # if not is_power_of_two(diff):
                                smoothness_score -= diff//2
                                
                    if i > 0 and board[i - 1][j] != 0:
                        diff = abs(current_tile - board[i - 1][j])
                        if diff > 0:
                            if math.log2(diff) > 8:
                            # if not is_power_of_two(diff):
                                smoothness_score -= diff//2
        return smoothness_score


    score_uniformity = Uniformity()
    score_smoothness = Smoothness()

    total_score = (UNIFORMITY_WEIGHT * score_uniformity) + (SMOOTHNESS_WEIGHT * score_smoothness)
    return total_score

    # return score_uniformity
  


