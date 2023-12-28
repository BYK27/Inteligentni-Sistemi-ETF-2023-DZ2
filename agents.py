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


def static_evaluation(state, maximizing_player):
    # za crvenog brojimo svaku win_mask koja kad se & sa checkers_yel daje 0 (svaka pobeda koja nije nemoguca zbog vec postavljenih zutih zetona), a za zutog brojimo svaku win_mask koja kad se & sa checkers_red daje 0
    score_red = 0
    score_yellow = 0

    # print(state.win_masks)
    # print("red:" , state.checkers_red)
    # print("yellow:" , state.checkers_yellow ,"\n")

    if state.get_state_status() == State.RED:
        return 1000 - bin(state.checkers_red).count('1')

    elif state.get_state_status() == State.YEL:
        return -1000 + bin(state.checkers_yellow).count('1')

    # points only count for winning positions
    for mask in state.win_masks:
        red_match = state.checkers_red & mask
        yellow_match = state.checkers_yellow & mask


        if red_match == 0: score_yellow += 1
        if yellow_match == 0: score_red += 1

    return score_red - score_yellow

def obliteration_evaluation(state, maximizing_player):
    score = 0

    if state.get_state_status() == State.RED:
        return 1000 - bin(state.checkers_red).count('1')

    elif state.get_state_status() == State.YEL:
        return -1000 + bin(state.checkers_yellow).count('1')

    # poeni pobednickih pozicija
    for mask in state.win_masks:
        red_match = state.checkers_red & mask
        yellow_match = state.checkers_yellow & mask

        # vise se racunaju potezi koji pobedjuju sa manje zetona
        weight = len([bit for bit in bin(mask) if bit == '1'])

        if red_match == 0:
            score -= weight
        if yellow_match == 0:
            score += weight

    # PENALI
    for mask in state.win_masks:
        if maximizing_player:
            if (state.checkers_yellow & mask == 0) and (state.checkers_red & mask != mask):
                score -= 5  # Penalize for unblocked opponent's win
        else:
            if (state.checkers_red & mask == 0) and (state.checkers_yellow & mask != mask):
                score += 5  # Penalize for unblocked opponent's win

    return score

class MinimaxABAgent(Agent):

    def get_chosen_column(self, state, max_depth):
        # print(max_depth)
        if self.id == 0:
            player = True
        else:
            player = False
        _, column = self.minimax(state, max_depth, player, 0, float('-inf'), float('inf'))
        return column

    def minimax(self, state, depth, maximizing_player, current_depth, alfa, beta):

        print("evaluation state ", state)
        # print("in minimax" ,depth)
        if depth == 0 or state.get_state_status() is not None:
            return static_evaluation(state, maximizing_player), None

        if maximizing_player:
            nodes = []
            possible_columns = state.get_possible_columns()
            for column in possible_columns:
                weight = -1 * get_weight(column)
                new_state = state.generate_successor_state(column)
                node = (
                    static_evaluation(new_state, maximizing_player), weight,
                    new_state,
                    column)
                nodes.append(node)

            max_eval = float('-inf')
            max_column = None

            nodes = sorted(nodes, key=lambda x: (x[0], x[1]))
            print("Player ", maximizing_player, nodes)

            while nodes:
                current_node = nodes.pop()
                _, _, state, column = current_node
                print(current_node)
                next_eval, next_column = self.minimax(state, depth - 1, not maximizing_player, current_depth + 1, alfa,
                                                      beta)
                if next_eval > max_eval:
                    max_eval = next_eval
                    max_column = column
                # print("Max with value: ", max_eval, " at depth ", current_depth, "\n")
                alfa = max(alfa, max_eval)
                if beta <= alfa:
                    break
            return max_eval, max_column

        else:
            nodes = []
            possible_columns = state.get_possible_columns()
            for column in possible_columns:
                weight = get_weight(column)
                new_state = state.generate_successor_state(column)
                node = (
                    static_evaluation(new_state, maximizing_player), weight,
                    new_state,
                    column)
                nodes.append(node)

            min_eval = float('inf')
            min_column = None
            nodes = sorted(nodes, key=lambda x: (x[0], x[1]), reverse=True)
            print("Player ", maximizing_player, nodes)

            while nodes:
                current_node = nodes.pop()
                _, _, state, column = current_node
                print(current_node)
                next_eval, next_column = self.minimax(state, depth - 1, not maximizing_player, current_depth + 1, alfa,
                                                      beta)
                if next_eval < min_eval:
                    min_eval = next_eval
                    min_column = column
                # print("Min with value: ", min_eval, " at depth ", current_depth, "\n")
                beta = min(beta, min_eval)
                if beta <= alfa:
                    break
            return min_eval, min_column


