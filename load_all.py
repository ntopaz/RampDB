import json
from setup_interactions import load_int
from setup_ligands import load_lig
from setup_references import load_reference
from setup_proteins import load_proteins
from core.views_load_int_ref import load_db
import sys

input = sys.argv[1]
ref_json = sys.argv[2]

with open(ref_json) as f:
	my_data = json.load(f)
	
load_proteins(input)
load_lig()
load_reference()
load_int()
load_db(my_data)

