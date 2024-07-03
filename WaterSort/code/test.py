# import copy
# import heapq
# from typing import TYPE_CHECKING

# solution_found = False
# moves = []
# class StateNode:
#     def __init__(self, g, h : int, state : list[list[int]], move : tuple[(int, int)], parent : 'Node') -> None:
#         self.g = g
#         self.h = h
#         self.move = move
#         self.state = state
#         self.parent = parent

#     def __lt__(self, other):
#     # Compare based on the total cost g
#         return (self.g + self.h) < (other.g + other.h)

# def solve(current_state):
#     stack = []
#     possible_moves_list=[]
#     """
#         Find a solution to the Water Sort game from the current state.

#         Args:
#             current_state (List[List[int]]): A list of lists representing the colors in each tube.

#         This method attempts to find a solution to the Water Sort game by iteratively exploring
#         different moves and configurations starting from the current state.
#     """
    
#     possible_moves = 0
#     found = False
#     is_finished = check_victory(current_state)
#     solution_found = False
#     if is_finished:
#         solution_found = True
#         return
#     for i in range (len(current_state)):
#         for j in range(len(current_state)):
#             if i == j:
#                 continue
#             elif len(current_state[i]) == 0:
#                 continue
#             elif len(current_state[j]) == 2:
#                 continue
#             elif len(current_state[j]) != 0 and current_state[i][-1] != current_state[j][-1]:
#                 continue
#             last_index = 0
            
#             if len(current_state[i]) > 1:
#                 for h in range (len(current_state[i])-1,-1,-1):
#                     if current_state[i][h] != current_state[i][-1]:
#                         break
#                     last_index += 1
#             elif len(current_state[i]) == 1:
#                 last_index = 1
                
#             if (2 - len(current_state[j]))< last_index:
#                 continue
#             print(last_index)

#             new_state = copy.deepcopy(current_state)
#             for k in range(last_index):
#                 new_state[j].append(current_state[i][-1])
#                 new_state[i].pop()

#             print(new_state)
#             stack.append(new_state)
#             found = True
#             possible_moves_list.append((i, j))
#             possible_moves += 1
#     if not found:
#         return
#     for p in range (possible_moves):
#         moves.append(possible_moves_list.pop())
#         last_state = stack.pop()
#         solve(last_state)
#         if solution_found:
#             return
#         moves.pop()
        

    
# def check_victory(tube_cols):
#     """Check if the player has won the game.
#             Args:
#                 tube_cols (List[List[int]]): A list of lists representing the colors in each tube.

#             Returns:
#                 bool: True if the player has won, False otherwise.
#     """
#     won = True
#     for i in range(len(tube_cols)):
#         if len(tube_cols[i]) > 0:
#             if len(tube_cols[i]) != 2:
#                 won = False
#             else:
#                 main_color = tube_cols[i][-1]
#                 for j in range(len(tube_cols[i])):
#                     if tube_cols[i][j] != main_color:
#                         won = False
#     return won       

# # solve([[0,2], [2, 1], [1,0], []])

# def heuristic(state):
#         all = 0
#         for i in range (len(state)):
#             distinct_colors = 0
#             colors = []
#             if len(state[i]) != 0:
#                 for j in range (len(state[i])):
#                     if state[i][j] not in colors:
#                         colors.append(state[i][j])
#                         distinct_colors += 1
#                 all += distinct_colors - 1
#         return all

# def heuristic2_water_sort(current_state):
#     num_matching_pairs = 0
#     for i in range(len(current_state)):
#         for j in range(i + 1, len(current_state)):
#             if current_state[i] and current_state[j] and current_state[i][-1] == current_state[j][-1]:
#                 num_matching_pairs += 1
#     return num_matching_pairs


# def possible_moves(current_state):
#     moves = []
#     visiteds = []
#     for i in range (len(current_state)):
#         for j in range(len(current_state)):
#             if i == j:
#                 continue
#             elif len(current_state[i]) == 0:
#                 continue
#             elif len(current_state[j]) == 7:
#                 continue
#             elif len(current_state[j]) != 0 and current_state[i][-1] != current_state[j][-1]:
#                 continue

#             N_units_of_top_color = 0
#             for h in range (len(current_state[i])-1,-1,-1):
#                 if current_state[i][h] != current_state[i][-1]:
#                     break
#                 N_units_of_top_color += 1
            