class NegamaxABAgent(Agent):

    def get_chosen_column(self, state, max_depth):
        # print(max_depth)
        if self.id == 0:
            player = True
        else:
            player = False
        _, column = self.negamax(state, max_depth, player, 0, float('-inf'), float('inf'))
        return column

    def negamax(self, state, depth, maximizing_player, current_depth, alfa, beta):

        print("evaluation state ", state)
        # print("in minimax" ,depth)
        if depth == 0 or state.get_state_status() is not None:
            if not maximizing_player: return -1 * static_evaluation(state, maximizing_player), None
            return static_evaluation(state, maximizing_player), None

        nodes = []
        possible_columns = state.get_possible_columns()
        for column in possible_columns:
            if maximizing_player:
                weight = -1 * get_weight(column)
            else:
                weight = get_weight(column)
            new_state = state.generate_successor_state(column)
            node = (
                static_evaluation(new_state, maximizing_player), weight,
                new_state,
                column)
            nodes.append(node)

        max_eval = float('-inf')
        max_column = None

        if maximizing_player:
            nodes = sorted(nodes, key=lambda x: (x[0], x[1]))
        else:
            nodes = sorted(nodes, key=lambda x: (x[0], x[1]), reverse=True)

        print("Player ", maximizing_player, nodes)

        while nodes:
            current_node = nodes.pop()
            _, _, state, column = current_node
            print(current_node)
            next_eval, next_column = self.negamax(state, depth - 1, not maximizing_player, current_depth + 1, -1 * beta,
                                                  -1 * alfa)
            next_eval *= -1
            if next_eval > max_eval:
                max_eval = next_eval
                max_column = column
            # print("Max with value: ", max_eval, " at depth ", current_depth, "\n")
            alfa = max(alfa, max_eval)
            if beta <= alfa:
                break
        return max_eval, max_column


def get_weight(column):
    weight = -1

    if column == 3:
        weight = 0
    elif column == 2:
        weight = 1
    elif column == 4:
        weight = 2
    elif column == 1:
        weight = 3
    elif column == 5:
        weight = 4
    elif column == 0:
        weight = 5
    elif column == 6:
        weight = 6

    return weight


