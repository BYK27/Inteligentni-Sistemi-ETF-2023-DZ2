import random
import time

import config
import heapq

from state import State


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


class MinimaxAgent2(Agent):
    def get_chosen_column(self, state, max_depth):
        evaluation, column = self.minimax(state, max_depth, True)
        return column if column is not None else state.get_possible_columns()[0]

    def minimax(self, state, depth, maximizing_player):
        if depth == 0 or state.is_terminal():
            return self.static_evaluation(state, maximizing_player), None

        nodes = self.add_nodes(state,
                               maximizing_player)  # nodes to be evaluated, expanded in descending heuristic order

        print("U minimaksu\n")

        if maximizing_player:
            max_evaluation = float('-inf')
            max_column = None
            while nodes:
                current_evaluation, current_state, current_column = heapq.heappop(nodes)[1]
                next_evaluation, next_state, next_column = self.minimax(current_state, depth - 1, not maximizing_player)
                if next_evaluation > max_evaluation:
                    max_evaluation = next_evaluation
                    max_column = current_column
            return max_evaluation, max_column

        else:
            min_evaluation = float('inf')
            min_column = None
            while nodes:
                current_evaluation, current_state, current_column = heapq.heappop(nodes)[1]
                next_evaluation, next_state, next_column = self.minimax(current_state, depth - 1, not maximizing_player)
                if next_evaluation < min_evaluation:
                    min_evaluation = next_evaluation
                    min_column = current_column
            return min_evaluation, min_column

    def add_nodes(self, state, maximizing_player):
        nodes = []  # node - evaluation, state, column
        possible_columns = state.get_possible_columns()
        print(possible_columns)
        for column in possible_columns:
            possible_state = state.generate_successor_state(column)
            possible_evaluation = self.static_evaluation(possible_state, maximizing_player)
            node = (possible_evaluation, possible_state, column)
            heapq.heappush(nodes, node)
        return nodes

    # TODO: define the evaluation by the difference of tiles
    # the lower the value the higher the priority
    def static_evaluation(self, state, maximizing_player):

        player_points = 0
        opponent_points = 0

        # print(state.win_masks)
        # print("red:" , state.checkers_red)
        # print("yellow:" , state.checkers_yellow ,"\n")

        for mask in state.win_masks:

            if maximizing_player is True and (state.checkers_red and mask) == mask:
                return -100
            elif maximizing_player is False and (state.checkers_yellow and mask) == mask:
                return -100

            red_match = state.checkers_red & mask
            yellow_match = state.checkers_yellow & mask
            # Count the number of missing pieces for red player
            red_missing_pieces = bin(mask).count('1') - bin(red_match).count('1')
            player_points += max(0, red_missing_pieces)  # Only add positive values

            # Count the number of missing pieces for yellow player
            yellow_missing_pieces = bin(mask).count('1') - bin(yellow_match).count('1')
            opponent_points += max(0, yellow_missing_pieces)  # Only add positive values

            # Calculate the difference in win counts
        evaluation = -(player_points - opponent_points)
        print(evaluation)
        return evaluation


def static_evaluation(state):
    player_points = 0
    opponent_points = 0

    # print(state.win_masks)
    # print("red:" , state.checkers_red)
    # print("yellow:" , state.checkers_yellow ,"\n")

    # points only count for winning positions
    for mask in state.win_masks:
        red_match = state.checkers_red & mask
        yellow_match = state.checkers_yellow & mask
        red_missing_pieces = bin(mask).count('1') - bin(red_match).count('1')
        player_points += bin(red_match).count('1')

        yellow_missing_pieces = bin(mask).count('1') - bin(yellow_match).count('1')
        opponent_points += bin(yellow_match).count('1')

    evaluation = player_points - opponent_points
    # print(evaluation)
    return evaluation


class MinimaxAgentSimple(Agent):

    def get_chosen_column(self, state, max_depth):
        # print(max_depth)
        evaluation, column = self.minimax(state, max_depth, True)
        print("Evaluation: ", evaluation)
        return column

    def minimax(self, state, depth, maximizing_player):

        # print("in minimax" ,depth)

        if depth == 0 or state.get_state_status() is not None:
            # print("in minimax")
            if maximizing_player:
                return static_evaluation(state), None
            else:
                return -1 * static_evaluation(state), None

        if maximizing_player:
            max_eval = float('-inf')
            max_column = None
            possible_columns = state.get_possible_columns()
            for column in possible_columns:
                next_eval, _, = self.minimax(state.generate_successor_state(column), depth - 1, not maximizing_player)
                if next_eval > max_eval:
                    max_eval = next_eval
                    max_column = column
            # print("Max", max_eval, "Depth: " , depth)
            return max_eval, max_column

        else:
            max_eval = float('inf')
            max_column = None
            possible_columns = state.get_possible_columns()
            for column in possible_columns:
                next_eval, _, = self.minimax(state.generate_successor_state(column), depth - 1, not maximizing_player)
                if next_eval < max_eval:
                    max_eval = next_eval
                    max_column = column
            # print("Min", max_eval, "Depth: " , depth)
            return max_eval, max_column

