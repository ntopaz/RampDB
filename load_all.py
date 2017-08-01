import json
from setup_interactions import load_int
#from setup_ligands import load_lig_api
from setup_references import load_reference
from setup_proteins import load_proteins
from setup_families import load_families
from core.views_load_int_ref import load_db
from core.views_load_ligands import load_ligands
import sys

input = sys.argv[1]
ref_json = sys.argv[2]
ligands = sys.argv[3]

with open(ref_json) as f:
	my_data = json.load(f)
family_data = load_families()	
load_proteins(input,family_data)
print("loaded proteins")
#load_lig()
#ligand_dict = load_lig_api()
with open(ligands) as f:
	ligand_dict = json.load(f)
load_ligands(ligand_dict)
print("loaded ligands")
load_reference()
print("loaded references")
load_int(ligand_dict)
print("loaded interactions")
load_db(my_data)
print("done")