class NegascoutAgent(Agent):
    def get_chosen_column(self, state, max_depth):
        # print(max_depth)
        if self.id == 0:
            player = True
        else:
            player = False
        _, column = self.negamax(state, max_depth, player, 0, float('-inf'), float('inf'))
        return column

    def negamax(self, state, depth, maximizing_player, current_depth, alfa, beta):

        print("evaluation state ", state)
        # print("in minimax" ,depth)
        if depth == 0 or state.get_state_status() is not None:
            if not maximizing_player: return -1 * static_evaluation(state, maximizing_player), None
            return static_evaluation(state, maximizing_player), None

        nodes = []
        possible_columns = state.get_possible_columns()
        for column in possible_columns:
            if maximizing_player:
                weight = -1 * get_weight(column)
            else:
                weight = get_weight(column)
            new_state = state.generate_successor_state(column)
            node = (
                static_evaluation(new_state, maximizing_player), weight,
                new_state,
                column)
            nodes.append(node)

        max_eval = float('-inf')
        max_column = None

        if maximizing_player:
            nodes = sorted(nodes, key=lambda x: (x[0], x[1]))
        else:
            nodes = sorted(nodes, key=lambda x: (x[0], x[1]), reverse=True)

        print("Player ", maximizing_player, nodes)

        first_node = True

        while nodes:
            current_node = nodes.pop()
            _, _, state, column = current_node
            print(current_node)

            if first_node:
                next_eval, next_column = self.negamax(state, depth - 1, not maximizing_player, current_depth + 1, -1 * beta, -1 * alfa)
                first_node = False
            else:
                next_eval, next_column = self.negamax(state, depth - 1, not maximizing_player, current_depth + 1, -1 * alfa - 1, -1 * alfa)
                if alfa < -1 * next_eval < beta:
                    next_eval, next_column = self.negamax(state, depth - 1, not maximizing_player, current_depth + 1,
                                                          -1 * beta, -1 * alfa)

            next_eval *= -1
            if next_eval > max_eval:
                max_eval = next_eval
                max_column = column
            # print("Max with value: ", max_eval, " at depth ", current_depth, "\n")
            alfa = max(alfa, max_eval)
            if beta <= alfa:
                break
        return max_eval, max_column


class CompetativeAgent(Agent):
    def get_chosen_column(self, state, max_depth):
        # print(max_depth)
        if self.id == 0:
            player = True
        else:
            player = False
        _, column = self.minimax(state, max_depth, player, 0, float('-inf'), float('inf'))
        return column

    def minimax(self, state, depth, maximizing_player, current_depth, alfa, beta):

        print("evaluation state ", state)
        # print("in minimax" ,depth)
        if depth == 0 or state.get_state_status() is not None:
            return obliteration_evaluation(state, maximizing_player), None

        if maximizing_player:
            nodes = []
            possible_columns = state.get_possible_columns()
            for column in possible_columns:
                weight = -1 * get_weight(column)
                new_state = state.generate_successor_state(column)
                node = (
                    obliteration_evaluation(new_state, maximizing_player), weight,
                    new_state,
                    column)
                nodes.append(node)

            max_eval = float('-inf')
            max_column = None

            nodes = sorted(nodes, key=lambda x: (x[0], x[1]))
            print("Player ", maximizing_player, nodes)

            while nodes:
                current_node = nodes.pop()
                _, _, state, column = current_node
                print(current_node)
                next_eval, next_column = self.minimax(state, depth - 1, not maximizing_player, current_depth + 1, alfa,
                                                      beta)
                if next_eval > max_eval:
                    max_eval = next_eval
                    max_column = column
                # print("Max with value: ", max_eval, " at depth ", current_depth, "\n")
                alfa = max(alfa, max_eval)
                if beta <= alfa:
                    break
            return max_eval, max_column

        else:
            nodes = []
            possible_columns = state.get_possible_columns()
            for column in possible_columns:
                weight = get_weight(column)
                new_state = state.generate_successor_state(column)
                node = (
                    obliteration_evaluation(new_state, maximizing_player), weight,
                    new_state,
                    column)
                nodes.append(node)

            min_eval = float('inf')
            min_column = None
            nodes = sorted(nodes, key=lambda x: (x[0], x[1]), reverse=True)
            print("Player ", maximizing_player, nodes)

            while nodes:
                current_node = nodes.pop()
                _, _, state, column = current_node
                print(current_node)
                next_eval, next_column = self.minimax(state, depth - 1, not maximizing_player, current_depth + 1, alfa,
                                                      beta)
                if next_eval < min_eval:
                    min_eval = next_eval
                    min_column = column
                # print("Min with value: ", min_eval, " at depth ", current_depth, "\n")
                beta = min(beta, min_eval)
                if beta <= alfa:
                    break
            return min_eval, min_column
