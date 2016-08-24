import os, sys, json
import pprint as pp
from core.views_load_interactions import load_interactions

def load_int():
	interaction = {}
	list = []
	attributes = {'rampfamily':'receptor activity modifying protein 1','gpcrfamily':'calcitonin receptor','ligand':'amylin'}
	interaction['AMY1'] = attributes
	attributes = {'rampfamily':'receptor activity modifying protein 2','gpcrfamily':'calcitonin receptor','ligand':'amylin'}
	interaction['AMY2'] = attributes
	attributes = {'rampfamily':'receptor activity modifying protein 3','gpcrfamily':'calcitonin receptor','ligand':'amylin'}
	interaction['AMY3'] = attributes
	attributes = {'rampfamily':'receptor activity modifying protein 1','gpcrfamily':'calcitonin receptor-like receptor','ligand':'calcitonin gene-related peptide'}
	interaction['CGRP'] = attributes
	attributes = {'rampfamily':'receptor activity modifying protein 2','gpcrfamily':'calcitonin receptor-like receptor','ligand':'adrenomedullin'}
	interaction['AM1'] = attributes
	attributes = {'rampfamily':'receptor activity modifying protein 3','gpcrfamily':'calcitonin receptor-like receptor','ligand':'intermedin'}
	interaction['AM2'] = attributes
	load_interactions(json.dumps(interaction))

def main():
	load_int()

if __name__=="__main__":
	main()
