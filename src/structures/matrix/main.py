import settings.main as global_var

import numpy as np


def create_ordered_list_from_set(p_set):
    return sorted(p_set)


def create_inverted_index():
    global_var.asn_index = dict()
    for idx, asn in enumerate(global_var.asn_ordered_list):
        global_var.asn_index[asn] = idx
        global_var.asn_inverted_index[idx] = asn
    return


# graph MUST BE a networkX object
def create_matrix_from_graph(graph):
    global_var.asn_ordered_list = create_ordered_list_from_set(global_var.asn_unordered_set)
    global_var.coverage_matrix = np.zeros((global_var.sets.__len__(), global_var.asn_ordered_list.__len__()))
    create_inverted_index()
    for set_idx, p_set in enumerate(global_var.sets):
        for asn in p_set:
            global_var.coverage_matrix[set_idx, global_var.asn_index[asn]] = 1
    return


def get_asn_from_coverage_line(coverage_line):
    indexes = np.where(coverage_line == 1)[0]
    list_of_asn_covered = []
    for idx in indexes:
        list_of_asn_covered.append(global_var.asn_inverted_index[idx])
    return list_of_asn_covered
