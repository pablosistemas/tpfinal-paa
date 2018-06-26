import settings.main as global_var
from algorithms.greedy.main import *


max_num_iterations_without_change = 10
upper_bound_solution = 0

PERCENT_OF_REMOVAL = 0.3

FACTOR = 0.25
TABU_LIST_SIZE = int(FACTOR * len(global_var.sets))

tabu_list = [-1 for i in range(TABU_LIST_SIZE)]
last_index_tabu_list = 0


def insert_into_tabu_list(value):
    global tabu_list, last_index_tabu_list
    tabu_list[last_index_tabu_list] = value
    last_index_tabu_list = last_index_tabu_list % TABU_LIST_SIZE
    return


# solution_greedy MUST BE indexes of chosen sets
def local_search(solution_greedy):
    global upper_bound_solution, tabu_list
    upper_bound_solution = len(solution_greedy)

    solution = solution_greedy[:]

    num_of_removal = int(len(solution) * PERCENT_OF_REMOVAL)

    remove_idx = random.sample(solution, num_of_removal)

    # infeasible solution
    solution = [sol for sol in solution if sol not in remove_idx]

    coverage_matrix = utils.from_candidate_solution_create_coverage_matrix(solution)
    updated_num_covered = utils.from_coverage_matrix_calculate_num_of_covered_asn(coverage_matrix)
    idx_covering_set = from_partial_solution_greedy_cover(coverage_matrix, solution)
    return idx_covering_set


def fitness():
    global upper_bound_solution
    neo_covering = num_of_uncovered_variables() + len(coverage_matrix)
    if neo_covering < upper_bound_solution:
        upper_bound_solution = neo_covering
    return neo_covering