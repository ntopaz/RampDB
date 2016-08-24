import os, sys, json
import pprint as pp
from core.views_load_ligands import load_ligands

def load_lig():
	ligand = {}

	list = ['amylin','adrenomedullin','intermedin','calcitonin gene-related peptide','vasoactive intestinal polypeptide','parathyroid hormone','tuberoinfundibular peptide']

	attributes = {'name_short':'AMY','chem_id':'16132430','inchi_key':'PLOPBXQQPZYQFA-AXPWDRQUSA-N'}
	ligand['amylin'] = attributes
	attributes = {'name_short':'AM1','chem_id':'56841671','inchi_key':'ULCUCJFASIJEOE-NPECTJMMSA-N'}
	ligand['adrenomedullin'] = attributes
	attributes = {'name_short':'AM2','chem_id':'16162729','inchi_key':'WHNFPRLDDSXQCL-UHFFFAOYSA-N'}
	ligand['intermedin'] = attributes
	attributes = {'name_short':'CGRP','chem_id':'56841902','inchi_key':'PBGNJGVTFINXOG-XJVRLEFXSA-N'}
	ligand['calcitonin gene-related peptide'] = attributes
	attributes = {'name_short':'VIP','chem_id':'16129679','inchi_key':'VBUWHHLIZKOSMS-UHFFFAOYSA-N'}
	ligand['vasoactive intestinal polypeptide'] = attributes
	attributes = {'name_short':'PTH','chem_id':'16129682','inchi_key':'OGBMKVWORPGQRR-UHFFFAOYSA-N'}
	ligand['parathyroid hormone'] = attributes
	attributes = {'name_short':'TIP39','chem_id':'3023','inchi_key':'IYYZUPMFVPLQIF-UHFFFAOYSA-N'}
	ligand['tuberoinfundibular peptide'] = attributes

	load_ligands(json.dumps(ligand))


def main():
	load_lig()

if __name__=="__main__":
	main()
