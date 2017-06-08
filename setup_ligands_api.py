import os, sys, json
import pprint as pp
import urllib3
import json
import ast
from core.views_load_ligands import load_ligands

def load_lig_api():
	http = urllib3.PoolManager()
	interacting_ligands = {}
	targets = {"AMY1":44,"CGRP":48,"AMY2":45,"AM1":49,"AMY3":46,"AM2":50,"VPAC1":371,"PTH1":331,"PTH2":332,"Glucagon":251}
	for complex in targets:
		if complex not in interacting_ligands:
			interacting_ligands[complex] = {}
		target_id = targets[complex]
		url = "http://www.guidetopharmacology.org/services/targets/{}/interactions".format(target_id)
		request = http.request('GET',url)
		request_data = json.loads(request.data)
		for result in request_data:
			ligand_int = result["ligandId"]
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
			ligand_type = lig_request_data["type"]

			if ligand_name not in interacting_ligands:
				interacting_ligands[complex][ligand_name] = {}
			interacting_ligands[complex][ligand_name]["affinity"] = result["affinity"]
			interacting_ligands[complex][ligand_name]["binding_type"] = result["type"]
			interacting_ligands[complex][ligand_name]["ligand_type"] = ligand_type
			interacting_ligands[complex][ligand_name]["inchi_key"] = inchi_key
			interacting_ligands[complex][ligand_name]["sequence"] = sequence
			interacting_ligands[complex][ligand_name]["chem_id"] = chem_id
			references = []
			for reference in result["refs"]:
				references.append(reference["pmid"])
			interacting_ligands[complex][ligand_name]["pmid"] = references
			synonyms = []
			for res in synonym_request_data:
				synonyms.append(res["name"].replace("<sup>"," ").replace("</sup>"," ").replace("<sub>"," "))
			interacting_ligands[complex][ligand_name]["synonyms"] = synonyms
	#interacting_ligands = ast.literal_eval(json.dumps(interacting_ligands))
	out_json = json.dumps(interacting_ligands)
	load_ligands(out_json)
def load_lig():
	ligand = {}
	### old ###
	list = ["amylin","adrenomedullin","intermedin","calcitonin gene-related peptide","vasoactive intestinal polypeptide","parathyroid hormone","tuberoinfundibular peptide"]
	ligand["amylin"] = {"name_short":"AMY","chem_id":"16132430","inchi_key":"PLOPBXQQPZYQFA-AXPWDRQUSA-N","sequence":"KCNTATCATQRLANFLVHSSNNFGAILSSTNVGSNTY","type":"Agonist"}
	ligand["adrenomedullin"] = {"name_short":"AM1","chem_id":"56841671","inchi_key":"ULCUCJFASIJEOE-NPECTJMMSA-N","sequence":"YRQSMNNFQGLRSFGCRFGTCTVQKLAHQIYQFTDKDKDNVAPRSKISPQGY","type":"Agonist"}
	ligand["calcitonin gene-related peptide alpha"] = {"name_short":"alpha-CGRP","chem_id":"44563440","inchi_key":"JMJJWZFCOWFIBU-XJVRLEFXSA-N","sequence":"ACDTATCVTHRLAGLLSRSGGVVKNNFVPTNVGSKAF","type":"Agonist"}
	ligand["vasoactive intestinal polypeptide"] = {"name_short":"VIP","chem_id":"16129679","inchi_key":"VBUWHHLIZKOSMS-UHFFFAOYSA-N","sequence":"HSDAVFTDNYTRLRKQMAVKKYLNSILN","type":"Agonist"}
	ligand["parathyroid hormone"] = {"name_short":"PTH","chem_id":"16129682","inchi_key":"OGBMKVWORPGQRR-UHFFFAOYSA-N","sequence":"SVSEXQLMHNLGKHLNSMERVEWLRKKLQDVHNF","type":"Agonist"}
	ligand["glucagon"] = {"name_short":"Glucagon","chem_id":"16132283","inchi_key":"MASNOZXLGMXCHN-ZLPAWPGGSA-N","sequence":"HSQGTFTSDYSKYLDSRRAQDFVQWLMNT","type":"Agonist"}

	### new ###
	ligand["calcitonin"] = {"name_short":"CT","chem_id":"16132288","inchi_key":"MKPOFZGVVSUXKS-JKQNMTHDSA-N","sequence":"CGNLSTCMLGTYTQDFNKFHTFPQTAIGVGAP","type":"Agonist"}
	ligand["oxyntomodulin"] = {"name_short":"Oxyntomodulin","chem_id":"121494088","inchi_key":"DDYAPMZTJAYBOF-ZMYDTDHYSA-N","sequence":"HSQGTFTSDYSKYLDSRRAQDFVQWLMNTKRNRNNIA","type":"Agonist"}
	ligand["calcitonin gene-related peptide beta"] = {"name_short":"beta-CGRP","chem_id":"N/A","inchi_key":"N/A","sequence":"ACNTATCVTHRLAGLLSRSGGMVKSNFVPTNVGSKAF","type":"Agonist"}
	ligand["pramlintide"] = {"name_short":"pramlintide","chem_id":"70691388","inchi_key":"TZIRZGBAFTZREM-MKAGXXMWSA-N","sequence":"KCNTATCATQRLANFLVHSSNNFGPILPPTNVGSNTY","type":"Agonist"}
	ligand["AC187"] = {"name_short":"AC187","chem_id":"16133792","inchi_key":"ZLFXHYNEZYAYPG-AABHONRUSA-N","sequence":"VLGKLSQELHKLQTYPRTNTGSNTY","type":"Antagonist"}
	ligand["adrenomedullin 2"] = {"name_short":"AM2","chem_id":"N/A","inchi_key":"N/A","sequence":"TQAQLLRVGCVLGTCQVQNLSHRLWQLMGPAGRQDSAPVDPSSPHSY","type":"Agonist"}
	ligand["olcegepant"] = {"name_short":"olcegepant","chem_id":"6918509","inchi_key":"ITIXDWVDFFXNEG-JHOUSYSJSA-N","sequence":"N/A","type":"Antagonist"}
	ligand["telcagepant"] = {"name_short":"telcagepant","chem_id":"11319053","inchi_key":"CGDZXLJGHVKVIE-DNVCBOLYSA-N","sequence":"N/A","type":"Antagonist"}
	ligand["erenumab"] = {"name_short":"erenumab","chem_id":"N/A","inchi_key":"N/A","sequence":"N/A","type":"Antagonist"}
	load_ligands(json.dumps(ligand))


def main():
	load_lig_api()

if __name__=="__main__":
	main()
