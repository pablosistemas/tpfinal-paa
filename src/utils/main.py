import numpy as np
import itertools
import settings.main as global_var


def binary_permutations(n):
    return list(itertools.product([0,1], repeat=n))


def verify_array_type(array):
    if type(array) is not np.ndarray:
        raise 'Invalid format'
    return


def get_sorted_matrix_increasing_weight_order(R_D_max):
    if type(R_D_max) is not np.ndarray:
        raise "Invalid format"
    # sum_of_columns_by_line = [sum(R_D_max[i]) for i in range(R_D_max.shape[0])]
    sum_of_columns_by_line = np.sum(R_D_max, 1)
    sorted_lines_indexes = np.argsort(sum_of_columns_by_line)
    return sorted_lines_indexes[::-1]


def update_lines_with_covered_asn(D, r_i):
    for i in range(D.shape[0]):
        for j in range(D.shape[1]):
            if r_i[j] == 1 and D[i,j] == 1:
                D[i,j] = 0
    return


def verify_set_cover(set_cover):
    covering = dict()
    for group in set_cover:
        for tes in group:
            if tes in covering:
                covering[tes] = covering[tes] + 1
            else:
                covering[tes] = 1
    return covering.__len__() == global_var.asn_ordered_list.__len__()

