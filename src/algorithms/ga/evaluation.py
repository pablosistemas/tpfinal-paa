import settings.main as global_var
import utils.main as utils

import sys


def eval_set_covering(individual):
    set_cover = list()
    idx_set_cover = np.where(np.array(individual) == 1)
    if (utils.verify_set_cover(utils.get_sets_from_idx_set(idx_set_cover))):
        return global_var.coverage_matrix.shape[1]
    
    total_cost = 0


    while True:
        total_cost = utils.verify_set_cover()
    for idx, _set in enumerate(individual):
        if _set is 1:
            set_cover.append()
    
    if verify_set_cover(set_cover):
        return len(set_cover)
    return (INFACTIVEL,)
