import os, sys, json
import pprint as pp
import urllib2
import json
import ast
#from core.views_load_ligands import load_ligands

def load_families():
	family_data = {}
	short_name = {'receptor activity modifying protein 1':'Ramp 1','receptor activity modifying protein 2':'Ramp 2','receptor activity modifying protein 3':'Ramp 3',
					'calcitonin receptor':'CT','calcitonin receptor-like receptor':'CLR',
					'vasoactive intestinal polypeptide receptor 1':'VPAC1','vasoactive intestinal polypeptide receptor 2':'VPAC2','parathyroid hormone receptor 1':'PTH1',
		'parathyroid hormone receptor 2':'PTH2','glucagon receptor':'Glucagon',"corticotropin-releasing factor receptor":"CRF","G protein-coupled estrogen receptor":"GPER"}
	targets = {"Ramp 1":51, "Ramp 2": 52,"Ramp 3": 53,"CT":43,"CLR":47,"AMY1":44,"CGRP":48,"AMY2":45,"AM1":49,"AMY3":46,"AM2":50,"VPAC1":371,"PTH1":331,"PTH2":332,"Glucagon":251,"VPAC2":372,"CRF":212,"GPER":221}
	for name in short_name:
		matching_name = short_name[name]
		target_id = targets[matching_name]
		if matching_name not in family_data:
			family_data[matching_name] = {}
		url = "http://www.guidetopharmacology.org/services/targets/{}/pdbStructure".format(target_id)
		pc_results = urllib2.urlopen(url)
		try:
			pc_results = json.load(pc_results)
		except:
			pc_results = {"no_pdb":"no_pdb"}
		if "no_pdb" not in pc_results:
			pdb_id = pc_results[0]["pdbCode"]
		else:
			pdb_id = "None"
		family_data[matching_name]["pdb_id"] = pdb_id
		family_data[matching_name]["name"] = name
		family_data[matching_name]["gtp_id"] = target_id
		if matching_name == "CLR" or matching_name == "CT":
			status = "Verified Interaction"
		else:
			status = "Unverified: Predicted domain of interaction based on sequence alignment with closely related receptors"
		family_data[matching_name]["status"] = status
	family_data["Ramp 2"]["pdb_id"] = "3AQE"
	family_data["CT"]["pdb_id"] = "5II0"
	family_data["Ramp 1"]["pdb_id"] = "2YX8"
	#pp.pprint(family_data)
	#out_json = json.dumps(interacting_ligands)
	#with open("interacting_ligands.json","w") as f:
	#	json.dump(interacting_ligands,f)
	#load_ligands(out_json)
	return family_data

def main():
	family_dict = load_families()
	return family_dict
if __name__=="__main__":
	main()