class MinimaxABAgentSimple(Agent):

    def get_chosen_column(self, state, max_depth):
        # print(max_depth)
        _, column = self.minimax(state, max_depth, True, float('-inf'), float('inf'))
        return column

    def minimax(self, state, depth, maximizing_player, alfa, beta):

        # print("in minimax" ,depth)

        if depth == 0 or state.get_state_status() is not None:
            # print("in minimax")
            if maximizing_player:
                return static_evaluation(state), None
            else:
                return static_evaluation(state), None

        if maximizing_player:
            max_eval = float('-inf')
            max_column = None
            possible_columns = state.get_possible_columns()
            for column in possible_columns:
                next_eval, _, = self.minimax(state.generate_successor_state(column), depth - 1, not maximizing_player,
                                             alfa, beta)
                if next_eval > max_eval:
                    max_eval = next_eval
                    max_column = column
                alfa = max(alfa, max_eval)
                if beta <= alfa:
                    break

            print("Max", max_eval, "Depth: ", depth)
            return max_eval, max_column

        else:
            max_eval = float('inf')
            max_column = None
            possible_columns = state.get_possible_columns()
            for column in possible_columns:
                next_eval, _, = self.minimax(state.generate_successor_state(column), depth - 1, not maximizing_player,
                                             alfa, beta)
                if next_eval < max_eval:
                    max_eval = next_eval
                    max_column = column
                beta = min(beta, max_eval)
                if beta <= alfa:
                    break
            print("Min", max_eval, "Depth: ", depth)
            return max_eval, max_column

class MinimaxAgent(Agent):

    def get_chosen_column(self, state, max_depth):
        # print(max_depth)
        _, column = self.minimax(state, max_depth, True)
        return column

    def minimax(self, state, depth, maximizing_player):

        # print("in minimax" ,depth)

        nodes = []
        possible_columns = state.get_possible_columns()
        for column in possible_columns:
            weight = get_weight(column)
            node = (static_evaluation(state.generate_successor_state(column)), weight, state, column)
            heapq.heappush(nodes, node)

        if depth == 0 or state.get_state_status() is not None:
            # print("in minimax")
            if maximizing_player:
                return static_evaluation(state), None
            else:
                return -1 * static_evaluation(state), None

        if maximizing_player:
            max_eval = float('-inf')
            max_column = None

            while nodes:
                next_eval, _, next_state, next_column = heapq.heappop(nodes)
                if next_eval > max_eval:
                    max_eval = next_eval
                    max_column = next_column
            return max_eval, max_column

        else:
            max_eval = float('inf')
            max_column = None

            while nodes:
                next_eval, _, next_state, next_column = heapq.heappop(nodes)
                if next_eval < max_eval:
                    max_eval = next_eval
                    max_column = next_column
            return max_eval, max_column
class MinimaxABAgent(Agent):

    def get_chosen_column(self, state, max_depth):
        # print(max_depth)
        _, column = self.minimax(state, max_depth, True, float('-inf'), float('inf'))
        return column

    def minimax(self, state, depth, maximizing_player, alfa, beta ):

        # print("in minimax" ,depth)

        nodes = []
        possible_columns = state.get_possible_columns()
        for column in possible_columns:
            weight = get_weight(column)
            node = (static_evaluation(state.generate_successor_state(column)), weight, state, column)
            heapq.heappush(nodes, node)

        if depth == 0 or state.get_state_status() is not None:
            # print("in minimax")
            if maximizing_player:
                return static_evaluation(state), None
            else:
                return -1 * static_evaluation(state), None

        if maximizing_player:
            max_eval = float('-inf')
            max_column = None

            while nodes:
                next_eval, _, next_state, next_column = heapq.heappop(nodes)
                if next_eval > max_eval:
                    max_eval = next_eval
                    max_column = next_column
                alfa = max(alfa, max_eval)
                if beta <= alfa:
                    break
            return max_eval, max_column

        else:
            max_eval = float('inf')
            max_column = None

            while nodes:
                next_eval, _, next_state, next_column = heapq.heappop(nodes)
                if next_eval < max_eval:
                    max_eval = next_eval
                    max_column = next_column
                beta = min(beta, max_eval)
                if beta <= alfa:
                    break
            return max_eval, max_column


def get_weight(column):
    if column == 3: weight = 0
    elif column == 2: weight = 1
    elif column == 4: weight = 2
    elif column == 1: weight = 3
    elif column == 5: weight = 4
    elif column == 0: weight = 5
    elif column == 6: weight = 6

    return weight
