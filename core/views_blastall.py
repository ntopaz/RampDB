import sys,os,json, re, tempfile
import pprint as pp
import urllib2
from subprocess import *
from Bio import SeqIO
os.environ["DJANGO_SETTINGS_MODULE"] = "rampdb.settings"
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from django.shortcuts import render
from django.shortcuts import redirect
from django.db import transaction
from rest_framework.decorators import api_view
from django.http import JsonResponse
from models import *
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Create your views here.

@transaction.atomic
def blast_all(query):
	result_dict = {}
	if not query.startswith(">"):
		result = {'error': 'Protein input query not in FASTA format'}
		return result
	q = open("query.txt","w")
	q.write(query)
	query = q.name
	q.close()
	my_fasta = ""
	proteins = Protein.objects.all()
	for prot_obj in proteins:
		header = ">"+prot_obj.reference_id+" | "+prot_obj.name+"\n"
		seq = prot_obj.sequence
		my_fasta += header
		my_fasta += seq+"\n"

	f = open("temp.txt","w")
	f.write(my_fasta)
	f.close()
	q=open("query.txt","r+")
	for record in SeqIO.parse(q,"fasta"):
		query_length = len(record.seq)
		query_seq = record.seq
		query_name = record.id
		query_desc = record.description
	result_dict['protein'] = {'name':query_name, 'seq':str(query_seq), 'length': query_length, 'desc':query_desc, 'match': None}
	q.close()
	result = check_output(["makeblastdb","-dbtype","prot","-in","temp.txt","-out","blastdb","-title","blastdb","-parse_seqids"], shell=False)
	os.remove("temp.txt")

	blast_results = check_output(["blastp","-db","blastdb","-outfmt","6","-query",query,"-max_target_seqs","5"], shell=False)
	res_avg = 0.0
	current_ident = 0.0
	current_eval = 10.0
	current_match = ""
	if blast_results.strip() != "":
		fixed_lines = re.split("\n",blast_results.rstrip())
		for line in fixed_lines:
			query_name = line.split('\t')[0]
			match = line.split('\t')[1]
			identity = float(line.split('\t')[2])
			e_val = float(line.split('\t')[10])
			if e_val <  current_eval:
				current_eval = e_val
				current_ident = identity
				current_match = match
		prot_obj = Protein.objects.filter(reference_id=current_match).select_related("family","source","organism")
		result_dict['protein']['match'] = {}
		result_dict['protein']['match']['name'] = prot_obj[0].name
		result_dict['protein']['match']['id'] = current_match
		result_dict['protein']['match']['eval'] = current_eval
		result_dict['protein']['match']['ident'] = current_ident
		result_dict['protein']['match']['seq'] = prot_obj[0].sequence
		result_dict['protein']['match']['family'] = prot_obj[0].family.name
		result_dict['protein']['match']['family_short'] = prot_obj[0].family.name_short
		result_dict['protein']['match']['source'] = prot_obj[0].source.url
		result_dict['protein']['match']['organism'] = prot_obj[0].organism.name
		return result_dict
	else:
		result = hmm_query(query,result_dict,query_name)
		return result

def hmm_query(query, result_dict,query_name):
        profile_score = {}
        profile_quer_seq = {}
        profile_ref_seq = {}
        my_profiles = ['Ramp 1','Ramp 2','Ramp 3','CLR','CT']
        fp = tempfile.NamedTemporaryFile(suffix="",dir="",delete = False)
        for profile in my_profiles:
                fp.seek(0)
                fp.truncate()
                check_output(["hmmscan","-o",fp.name,
                "core/profiles/%s" % profile,query],shell=False)
                best_domain = 0
                best_domain_score = 0
                rows = fp.read()
                rows = re.split("\n",rows.rstrip())
                i=0
		skip = False
                for line in rows:
			if "No hits detected" in line:
				skip = True
                        col = re.split('\s*',rows[i].strip())
                        rows[i]=(col)
                        i+=1
                if len(rows[16]) > 1 and skip==False:
                        profile_score[profile] = float(rows[16][1])
                        do_continue = True
                        num_domains = int(rows[16][7])
                        for i in range(0,num_domains):
                                if float(rows[23+i][2]) > float(best_domain_score):
                                        best_domain = rows[23+i][0]
                                        best_domain_score = rows[23+i][2]
                        for i in range(len(rows)):
                                if rows[i][0] == "==" and rows[i][2] == best_domain:
                                        profile_ref_seq[profile] = rows[i+1][2]
                                        if rows[i+6][0] == rows[i+1][0]:
                                                profile_ref_seq[profile] += rows[i+6][2]
                                        profile_quer_seq[profile] = rows[i+3][2]
                                        if rows[i+8][0] == rows[i+3][0]:
                                                profile_quer_seq[profile] += rows[i+8][2]
                else:
                        profile_score[profile] = 0

        max_value = 0

        for key in profile_score:
                if (max_value < profile_score[key]):
                        max_value = profile_score[key]
                        best_profile = key

        if max_value > 0:
                fp_quer = tempfile.NamedTemporaryFile(suffix="",dir="", delete = False)
                fp_quer.write(">query\n"+profile_quer_seq[best_profile])
                fp_quer.seek(0)
                fp_subj = tempfile.NamedTemporaryFile(suffix="",dir="", delete = False)
                fp_subj.write(">ref\n"+profile_ref_seq[best_profile])
                fp_subj.seek(0)
                results = check_output(["blastp","-subject",
                fp_subj.name,"-outfmt","6","-query",fp_quer.name],shell=False)
                fp_quer.close()
                os.remove(fp_quer.name)
                fp_subj.close()
                os.remove(fp_subj.name)
                result = hmm_match(query,best_profile, profile_ref_seq[best_profile], max_value,results,result_dict,query_name)
        	return result
	else:
                return result_dict
        fp.close()
        os.remove(fp.name)

