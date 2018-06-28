from algorithms.probabilistic.main import *
from algorithms.local_search.main import *
from algorithms.greedy.main import *
from structures.matrix.main import *
from algorithms.ga.main import *
from iomanip.io.main import *

from memory_profiler import memory_usage, LogFile
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

    print('Number of ASN in network: %d'%(global_var.asn_unordered_set.__len__()))
    print('Number of probes: %d'%(global_var.sets.__len__()))

    start = time.time()
    idx_set_covering_group = greedy_set_cover(global_var.coverage_matrix.copy())
    end = time.time()
    print_report("GREEDY SEARCH", utils.get_sets_from_idx_set(idx_set_covering_group), end - start)

    # utils.set_max_number_N_probabilistic_search()

    Ns = [3,5,7,9,10]
    best_n = Ns[0]
    best_coverage = None
    for idx, n in enumerate(Ns):
        start = time.time()
        idx_set_covering_group_prob = probabilistic_greedy_set_cover(global_var.coverage_matrix.copy(), n)
        end = time.time()
        if best_coverage is None:
            best_coverage = idx_set_covering_group_prob
        elif idx > 0:
            if idx_set_covering_group_prob.__len__() < best_coverage.__len__():
                best_coverage = idx_set_covering_group_prob
                best_n = n
        
        print_report("PROBABILISTIC GREEDY SET COVER %d"%(n), utils.get_sets_from_idx_set(idx_set_covering_group_prob), end - start)

    for percentual_of_removal in global_var.PERCENT_OF_REMOVAL:
        start = time.time()
        idx_set_covering_group_local_search = local_search(idx_set_covering_group, percentual_of_removal)
        end = time.time()
        print_report("LOCAL SEARCH + GREEDY: %f"%(percentual_of_removal), utils.get_sets_from_idx_set(idx_set_covering_group_local_search), end - start)

    for percentual_of_removal in global_var.PERCENT_OF_REMOVAL:
        start = time.time()
        idx_set_covering_group_local_search = local_search(idx_set_covering_group, percentual_of_removal, True, best_n)
        end = time.time()
        print_report("LOCAL SEARCH + PROBABILISTIC %d: %f"%(best_n, percentual_of_removal), utils.get_sets_from_idx_set(idx_set_covering_group_local_search), end - start)

    return


def profiling():
    print(max(memory_usage((main))))


if __name__ == "__main__":
    profiling()