#             if N_units_of_top_color == len(current_state[i]) and len(current_state[j]) == 0: # this if clause avoids cycle
#                 continue

#             if (7 - len(current_state[j])) < N_units_of_top_color:
#                 continue
#             moves . append((i, j))
#     return moves
    
# def find_next_state(current_state, move):
#     res = copy.deepcopy(current_state)
#     units = 0
#     for h in range (len(res[move[0]])-1,-1,-1):
#         if res[move[0]][h] != res[move[0]][-1]:
#             break
#         units += 1
#     for i in range (units):
#         res[move[1]].append(res[move[0]][-1])
#         res[move[0]].pop()
#     return res




# moves1 = []

# def optimal_solve1(current_state):
#     """
#         Find an optimal solution to the Water Sort game from the current state.

#         Args:
#             current_state (List[List[int]]): A list of lists representing the colors in each tube.

#         This method attempts to find an optimal solution to the Water Sort game by minimizing
#         the number of moves required to complete the game, starting from the current state.
        
#     """
#     visiteds = []
#     frontiers = []
#     h = heuristic(current_state)
#     cur_state = (h, StateNode(0, h, current_state, None, None))
#     heapq.heappush(frontiers, cur_state)
#     while frontiers:
#         e = heapq.heappop(frontiers)
#         cur_state_node = e[1]
#         cur_state = cur_state_node.state
#         visiteds.append(cur_state)
#         is_finished = check_victory(cur_state)
#         if is_finished:
#             solution_found = True
#             break

#         for m in possible_moves(cur_state):
#             possible_state = find_next_state(cur_state, m)
#             if visiteds.__contains__(possible_state) == False:
#                 h_current = heuristic(possible_state)
#                 next_s = StateNode(cur_state_node.g + 1,h_current, possible_state, m, cur_state_node)
#                 heapq.heappush(frontiers, (next_s.g + h_current, next_s))

#     if solution_found:
#         while cur_state_node.parent != None:
#             moves1.append(cur_state_node.move)
#             cur_state_node = cur_state_node.parent
#         moves1.reverse()
#     print(len(moves1))
#     print(moves1)

# def optimal_solve2(current_state):
#     """
#         Find an optimal solution to the Water Sort game from the current state.

#         Args:
#             current_state (List[List[int]]): A list of lists representing the colors in each tube.

#         This method attempts to find an optimal solution to the Water Sort game by minimizing
#         the number of moves required to complete the game, starting from the current state.
        
#     """
#     visiteds = set()
#     frontiers = []
#     h = heuristic2_water_sort(current_state)
#     cur_state = (h + 0, StateNode(0, h, current_state, None, None))
#     heapq.heappush(frontiers, cur_state)
#     while frontiers:
#         e = heapq.heappop(frontiers)
#         cur_state_node = e[1]
#         cur_state = cur_state_node.state
#         visiteds.append(cur_state)
#         is_finished = check_victory(self, cur_state)
#         if is_finished:
#             solution_found = True
#             break

#         for m in possible_moves(self, cur_state):
#             possible_state = find_next_state(self, cur_state, m)
#             if visiteds.__contains__(possible_state) == False:
#                 h_current = heuristic2_water_sort(possible_state)
#                 next_s = StateNode(cur_state_node.g + 1, h_current, possible_state, m, cur_state_node)
#                 heapq.heappush(frontiers, (next_s.g + h_current, next_s))

#     if solution_found:
#         while cur_state_node.parent != None:
#             moves.append(cur_state_node.move)
#             cur_state_node = cur_state_node.parent
#         moves.reverse()
#     print(len(moves1))
#     print(moves1)
    
# optimal_solve1([[5, 2, 5, 5, 1, 3, 1], [2, 3, 0, 0, 3, 4, 6], [2, 4, 6, 5, 4, 3, 4], [6, 1, 0, 0, 1, 1, 0], [6, 2, 4, 2, 6, 6, 2], [5, 4, 0, 3, 3, 0, 1], [5, 2, 4, 1, 3, 5, 6], [], []] )

# # optimal_solve2([[5, 2, 5, 5, 1, 3, 1], [2, 3, 0, 0, 3, 4, 6], [2, 4, 6, 5, 4, 3, 4], [6, 1, 0, 0, 1, 1, 0], [6, 2, 4, 2, 6, 6, 2], [5, 4, 0, 3, 3, 0, 1], [5, 2, 4, 1, 3, 5, 6], [], []] )