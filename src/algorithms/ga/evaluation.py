import settings.main as global_var
from utils.main import *

import sys

INFACTIVEL = sys.maxsize

def eval_set_covering(individual):
    set_cover = list()
    for idx, _set in enumerate(individual):
        if _set is 1:
            set_cover.append(global_var.sets[idx])
    
    if verify_set_cover(set_cover):
        return len(set_cover)
    return (INFACTIVEL,)
