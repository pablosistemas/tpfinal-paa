import numpy as np
import random

import structures.matrix.main as matrix
import settings.main as global_var
import utils.main as utils


def greedy_set_cover(coverage_matrix, probabilistic=False, n_first=1):
    covering_set = []
    
    utils.verify_array_type(coverage_matrix)   
    sorted_cov_mat_idx = utils.get_sorted_matrix_increasing_weight_order(coverage_matrix)

    num_covered_edges = 0
    num_edges = coverage_matrix.shape[1]

    while num_covered_edges < num_edges:
        if not probabilistic:
            chosen_idx = 1
        else:
            chosen_idx = random.randint(1, n_first)
        # update the covering set and the number of covered vertices
        covering_set.append(matrix.get_asn_from_coverage_line(global_var.coverage_matrix[sorted_cov_mat_idx[chosen_idx - 1], ]))
        num_covered_edges = num_covered_edges + sum(coverage_matrix[sorted_cov_mat_idx[chosen_idx - 1], ])
        # must be send a copy for not update the reference
        utils.update_lines_with_covered_asn(coverage_matrix, coverage_matrix[sorted_cov_mat_idx[chosen_idx - 1], ].copy())
        sorted_cov_mat_idx = utils.get_sorted_matrix_increasing_weight_order(coverage_matrix)

    return covering_set

