from algorithms.greedy.main import *
import settings.main as global_var


def probabilistic_greedy_set_cover(coverage_matrix, N=global_var.N):
    return greedy_set_cover(coverage_matrix, True, N)