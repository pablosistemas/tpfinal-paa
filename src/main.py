from algorithms.probabilistic.main import *
from algorithms.greedy.main import *
from structures.matrix.main import *
from iomanip.io.main import *

import networkx as nx
import numpy as np
import time
import sys
import re
import os


class GraphHelper():
    def __init__(self):
        pass

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
    def PS_algorithm(R_D_max):
        GraphHelper.verify_array_type(R_D_max)

        sorted_R_D_max_indexes = GraphHelper.get_sorted_matrix_increased_weight_order(R_D_max)
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


def main():
    if len(sys.argv) < 2:
        raise "No BGP file as argument"

    input_file = sys.argv[1]
    g = nx.Graph()

    read_bgp_file(g, input_file)
    create_matrix_from_graph(g)

    start = time.time()
    set_covering_group = greedy_set_cover(global_var.coverage_matrix.copy())
    end = time.time()
    if (utils.verify_set_cover(set_covering_group)):
        print('GREEDY SET COVER. Number of sets: %d, time in seconds: %f\n'%(len(set_covering_group), end - start))
    else:
        print('Error')

    for n in range(2, global_var.N):
        start = time.time()
        set_covering_group = probabilistic_greedy_set_cover(global_var.coverage_matrix.copy(), n)
        end = time.time()
        print('PROBABILISTIC GREEDY SET COVER %d. Number of sets: %d, time in seconds: %f\n'%(n, len(set_covering_group), end - start))
    
    return


if __name__ == "__main__":
    main()