import random
import time

import config


class Agent:
    ident = 0

    def __init__(self):
        self.id = Agent.ident
        Agent.ident += 1

    def get_chosen_column(self, state, max_depth):
        pass


class Human(Agent):
    pass


class ExampleAgent(Agent):
    def get_chosen_column(self, state, max_depth):
        time.sleep(random.random())
        columns = state.get_possible_columns()
        return columns[random.randint(0, len(columns) - 1)]


def evaluate(state):
    win_value = 1  # Value to reward winning positions (can be any positive number)
    opponent_win_value = -1  # Value to penalize opponent winning positions (can be any negative number)

    win_count = 0
    opponent_win_count = 0

    # Check for winning positions
    for mask in state.win_masks:
        red_match = state.checkers_red & mask
        yellow_match = state.checkers_yellow & mask

        # Count the number of missing pieces for red player
        red_missing_pieces = bin(mask).count('1') - bin(red_match).count('1')
        win_count += max(0, red_missing_pieces)  # Only add positive values

        # Count the number of missing pieces for yellow player
        yellow_missing_pieces = bin(mask).count('1') - bin(yellow_match).count('1')
        opponent_win_count += max(0, yellow_missing_pieces)  # Only add positive values

    # Calculate the difference in win counts
    evaluation = win_value * win_count + opponent_win_value * opponent_win_count

    # center_column = config.N // 2
    # for column in range(config.N):
    #     red_tokens_in_column = bin(state.checkers_red >> (column * config.M)).count('1')
    #     yellow_tokens_in_column = bin(state.checkers_yellow >> (column * config.M)).count('1')
    #     token_difference = red_tokens_in_column - yellow_tokens_in_column
    #     distance_to_center = abs(column - center_column)
    #     evaluation += token_difference / (distance_to_center + 1)  # Avoid division by zero

    print(win_count, opponent_win_count ,evaluation)
    print("\n")

    return evaluation


class MinimaxAgent(Agent):
    def get_chosen_column(self, state, max_depth):
        evaluation, chosen_column = self.minimax(state, max_depth, True)
        return chosen_column if chosen_column is not None else state.get_possible_columns()[0]

    def minimax(self, state, depth, maximizing_player):
        if depth == 0 or state.is_terminal():
            return evaluate(state), None

        possible_columns = state.get_possible_columns()

        if maximizing_player:
            successors = [(c, state.generate_successor_state(c)) for c in possible_columns]
            successors.sort(key=lambda x: (evaluate(x[1]), -abs(config.N // 2 - x[0])))
            max_evaluation = float('-inf')
            max_column = None
            for colum, next_state in successors:
                next_state = state.generate_successor_state(colum)
                next_evaluation, next_colum = self.minimax(next_state, depth - 1, False)
                if next_evaluation > max_evaluation:
                    max_evaluation = next_evaluation
                    max_column = colum
            return max_evaluation, max_column

        else:
            successors = [(c, state.generate_successor_state(c)) for c in possible_columns]
            successors.sort(key=lambda x: (evaluate(x[1]), -abs(config.N // 2 - x[0])))
            min_evaluation = float('inf')
            min_column = None
            for colum, next_state in successors:
                next_state = state.generate_successor_state(colum)
                next_evaluation, next_colum = self.minimax(next_state, depth - 1, True)
                if next_evaluation < min_evaluation:
                    min_evaluation = next_evaluation
                    min_column = colum
            return min_evaluation, min_column