def hmm_match(query,family,subj_seq, confidence,blast_results,result_dict,query_name):
	my_line = re.split('\s+', blast_results)
	print subj_seq
	with open("hmm_match.txt","w") as h:
		h.write(">Closest_Match\n")
		h.write(subj_seq)
        blast_results = check_output(["blastp","-db","blastdb","-outfmt","6","-query",h.name,"-max_target_seqs","1"], shell=False)
	print my_line
	os.system("rm hmm_match.txt")

	print "blast results of hmm match:",blast_results
	prot_obj = Protein.objects.filter(reference_id=blast_results.split('\t')[1]).select_related("family","source","organism")
        my_ident = round(float(my_line[2]),1)
	result_dict['protein']['match'] = {}
	result_dict['protein']['match']['name'] = prot_obj[0].name
	result_dict['protein']['match']['id'] = blast_results.split('\t')[1]
	result_dict['protein']['match']['eval'] = my_line[10]
	result_dict['protein']['match']['ident'] = my_ident
	result_dict['protein']['match']['seq'] = prot_obj[0].sequence
	result_dict['protein']['match']['family'] = prot_obj[0].family.name
	result_dict['protein']['match']['family_short'] = prot_obj[0].family.name_short
	result_dict['protein']['match']['source'] = prot_obj[0].source.url
	result_dict['protein']['match']['organism'] = prot_obj[0].organism.name
	return result_dict

