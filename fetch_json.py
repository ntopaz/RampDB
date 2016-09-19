from Bio import SeqIO, Entrez
import  re, os, sys, json
import pprint as pp
#from core.views_load_proteins import load_db
Entrez.email = "ntopaz@spsu.edu"
final_dict = {}
acc_str = '<TSeq_accver>(.+)</TSeq_accver>'
org_str = '\[(.+)\]'
xml_org_str = '<TSeq_orgname>(.+)</TSeq_orgname>'
seq_str = '<TSeq_sequence>(.+)</TSeq_sequence>'
desc_str = '<TSeq_defline>(.+)</TSeq_defline>'

families_to_search = ['receptor activity modifying protein 1','receptor activity modifying protein 2','receptor activity modifying protein 3',
			'receptor activity modifying protein 4','receptor activity modifying protein 5','calcitonin receptor','calcitonin receptor-like receptor',
			'vasoactive intestinal polypeptide receptor 1', 'parathyroid hormone receptor 1','parathyroid hormone receptor 2',
			'glucagon receptor']

validation_terms = {
			'receptor activity modifying protein 1':['ramp 1','RAMP 1','receptor activity modifying protein 1','receptor activity-modifying protein 1','receptor (calcitonin) activity modifying protein 1'],
			'receptor activity modifying protein 2':['ramp 2','RAMP 2','receptor activity modifying protein 2','receptor activity-modifying protein 2',
			'receptor (calcitonin) activity modifying protein 2','receptor (G protein-coupled)'],
			'receptor activity modifying protein 3':['ramp 3','RAMP 3','receptor activity modifying protein 3','receptor activity-modifying protein 3', 'receptor (calcitonin)','receptor (G protein-coupled)'],
			'receptor activity modifying protein 4':['ramp 4','RAMP 4','receptor activity modifying protein 4','receptor activity-modifying protein 4'],
			'receptor activity modifying protein 5':['ramp 5','RAMP 5','receptor activity modifying protein 5','receptor activity-modifying protein 5'],
			'calcitonin receptor':['CT receptor','calcitonin receptor'],
			'calcitonin receptor-like receptor':['calcitonin-like','calcitonin receptor-like','clr','calcitonin gene-related peptide'],
			'vasoactive intestinal polypeptide receptor 1':['VIP1','vasoactive intestinal polypeptide receptor 1'],
			'parathyroid hormone receptor 1': ['Parathyroid hormone receptor 1','parathyroid hormone receptor 1','PTH1R','PTHR1','Parathyroid hormone 1 receptor','parathyroid hormone 1 receptor'],
			'parathyroid hormone receptor 2': ['Parathyroid hormone receptor 2','parathyroid hormone receptor 2','PTH2R','PTHR2','Parathyroid hormone 2 receptor','parathyroid hormone 2 receptor'],
			'glucagon receptor': ['Glucagon Receptor','glucagon receptor'],
}

for entry in families_to_search:
	search_handle = Entrez.esearch(db="protein", retmax=10000,term=entry)
	results = Entrez.read(search_handle)
	ids = ""
	for record in results['IdList']:
		ids += record+","
	protein_list = []

	handle = Entrez.efetch(db="protein", id=ids, rettype="fasta")
	text = handle.read()
	proteins = {}
	for line in text.split('\n'):
		if line.startswith(">"):
			accen = None
			myadd = False
			for item in validation_terms[entry]:
				if item in line:
					myadd = True
			for key in validation_terms.keys():
				for item in validation_terms[key]:
					if key is not entry:
						if item in line:
							myadd = False
		 	if myadd == False:
				continue
			protein_entry = {'org':None,'desc':None,'seq':""}
			accen = line.split('|')[3]
			organism = re.search(org_str,line)
			if organism == None:
				org_handle = Entrez.efetch(db="protein",id=line.split('|')[1], rettype="fasta", retmode="xml")
				org_text = org_handle.read()
				org_search = re.search(xml_org_str,org_text)
				if org_search is not None:
					organism = org_search.group(1)
				else:
					continue
			else:
				organism = organism.group(1)
			proteins[accen] = protein_entry
			proteins[accen]['org'] = organism.strip()
			desc = line.split('|')[4].split('[')[0].replace('PREDICTED:',"").replace('LOW QUALITY PROTEIN:','')
			proteins[accen]['desc'] = desc.strip()
		elif line.strip():
			if not accen == None:
				if proteins.has_key(accen):
					proteins[accen]['seq'] += line


	final_dict[entry] = proteins

with open("output.json","w") as f:
	json.dump(final_dict,f)
#pp.pprint(final_dict)
#load_db(json.dumps(final_dict))



