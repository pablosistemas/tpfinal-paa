import networkx as nx
import numpy as np
import itertools
import sys
import re
import os

class Node:
    __time = None
    __type = None
    __from = None
    __to = None
    __asn_src = None
    __asn_dst = None
    __origin = None
    __as_path = None
    __mp_reach_nlri = None
    __next_hop = None
    __announce = None

    def __init__(self):
        pass
    

class GraphHelper():
    def __init__(self):
        pass

    @staticmethod
    def __parse__(line): 
        match = re.search('\s*\w+:\s(.+)\n', line)
        if match != None:
            return match.group(1)
        else:
            print(line)
            return None
    
    @staticmethod
    def __get_asn_number__(line):
        match = re.search('.+\s[AS]*(\w+)', line)
        if match != None:
            return match.group(1)
        else:
            return None

    @staticmethod
    def __reader__(self, input_file):
        file = open(input_file, 'r')
        line_n = 0
        line = file.readline()
        line_n = line_n + 1
        while line != '':
            _node = Node()
            status = True

            if not re.match('TIME', line):
                print(line)
                raise 'No TIME'

            _node.__time = GraphHelper.__parse__(line)
            line = file.readline()
            line_n = line_n + 1
            _node.__type = GraphHelper.__parse__(line)
            line = file.readline()
            line_n = line_n + 1
            _node.__from = GraphHelper.__parse__(line)
            line = file.readline()
            line_n = line_n + 1
            _node.__to = GraphHelper.__parse__(line)

            _node.__asn_src = GraphHelper.__get_asn_number__(_node.__from)
            _node.__asn_dst = GraphHelper.__get_asn_number__(_node.__to)

            status = _node.__asn_src != None and _node.__asn_dst != None

            while line != '\n':
                line = file.readline()
                line_n = line_n + 1

            if status:
                self.add_node(_node.__asn_src)
                self.add_node(_node.__asn_dst)
                self.add_edge(_node.__asn_src, _node.__asn_dst)

            line = file.readline()
            line_n = line_n + 1

        file.close()

    @staticmethod
    def binary_permutations(n):
        return list(itertools.product([0,1], repeat=n))

    @staticmethod
    def calculate_span_vectors_from_R_D_star(R_D_star, r_i):
        if type(R_D_star) is not np.ndarray:
            raise "Invalid format"

        perms = GraphHelper.binary_permutations()

        for perm in perms:
            num_lines = R_D_star.shape[0]
            span = R_D_star[0]
            for index in range(1, num_lines):
                span = np.logical_or(span, perm[index] * R_D_star[index])
            # False whether r_i is a linear combination of < R(D*) >
            if sum(np.logical_and(span, r_i) == len(r_i)):
                return False
        return True

    @staticmethod
    def verify_array_type(array):
        if type(array) is not np.ndarray:
            raise 'Invalid format'

    @staticmethod
    def PS_algorithm(R_D_max):
        GraphHelper.verify_array_type(R_D_max)

        sorted_R_D_max_indexes = GraphHelper.get_sorted_matrix_increased_weigth_order(R_D_max)
        sorted_R_D_max = R_D_max[sorted_R_D_max_indexes,]

        GraphHelper.verify_array_type(sorted_R_D_max)

        R_D_star = []
        R_D_star.append(sorted_R_D_max[0, ])
        mask = np.ones(R_D_max.shape[0], dtype=bool)
        mask[[0]] = False
        indexes_of_r_i_sampled_from_sorted_R_D = [0]
        i = 1

        while sum(mask) > 0:
            r_i = sorted_R_D_max[i, ]
            r_i_not_in_R_D_star = GraphHelper.calculate_span_vectors_from_R_D_star(R_D_star, r_i) 

            if r_i_not_in_R_D_star:
                R_D_star.append(r_i)
                indexes_of_r_i_sampled_from_sorted_R_D.append(i)
            i = i + 1             

        return (sorted_R_D_max_indexes, indexes_of_r_i_sampled_from_sorted_R_D, np.matrix(R_D_star))

    @staticmethod
    def get_sorted_matrix_increased_weigth_order(R_D_max):
        if type(R_D_max) is not np.ndarray:
            raise "Invalid format"
        # sum_of_columns_by_line = [sum(R_D_max[i]) for i in range(R_D_max.shape[0])]
        sum_of_columns_by_line = np.sum(R_D_max, 1)
        sorted_lines_indexes = np.argsort(sum_of_columns_by_line)
        return sorted_lines_indexes
    
    @staticmethod
    def greedy_set_cover_uncovered_elements():
        pass

    @staticmethod
    def update_D(D, r_i):
        for i in D.shape[0]:
            for j in D.shape[1]:
                if D[i,j] == 1 and r_i[j] == 1:
                    D[i,j] = 0

    @staticmethod
    def greedy_set_cover(D_max):
        GraphHelper.verify_array_type(D_max)   
        D_max_t = np.transpose(D_max)

        sorted_D_max_t_indexes = GraphHelper.get_sorted_matrix_increased_weigth_order(D_max_t)
        sorted_D_max_t = D_max[sorted_D_max_t_indexes,]

        GraphHelper.verify_array_type(sorted_D_max_t)

        D_star = []

        mask = np.ones(D_max_t.shape[0], dtype=bool)
        mask[[0]] = False

        D_star.append(sorted_D_max_t[0, ])
        indexes_of_r_i_sampled_from_sorted_D = [0]

        iterator_mask = 0
        num_covered_edges = 0
        num_edges = D_max_t.shape[1]

        while num_covered_edges < num_edges:
            r_i = sorted_D_max_t[iterator_mask, ]
            iterator_mask = iterator_mask + 1
            GraphHelper.update_D(sorted_D_max_t, r_i)

            sorted_D_max_t_indexes = GraphHelper.get_sorted_matrix_increased_weigth_order(sorted_D_max_t[mask,])
            sorted_D_max_t = D_max[sorted_D_max_t_indexes,]

            if r_i_not_in_R_D_star:
                R_D_star.append(r_i)
                indexes_of_r_i_sampled_from_sorted_R_D.append(i)
            i = i + 1             

        return (sorted_R_D_max_indexes, indexes_of_r_i_sampled_from_sorted_R_D, np.matrix(R_D_star))


    @staticmethod
    def brute_force():
        # for k = 1 to n
        # generate all permutations from i = 1 to k
        # test if this permutation covers the graph
        # return first


def main():
    input_file = 'data/input_bgp'
    g = nx.Graph()

    GraphHelper.__reader__(g, input_file)
    print(g)

if __name__ == "__main__":
    main()