def ligand_search(ligand):
	result_dict = {}
	ligand_objects = Ligand.objects.all()
	result_dict['ligand'] = {'query_name':ligand, 'match': {}}
	for lig_obj in ligand_objects:
		if ligand.lower() == lig_obj.name.lower():
			match_url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/%s/JSON" % lig_obj.chem_id
                        pc_results = urllib2.urlopen(match_url)
			pc_results = json.load(pc_results)
			for dummy in pc_results['PC_Compounds']:
				if dummy.has_key("props"):
					for item in dummy['props']:
						if item.has_key("urn"):
							print item['urn']['label']
							if item['urn']['label'] == "Molecular Formula":
								molecular_formula = item['value']['sval']
							if item['urn']['label'] == "Molecular Weight":
								molecular_weight = item['value']['fval']
			result_dict['ligand']['match']['molecular_weight'] = molecular_weight
			result_dict['ligand']['match']['molecular_formula'] = molecular_formula
			result_dict['ligand']['match']['name'] = lig_obj.name
			result_dict['ligand']['match']['name_short'] = lig_obj.name_short
			result_dict['ligand']['match']['inchi_key'] = lig_obj.inchi_key
			result_dict['ligand']['match']['chem_id'] = lig_obj.chem_id
			#img_url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/%s/PNG?record_type=2d&image_size=large" % lig_obj.chem_id
			#img_results = urllib2.urlopen(img_url)
			#print type(img_results)
			#print img_results
			#result_dict['ligand']['match']['image'] = img_results
			return result_dict

	try:
		initial_url = "http://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/%s/cids/TXT?name_type=word" % ligand
        	response = urllib2.urlopen(initial_url)
		print response
        	results = re.split("\n",response.read().rstrip())
        	capt_cid = "<CID>(.+)</CID>"
        	for line in results:
                	res = urllib2.urlopen("http://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastsimilarity_2d/cid/%s/XML?Threshold=80" % line)
                	hits = re.findall(capt_cid,res.read())
                	for item in hits:
		       		if Ligand.objects.filter(chem_id=item).exists():
						match_url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/%s/JSON" % item
						pc_results = urllib2.urlopen(match_url)
						pc_results = json.load(pc_results)
						lig_obj = Ligand.objects.get(chem_id=item)
						for dummy in pc_results['PC_Compounds']:
							if dummy.has_key("props"):
								for item in dummy['props']:
									if item.has_key("urn"):
										print item['urn']['label']
										if item['urn']['label'] == "Molecular Formula":
											molecular_formula = item['value']['sval']
										if item['urn']['label'] == "Molecular Weight":
											molecular_weight = item['value']['fval']
						result_dict['ligand']['match']['molecular_weight'] = molecular_weight
						result_dict['ligand']['match']['molecular_formula'] = molecular_formula
						result_dict['ligand']['match']['name'] = lig_obj.name
						result_dict['ligand']['match']['name_short'] = lig_obj.name_short
						result_dict['ligand']['match']['inchi_key'] = lig_obj.inchi_key
						result_dict['ligand']['match']['chem_id'] = lig_obj.chem_id
						return result_dict
	except:
		try:
			inchi_url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/inchikey/%s/cids/TXT?name_type=word" % ligand
			response = urllib2.urlopen(inchi_url)
                	results = re.split("\n",response.read().rstrip())
                	capt_cid = "<CID>(.+)</CID>"
                	for line in results:
	                	res = urllib2.urlopen("http://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastsimilarity_2d/cid/%s/XML?Threshold=80" % line)
                        	hits = re.findall(capt_cid,res.read())
                        	for item in hits:
                                	if Ligand.objects.filter(chem_id=item).exists():
							match_url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/%s/JSON" % item
                                                	pc_results = urllib2.urlopen(match_url)
							pc_results = json.load(pc_results)
					        	lig_obj = Ligand.objects.get(chem_id=item)
                                                	for dummy in pc_results['PC_Compounds']:
                                                        	if dummy.has_key("props"):
                                                                	for item in dummy['props']:
                                                                        	if item.has_key("urn"):
                                                                                	print item['urn']['label']
                                                                                	if item['urn']['label'] == "Molecular Formula":
                                                                                        	molecular_formula = item['value']['sval']
                                                                                	if item['urn']['label'] == "Molecular Weight":
                                                                                        	molecular_weight = item['value']['fval']
							result_dict['ligand']['match']['molecular_weight'] = molecular_weight
							result_dict['ligand']['match']['molecular_formula'] = molecular_formula
                                                	result_dict['ligand']['match']['name'] = lig_obj.name
                                                	result_dict['ligand']['match']['name_short'] = lig_obj.name_short
                                                	result_dict['ligand']['match']['inchi_key'] = lig_obj.inchi_key
                                                	result_dict['ligand']['match']['chem_id'] = lig_obj.chem_id
                                                	return result_dict
		except:
			result = {'error' : 'No match found for that ligand query'}
			return result

@api_view(['POST'])
def get_result(request):
	if request.method == 'POST':
		data = request.data
		print data
		if data.has_key('protein') and data.has_key('ligand') and data['ligand'].strip() != '' and data['protein'] != '':
			results = {'error': 'Please submit either a protein sequence or ligand, not both'}
			response = JsonResponse(results)
			pp.pprint(results)
			return response
		elif data.has_key('protein') and data['protein'].strip() !='':
			results = blast_all(data['protein'])
			print results

                        if 'error' in results.keys():
                                results = {'error': 'Protein input query not in FASTA format'}
			elif results['protein']['match'] == None:
				results = {'error':'No match found for that protein query'}
			else:
				q_name = results['protein']['name']
				q_seq = results['protein']['seq']
				s_name = results['protein']['match']['name']
				s_seq = results['protein']['match']['seq']
				with open("msa.fa","w") as f:
					f.write(">Match\n")
					f.write(s_seq+"\n")
					f.write(">Query\n")
					f.write(q_seq+"\n")
				msa = check_output(['clustalo','-i','msa.fa'])
				os.remove("msa.fa")
				results['msa'] = msa
			os.system("rm blastdb*")
		elif data.has_key('ligand'):
			print "ligand search"
			results = ligand_search(data['ligand'])
		pp.pprint(results)
		response = JsonResponse(results)
		return response
