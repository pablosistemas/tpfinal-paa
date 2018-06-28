# GLOBAL VARIABLES

# autonomous systems numbers (column labels)
asn_unordered_set = set()
asn_ordered_list = None

# inverted index
asn_index = dict()
asn_inverted_index = dict()

# list of sets candidates to cover the asn
sets = []

# matrix
coverage_matrix = None

# probabilisic algorithm parametrization
N = 10 # default
PERCENT_OF_PROBABILISTIC_CHOICES = 0.05

# local search
PERCENT_OF_REMOVAL = [0.25, 0.3, 0.4, 0.5]
