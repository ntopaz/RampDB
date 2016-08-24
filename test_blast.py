from core.views_blastall import blast_all
from core.views_hmm import hmm_query
import sys

input_file = sys.argv[1]
#hmm_query(input_file)
blast_all(input_file)
