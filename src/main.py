from algorithms.probabilistic.main import *
from algorithms.local_search.main import *
from algorithms.greedy.main import *
from structures.matrix.main import *
from algorithms.ga.main import *
from iomanip.io.main import *

import networkx as nx
import numpy as np
import time
import sys
import re
import os


def print_report(description, set_cover, evaluation_time):
    if (utils.verify_set_cover(set_cover)):
        print('%s. Number of sets: %d, time in seconds: %f\n'%(description, len(set_cover), evaluation_time))
    else:
        print('Error')
    return


def main():
    if len(sys.argv) < 2:
        raise "No BGP file as argument"

    input_file = sys.argv[1]
    g = nx.Graph()

    read_bgp_file(g, input_file)
    create_matrix_from_graph(g)

    #ga()

    start = time.time()
    idx_set_covering_group = greedy_set_cover(global_var.coverage_matrix.copy())
    end = time.time()
    print_report("GREEDY SEARCH", utils.get_sets_from_idx_set(idx_set_covering_group), end - start)


    '''
    for n in range(2, global_var.N):
        start = time.time()
        set_covering_group = probabilistic_greedy_set_cover(global_var.coverage_matrix.copy(), n)
        end = time.time()
        print('PROBABILISTIC GREEDY SET COVER %d. Number of sets: %d, time in seconds: %f\n'%(n, len(set_covering_group), end - start))
    '''

    start = time.time()
    idx_set_covering_group_local_search = local_search(idx_set_covering_group)
    end = time.time()
    print_report("LOCAL SEARCH SEARCH", utils.get_sets_from_idx_set(idx_set_covering_group_local_search), end - start)

    return


if __name__ == "__main__":
    main()
