import os, sys, json
import pprint as pp
import urllib3
import json
import ast
from core.views_load_ligands import load_ligands

def load_lig_api():
	http = urllib3.PoolManager()
	interacting_ligands = {}
	all_synonyms = {}
	skip = [696, 4449, 1787, 1788,1790,1814,700,701,682]
	targets = {"AMY1":44,"CGRP":48,"AMY2":45,"AM1":49,"AMY3":46,"AM2":50,"VPAC1":371,"PTH1":331,"PTH2":332,"Glucagon":251,"VPAC2":372,"CRF":212,"GPER/GPR30":221}
	for complex in targets:
		if complex not in interacting_ligands:
			interacting_ligands[complex] = {}
		target_id = targets[complex]
		url = "http://www.guidetopharmacology.org/services/targets/{}/interactions".format(target_id)
		request = http.request('GET',url)
		request_data = json.loads(request.data)
		for result in request_data:
			ligand_int = result["ligandId"]
			if ligand_int in skip:
				continue
			url="http://www.guidetopharmacology.org/services/ligands/{}".format(ligand_int)
			lig_request = http.request("GET",url)
			lig_request_data = json.loads(lig_request.data)
			url="http://www.guidetopharmacology.org/services/ligands/{}/synonyms".format(ligand_int)
			synonym_request = http.request("GET",url)
			if synonym_request.data:
				synonym_request_data = json.loads(synonym_request.data)

			url="http://www.guidetopharmacology.org/services/ligands/{}/structure".format(ligand_int)
			struct_request = http.request("GET",url)
			if struct_request.data:
				struct_data = json.loads(struct_request.data)
				inchi_key = struct_data["inchiKey"]
				if "oneLetterSeq" in struct_data:
					sequence = struct_data["oneLetterSeq"]
				else:
					sequence = "Not a peptide"
			else:
				inchi_key = "Not available"
				sequence = "Not available"
			url="http://www.guidetopharmacology.org/services/ligands/{}/databaseLinks".format(ligand_int)
			db_request = http.request("GET",url)
			chem_id = 0
			if db_request.data:
				db_data = json.loads(db_request.data)
				for db_res in db_data:
					if db_res["database"] == "PubChem CID":
						chem_id = db_res["accession"]

			ligand_name = lig_request_data["name"].replace("<sup>"," ").replace("</sup>"," ").replace("<sub>"," ")
			ligand_name = ligand_name.replace("&","").replace(";","")
			if "[" in ligand_name:
				continue
			ligand_type = lig_request_data["type"]

			if ligand_name not in interacting_ligands:
				interacting_ligands[complex][ligand_name] = {}
			else:
				continue
			if result["affinity"].strip() == "":
				result["affinity"] = "N/A"
			interacting_ligands[complex][ligand_name]["affinity"] = result["affinity"]
			interacting_ligands[complex][ligand_name]["binding_type"] = result["type"]
			interacting_ligands[complex][ligand_name]["ligand_type"] = ligand_type
			if inchi_key.strip() == "":
				inchi_key = "N/A"
			interacting_ligands[complex][ligand_name]["inchi_key"] = inchi_key
			interacting_ligands[complex][ligand_name]["sequence"] = sequence
			interacting_ligands[complex][ligand_name]["chem_id"] = chem_id
			interacting_ligands[complex][ligand_name]["gtp_id"] = ligand_int
			references = []
			for reference in result["refs"]:
				references.append(reference["pmid"])
			interacting_ligands[complex][ligand_name]["pmid"] = references
			synonyms = []
			if ligand_name not in all_synonyms:
				all_synonyms[ligand_name] = []
			for res in synonym_request_data:
				res_name = res["name"].replace("<sup>"," ").replace("</sup>"," ").replace("<sub>"," ")
				res_name = res_name.replace("u'","").replace("'","")
				all_synonyms[ligand_name].append(res_name)
			#interacting_ligands[complex][ligand_name]["synonyms"] = synonyms
	for complex in interacting_ligands:
		for ligand_name in interacting_ligands[complex]:
			interacting_ligands[complex][ligand_name]["synonyms"] = all_synonyms[ligand_name]
	#interacting_ligands = ast.literal_eval(json.dumps(interacting_ligands))
	custom_ligand = {}
	custom_ligand["amylin"] = {"inchi_key":"PLOPBXQQPZYQFA-AXPWDRQUSA-N","chem_id":16132430}
	custom_ligand["adrenomedullin"] = {"inchi_key":"ULCUCJFASIJEOE-NPECTJMMSA-N","chem_id":56841671}
	custom_ligand["alpha-CGRP"] = {"inchi_key":"PBGNJGVTFINXOG-XJVRLEFXSA-N","chem_id":56841902}
	custom_ligand["PTHrP-(1-34) (human)"] = {"inchi_key":"ZOWOHMFPXMYFKJ-WBTWNKCNSA-N","chem_id":16144017}
	for complex in interacting_ligands:
		for ligand in custom_ligand:
			if ligand in interacting_ligands[complex]:
				interacting_ligands[complex][ligand]["inchi_key"] = custom_ligand[ligand]["inchi_key"]
				interacting_ligands[complex][ligand]["chem_id"] = custom_ligand[ligand]["chem_id"]
	out_json = json.dumps(interacting_ligands)
	with open("interacting_ligands.json","w") as f:
		json.dump(interacting_ligands,f)
	pp.pprint(interacting_ligands)
	#load_ligands(out_json)
	return interacting_ligands

def main():
	ligand_dict = load_lig_api()
	return ligand_dict
if __name__=="__main__":
	main()
