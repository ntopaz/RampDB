import os, sys, json
import pprint as pp
from core.views_load_ligands import load_ligands

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
	load_lig()

if __name__=="__main__":
	main()
