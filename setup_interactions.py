import os, sys, json
import pprint as pp
from core.views_load_interactions import load_interactions
ligand_dict = sys.argv[1]
def load_int(ligand_dict):
		
	interaction = {}
	list = []
	interaction['Amylin receptor 1'] = {'name':'Amylin receptor 1','name_short': 'AMY1', 'rampfamily':'receptor activity modifying protein 1','gpcrfamily':'calcitonin receptor'}
	interaction['Amylin receptor 2'] = {'name':'Amylin receptor 2','name_short': 'AMY2','rampfamily':'receptor activity modifying protein 2','gpcrfamily':'calcitonin receptor'}
	interaction['Amylin receptor 3'] = {'name':'Amylin receptor 3','name_short': 'AMY3','rampfamily':'receptor activity modifying protein 3','gpcrfamily':'calcitonin receptor'}
	interaction['Calcitonin gene-related peptide receptor'] = {'name':'Calcitonin gene-related peptide receptor','name_short': 'CGRP','rampfamily':'receptor activity modifying protein 1','gpcrfamily':'calcitonin receptor-like receptor'}
	interaction['Adrenomedullin receptor'] = {'name':'Adrenomedullin receptor','name_short': 'AM1','rampfamily':'receptor activity modifying protein 2','gpcrfamily':'calcitonin receptor-like receptor'}
	interaction['Intermedin receptor'] = {'name':'Intermedin receptor','name_short': 'AM2','rampfamily':'receptor activity modifying protein 3','gpcrfamily':'calcitonin receptor-like receptor'}
	interaction['Vasoactive Intestinal Polypeptide Receptor 1_1'] = {'name':'Vasoactive Intestinal Polypeptide Receptor','name_short': 'VPAC1','rampfamily':'receptor activity modifying protein 1','gpcrfamily':'vasoactive intestinal polypeptide receptor 1'}
	interaction['Vasoactive Intestinal Polypeptide Receptor 1_2'] = {'name':'Vasoactive Intestinal Polypeptide Receptor','name_short': 'VPAC1','rampfamily':'receptor activity modifying protein 2','gpcrfamily':'vasoactive intestinal polypeptide receptor 1'}
	interaction['Vasoactive Intestinal Polypeptide Receptor 1_3'] = {'name':'Vasoactive Intestinal Polypeptide Receptor','name_short': 'VPAC1','rampfamily':'receptor activity modifying protein 3','gpcrfamily':'vasoactive intestinal polypeptide receptor 1'}
	interaction['Parathyroid Hormone Receptor 1_2'] = {'name':'Parathyroid Hormone Receptor 1','name_short': 'PTH1','rampfamily':'receptor activity modifying protein 2','gpcrfamily':'parathyroid hormone receptor 1'}
	interaction['Parathyroid Hormone Receptor 2_3'] = {'name':'Parathyroid Hormone Receptor 2','name_short': 'PTH2','rampfamily':'receptor activity modifying protein 3','gpcrfamily':'parathyroid hormone receptor 2'}
	interaction['Glucagon Receptor 1_2'] = {'name':'Glucagon Receptor','name_short': 'Glucagon','rampfamily':'receptor activity modifying protein 2','gpcrfamily':'glucagon receptor'}
	for receptor in interaction:
		name_short = interaction[receptor]["name_short"]
		ligand_set = ligand_dict[name_short]
		interaction[receptor]["ligands"] = ligand_set
	#pp.pprint(interaction)
	
	load_interactions(json.dumps(interaction))

def main(ligand_dict):
	with open(ligand_dict) as f:
		my_data = json.load(f)
	load_int(my_data)

if __name__=="__main__":
	main(ligand_dict)
