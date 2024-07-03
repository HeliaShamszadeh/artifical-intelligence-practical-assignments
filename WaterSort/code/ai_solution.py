import copy
import heapq


class StateNode:
    def __init__(self, g, h : int, state : list[list[int]], move : tuple[(int, int)], parent : 'Node') -> None:
        self.g = g
        self.h = h
        self.move = move
        self.state = state
        self.parent = parent
    
    def __lt__(self, other):
        return (self.g + self.h) < (other.g + other.h)


class GameSolution:
    """
        A class for solving the Water Sort game and finding solutions(normal, optimal).

        Attributes:
            ws_game (Game): An instance of the Water Sort game which implemented in game.py file.
            moves (List[Tuple[int, int]]): A list of tuples representing moves between source and destination tubes.
            solution_found (bool): True if a solution is found, False otherwise.

        Methods:
            solve(self, current_state):
                Find a solution to the Water Sort game from the current state.
                After finding solution, please set (self.solution_found) to True and fill (self.moves) list.

            optimal_solve(self, current_state):
                Find an optimal solution to the Water Sort game from the current state.
                After finding solution, please set (self.solution_found) to True and fill (self.moves) list.
    """
    
    def __init__(self, game):
        """
            Initialize a GameSolution instance.
            Args:
                game (Game): An instance of the Water Sort game.
        """
        self.ws_game = game  # An instance of the Water Sort game.
        self.moves = []  # A list of tuples representing moves between source and destination tubes.
        self.tube_numbers = game.NEmptyTubes + game.NColor  # Number of tubes in the game.
        self.solution_found = False  # True if a solution is found, False otherwise.
        self.visited_tubes = set()  # A set of visited tubes.
        self.Ncolor = game.NColorInTube
        self.visited = []


    def solve(self, current_state):
        """
            Find a solution to the Water Sort game from the current state.

            Args:
                current_state (List[List[int]]): A list of lists representing the colors in each tube.

            This method attempts to find a solution to the Water Sort game by iteratively exploring
            different moves and configurations starting from the current state.
        """
        
        stack = []
        possible_moves_list = [] # all possible moves in each call are stored in this list
        N_possible_moves = 0 # this represents the number of branches (or next possible states) for each node
        found = False
        is_finished = GameSolution.check_victory(self, current_state)
        if is_finished:
            self.solution_found = True
            return

        for i in range (len(current_state)):
            for j in range(len(current_state)):
                if i == j:
                    continue
                elif len(current_state[i]) == 0:
                    continue
                elif len(current_state[j]) == self.Ncolor:
                    continue
                elif len(current_state[j]) != 0 and current_state[i][-1] != current_state[j][-1]:
                    continue

                N_units_of_top_color = 0
                for h in range (len(current_state[i])-1,-1,-1):
                    if current_state[i][h] != current_state[i][-1]:
                        break
                    N_units_of_top_color += 1
                
                if N_units_of_top_color == len(current_state[i]) and len(current_state[j]) == 0: # this if clause avoids cycle
                    continue

                if (self.Ncolor - len(current_state[j])) < N_units_of_top_color:
                    continue

                next_state = copy.deepcopy(current_state)
                for k in range(N_units_of_top_color):
                    next_state[j].append(next_state[i][-1])
                    next_state[i].pop()

                if self.visited.__contains__(next_state): # if current_state is already discovered (repetitive state), ignore it
                    continue
                self.visited.append(next_state)

                stack.append(next_state)
                found = True
                possible_moves_list . append((i, j))
                N_possible_moves += 1

        if not found: # this means that we cannot reach a new state from this node(state)
            return

        for p in range (N_possible_moves): # iteration on all branches
            self.moves.append(possible_moves_list.pop())
            nexts_state = stack.pop()
            GameSolution.solve(self, nexts_state)
            if self.solution_found:
                return
            self.moves.pop()
            

        
    def check_victory(self, tube_cols):
        """Check if the player has won the game.
                Args:
                    tube_cols (List[List[int]]): A list of lists representing the colors in each tube.

                Returns:
                    bool: True if the player has won, False otherwise.
        """
        won = True
        for i in range(len(tube_cols)):
            if len(tube_cols[i]) > 0:
                if len(tube_cols[i]) != self.Ncolor:
                    won = False
                else:
                    main_color = tube_cols[i][-1]
                    for j in range(len(tube_cols[i])):
                        if tube_cols[i][j] != main_color:
                            won = False
        return won   


    def heuristic(self, state):
        heuristic = 0
        for i in range (len(state)):
            distinct_colors = 0
            colors = []
            if len(state[i]) != 0:
                for j in range (len(state[i])):
                    if state[i][j] not in colors:
                        colors.append(state[i][j])
                        distinct_colors += 1
            heuristic += distinct_colors - 1
        return heuristic

    def possible_moves(self, current_state):
        moves = []
        visiteds = []
        for i in range (len(current_state)):
            for j in range(len(current_state)):
                if i == j:
                    continue
                elif len(current_state[i]) == 0:
                    continue
                elif len(current_state[j]) == self.Ncolor:
                    continue
                elif len(current_state[j]) != 0 and current_state[i][-1] != current_state[j][-1]:
                    continue

                N_units_of_top_color = 0
                for h in range (len(current_state[i])-1,-1,-1):
                    if current_state[i][h] != current_state[i][-1]:
                        break
                    N_units_of_top_color += 1
                
                if N_units_of_top_color == len(current_state[i]) and len(current_state[j]) == 0: # this if clause avoids cycle
                    continue

                if (self.Ncolor - len(current_state[j])) < N_units_of_top_color:
                    continue

                if visiteds.__contains__(current_state): # if current_state is already discovered (repetitive state), ignore it
                    continue
                visiteds.append(current_state)
                moves . append((i, j))
        return moves
        
    def find_next_state(self, current_state, move):
        res = copy.deepcopy(current_state)
        units = 0
        for h in range (len(res[move[0]])-1,-1,-1):
            if res[move[0]][h] != res[move[0]][-1]:
                break
            units += 1
        for i in range (units):
            res[move[1]].append(res[move[0]][-1])
            res[move[0]].pop()
        return res


    def expand_current_state(self, cur_state, cur_state_node, frontiers):
        for m in GameSolution.possible_moves(self, cur_state):
            possible_state = GameSolution.find_next_state(self, cur_state, m)
            if self.visited.__contains__(possible_state) == False:
                h_current = GameSolution.heuristic(self, possible_state)
                next_s = StateNode(cur_state_node.g + 1, h_current, possible_state, m, cur_state_node)
                heapq.heappush(frontiers, (next_s.g + next_s.h, next_s))
                

    def optimal_solve(self, current_state):
        """
            Find an optimal solution to the Water Sort game from the current state.

            Args:
                current_state (List[List[int]]): A list of lists representing the colors in each tube.

            This method attempts to find an optimal solution to the Water Sort game by minimizing
            the number of moves required to complete the game, starting from the current state.
            
        """
        frontiers = []
        h = GameSolution.heuristic(self, current_state)
        current = (h, StateNode(0, h, current_state, None, None))
        heapq.heappush(frontiers, current)
        while frontiers:
            e = heapq.heappop(frontiers)
            cur_state_node = e[1]
            cur_state = cur_state_node.state
            self.visited.append(cur_state)
            is_finished = GameSolution.check_victory(self, cur_state)
            if is_finished:
                self.solution_found = True
                break

            self.expand_current_state(cur_state,cur_state_node, frontiers)

        if self.solution_found:
            while cur_state_node.parent != None:
                self.moves.append(cur_state_node.move)
                cur_state_node = cur_state_node.parent
            self.moves.reverse()
