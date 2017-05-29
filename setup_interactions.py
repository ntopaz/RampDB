import os, sys, json
import pprint as pp
from core.views_load_interactions import load_interactions

def load_int():
	interaction = {}
	list = []
	interaction['Amylin receptor 1'] = {'name':'Amylin receptor 1','name_short': 'AMY1', 'rampfamily':'receptor activity modifying protein 1','gpcrfamily':'calcitonin receptor','ligand':'amylin', 'function':'High affinity for amylin and CGRP'}
	interaction['Amylin receptor 2'] = {'name':'Amylin receptor 2','name_short': 'AMY2','rampfamily':'receptor activity modifying protein 2','gpcrfamily':'calcitonin receptor','ligand':'amylin','function':'High affinity for amylin'}
	interaction['Amylin receptor 3'] = {'name':'Amylin receptor 3','name_short': 'AMY3','rampfamily':'receptor activity modifying protein 3','gpcrfamily':'calcitonin receptor','ligand':'amylin','function':'High affinity for amylin and low affinity for CGRP'}
	interaction['Calcitonin gene-related peptide receptor'] = {'name':'Calcitonin gene-related peptide receptor','name_short': 'CGRP','rampfamily':'receptor activity modifying protein 1','gpcrfamily':'calcitonin receptor-like receptor','ligand':'calcitonin gene-related peptide alpha','function':'High affinity for CGRP'}
	interaction['Adrenomedullin receptor'] = {'name':'Adrenomedullin receptor','name_short': 'AM1','rampfamily':'receptor activity modifying protein 2','gpcrfamily':'calcitonin receptor-like receptor','ligand':'adrenomedullin','function':'100-fold selectivity for Adrenomedullin over CGRP'}
	interaction['Intermedin receptor'] = {'name':'Intermedin receptor','name_short': 'AM2','rampfamily':'receptor activity modifying protein 3','gpcrfamily':'calcitonin receptor-like receptor','ligand':'adrenomedullin 2','function':'Affinity for intermedin and adrenomedullin'} 
	interaction['Vasoactive Intestinal Polypeptide Receptor 1_1'] = {'name':'Vasoactive Intestinal Polypeptide Receptor','name_short': 'VIP1_1','rampfamily':'receptor activity modifying protein 1','gpcrfamily':'vasoactive intestinal polypeptide receptor 1','ligand':'vasoactive intestinal polypeptide','function':'Translocation to the cell surface'}
	interaction['Vasoactive Intestinal Polypeptide Receptor 1_2'] = {'name':'Vasoactive Intestinal Polypeptide Receptor','name_short': 'VIP1_2','rampfamily':'receptor activity modifying protein 2','gpcrfamily':'vasoactive intestinal polypeptide receptor 1','ligand':'vasoactive intestinal polypeptide','function':'Increased affinity for VIP1 agonists'}
	interaction['Vasoactive Intestinal Polypeptide Receptor 1_3'] = {'name':'Vasoactive Intestinal Polypeptide Receptor','name_short': 'VIP1_3','rampfamily':'receptor activity modifying protein 3','gpcrfamily':'vasoactive intestinal polypeptide receptor 1','ligand':'vasoactive intestinal polypeptide','function':'Not enough data to determine function'}
	interaction['Parathyroid Hormone Receptor 1_2'] = {'name':'Parathyroid Hormone Receptor 1','name_short': 'PTHR1','rampfamily':'receptor activity modifying protein 2','gpcrfamily':'parathyroid hormone receptor 1','ligand':'parathyroid hormone','function':'Not enough data to determine function'}
	interaction['Parathyroid Hormone Receptor 2_3'] = {'name':'Parathyroid Hormone Receptor 2','name_short': 'PTHR2','rampfamily':'receptor activity modifying protein 3','gpcrfamily':'parathyroid hormone receptor 2','ligand':'parathyroid hormone','function':'Not enough data to determine function'}
	interaction['Glucagon Receptor 1_2'] = {'name':'Glucagon Receptor','name_short': 'Glucagon','rampfamily':'receptor activity modifying protein 2','gpcrfamily':'glucagon receptor','ligand':'glucagon','function':'Increases glucagon ligand potency and efficacy'}

	load_interactions(json.dumps(interaction))

def main():
	load_int()

if __name__=="__main__":
	main()
