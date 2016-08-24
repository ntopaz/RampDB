from setup_interactions import load_int
from setup_ligands import load_lig
from setup_references import load_reference
from setup_proteins import load_proteins
import sys
input = sys.argv[1]


load_proteins(input)
load_lig()
load_reference()
load_int()
