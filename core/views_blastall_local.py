import sys,os,json, re, tempfile, time
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
### LOCAL ###
BLAST_PATH = "/home/ntopaz3/rampdb/core/exec/"
HMMER_PATH = "/home/ntopaz3/rampdb/core/exec/"
CLUSTAL_PATH = "/home/ntopaz3/rampdb/core/exec/"
############
#BLAST_PATH = ""
#HMMER_PATH = ""
#CLUSTAL_PATH = ""
### SERVER ###
HOME_DIR= "/home/ntopaz3/"
#BLAST_PATH = "/projects/VirtualHost/rampdb/core/exec/blast/bin"
#HMMER_PATH = "/projects/VirtualHost/rampdb/core/exec/hmmer/src"
#CLUSTAL_PATH = "/projects/VirtualHost/rampdb/core/exec/clustal/bin"
##############
# Create your views here.
aa_list = ['D','S','Q','K','I','P','F','N','H','L','R','W','Y','M','V','E']
@transaction.atomic
def blast_all(query):
	print query
	result_dict = {}
	print HOME_DIR+"/"+"temp.txt"
	if not query.startswith(">"):
		result = {'error': 'Protein input query not in FASTA format'}
		return result
	if not "|" in query:
		new_query = ""
		count = 0 
		for item in query.split("\n"):
			if count == 0:
				new_query += item + " | ph \n"
			else:
				new_query += item
			count +=1
		query = new_query
	print query
	q = open(HOME_DIR+"/"+"query.txt","w")
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

	f = open(HOME_DIR+"/"+"temp.txt","w")
	f.write(my_fasta)
	f.close()
	query_is_prot = False
	q=open(HOME_DIR + "/" + "query.txt","r+")
	for record in SeqIO.parse(q,"fasta"):
		query_length = len(record.seq)
		query_seq = record.seq
		for letter in query_seq:
			if letter in aa_list:
				query_is_prot = True
		query_name = record.id
		query_desc = record.description
	if not query_is_prot:
		result = {'error': 'Input must be a protein sequence, not DNA'}
		return result
	result_dict['protein'] = {'name':query_name, 'seq':str(query_seq), 'length': query_length, 'desc':query_desc, 'match': None}
	q.close()
	result = check_output([BLAST_PATH+"makeblastdb","-dbtype","prot","-in",HOME_DIR+"/temp.txt","-out",HOME_DIR+"/"+"blastdb","-title","blastdb","-parse_seqids"], shell=False)
	os.remove(HOME_DIR+"/"+"temp.txt")

	blast_results = check_output([BLAST_PATH+"blastp","-db",HOME_DIR+"/"+"blastdb","-outfmt","6","-query",query,"-max_target_seqs","5"], shell=False)
	res_avg = 0.0
	current_ident = 0.0
	current_eval = 10.0
	current_match = ""
	fixed_lines = re.split("\n",blast_results.rstrip())
	for line in fixed_lines:
		query_name = line.split('\t')[0]
		match = line.split('\t')[1]
		identity = float(line.split('\t')[2])
		e_val = float(line.split('\t')[10])
		print match,identity,e_val
		if e_val <  current_eval:
			current_eval = e_val
			current_ident = identity
			current_match = match
	prot_obj = Protein.objects.filter(reference_id=current_match).select_related("family","source","organism")
	result = hmm_query(query,result_dict,query_name)
	return result

def hmm_query(query, result_dict,query_name):
        profile_score = {}
        profile_quer_seq = {}
        profile_ref_seq = {}
        my_profiles = ['Ramp 1','Ramp 2','Ramp 3','CLR','CT','vip1','pth1','pth2','glucagon','VPAC2']
        fp = tempfile.NamedTemporaryFile(suffix="",dir=HOME_DIR,delete = False)
        for profile in my_profiles:
                fp.seek(0)
                fp.truncate()
                check_output([HMMER_PATH+"hmmscan","-o",fp.name,
                BASE_DIR+"/"+"core/profiles/%s" % profile,query],shell=False)
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
                fp_quer = tempfile.NamedTemporaryFile(suffix="",dir=HOME_DIR, delete = False)
                fp_quer.write(">query\n"+profile_quer_seq[best_profile])
                fp_quer.seek(0)
                fp_subj = tempfile.NamedTemporaryFile(suffix="",dir=HOME_DIR, delete = False)
                fp_subj.write(">ref\n"+profile_ref_seq[best_profile])
                fp_subj.seek(0)
                results = check_output([BLAST_PATH+"blastp","-subject",fp_subj.name,"-outfmt","6","-query",fp_quer.name],shell=False)
                fp_quer.close()
                os.remove(fp_quer.name)
                fp_subj.close()
                os.remove(fp_subj.name)
                result = hmm_match(query,best_profile, profile_ref_seq[best_profile], profile_quer_seq[best_profile], max_value,results,result_dict,query_name)
        	return result
	else:
                return result_dict
        fp.close()
        os.remove(fp.name)

def hmm_match(query,family,subj_seq, quer_seq, confidence,blast_results,result_dict,query_name):
	my_line = re.split('\s+', blast_results)
	print subj_seq
	with open(HOME_DIR+"/hmm_match.txt","w") as h:
		h.write(">Closest_Match\n")
		h.write(subj_seq)
        blast_results_2 = check_output([BLAST_PATH+"blastp","-db",HOME_DIR+"/"+"blastdb","-outfmt","6","-query",h.name,"-max_target_seqs","1"], shell=False)
	print my_line
	os.system("rm " + HOME_DIR + "/hmm_match.txt")

	print "blast results of hmm match:",blast_results
	prot_obj = Protein.objects.filter(reference_id=blast_results_2.split('\t')[1]).select_related("family","source","organism")
        my_ident = round(float(blast_results.split('\t')[2]),1)
	result_dict['protein']['match'] = {}
	print prot_obj
	result_dict['protein']['match']['name'] = prot_obj[0].name
	result_dict['protein']['match']['id'] = blast_results.split('\t')[1]
	result_dict['protein']['match']['eval'] = blast_results.split('\t')[10]
	result_dict['protein']['match']['max_score'] = blast_results.split('\t')[11]
	result_dict['protein']['match']['ident'] = my_ident
	result_dict['protein']['match']['seq'] = quer_seq
	result_dict['protein']['match']['domain_seq'] = subj_seq
	result_dict['protein']['match']['family'] = prot_obj[0].family.name
	result_dict['protein']['match']['family_short'] = prot_obj[0].family.name_short
	result_dict['protein']['match']['int_status'] = prot_obj[0].family.status
	result_dict['protein']['match']['source'] = prot_obj[0].source.url
	result_dict['protein']['match']['organism'] = prot_obj[0].organism.name
	return result_dict

def ligand_search(ligand, t_threshold):
	result_dict = {}
	ligand_objects = Ligand.objects.all()
	result_dict['ligand'] = {'query_name':ligand, 'match': {}}
	found_result = False
	for lig_obj in ligand_objects:
		if ligand.lower() == lig_obj.name.lower():
			found_result = True
			if lig_obj.chem_id != '0':
				match_url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{}/JSON".format(lig_obj.chem_id)
				pc_results = urllib2.urlopen(match_url)
				pc_results = json.load(pc_results)
				for dummy in pc_results['PC_Compounds']:
					if dummy.has_key("props"):
						for item in dummy['props']:
							if item.has_key("urn"):
								if item['urn']['label'] == "Molecular Formula":
									molecular_formula = item['value']['sval']
								if item['urn']['label'] == "Molecular Weight":
									molecular_weight = item['value']['fval']
								if item['urn']['label'] == "InChIKey":
									inchi_key = item['value']['sval']
				result_dict['ligand']['match']['molecular_weight'] = molecular_weight
				result_dict['ligand']['match']['molecular_formula'] = molecular_formula
				result_dict['ligand']['match']['inchi_key'] = inchi_key
				result_dict['ligand']['match']['chem_id'] = lig_obj.chem_id

			else:
				result_dict['ligand']['match']['molecular_weight'] = "N/A"
				result_dict['ligand']['match']['molecular_formula'] = "N/A"
				result_dict['ligand']['match']['chem_id'] = "Not on PubChem"
				result_dict['ligand']['match']['inchi_key'] = lig_obj.inchi_key

			result_dict['ligand']['match']['name'] = lig_obj.name
			result_dict['ligand']['match']['gtp_id'] = lig_obj.gtp_id
			result_dict['ligand']['match']['sequence'] = lig_obj.sequence
			result_dict['ligand']['match']['lig_type'] = lig_obj.lig_type
			result_dict['ligand']['match']['type'] = lig_obj.lig_type
			return result_dict
	if not found_result:
		for lig_obj in ligand_objects:
			if ligand.lower() in lig_obj.name.lower():
				found_result = True
				if lig_obj.chem_id != '0':
					match_url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{}/JSON".format(lig_obj.chem_id)
					pc_results = urllib2.urlopen(match_url)
					pc_results = json.load(pc_results)
					for dummy in pc_results['PC_Compounds']:
						if dummy.has_key("props"):
							for item in dummy['props']:
								if item.has_key("urn"):
									if item['urn']['label'] == "Molecular Formula":
										molecular_formula = item['value']['sval']
									if item['urn']['label'] == "Molecular Weight":
										molecular_weight = item['value']['fval']
									if item['urn']['label'] == "InChIKey":
										inchi_key = item['value']['sval']
					result_dict['ligand']['match']['molecular_weight'] = molecular_weight
					result_dict['ligand']['match']['molecular_formula'] = molecular_formula
					result_dict['ligand']['match']['inchi_key'] = inchi_key
					result_dict['ligand']['match']['chem_id'] = lig_obj.chem_id

				else:
					result_dict['ligand']['match']['molecular_weight'] = "N/A"
					result_dict['ligand']['match']['molecular_formula'] = "N/A"
					result_dict['ligand']['match']['chem_id'] = "Not on PubChem"
					result_dict['ligand']['match']['inchi_key'] = lig_obj.inchi_key

				result_dict['ligand']['match']['name'] = lig_obj.name
				result_dict['ligand']['match']['gtp_id'] = lig_obj.gtp_id
				result_dict['ligand']['match']['sequence'] = lig_obj.sequence
				result_dict['ligand']['match']['lig_type'] = lig_obj.lig_type
				result_dict['ligand']['match']['type'] = lig_obj.lig_type
				return result_dict
	if not found_result:
		try:
			initial_url = "http://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{}/cids/TXT?name_type=word".format(ligand)
        		response = urllib2.urlopen(initial_url)
        		results = re.split("\n",response.read().rstrip())
        		capt_cid = "<CID>(.+)</CID>"
        		for line in results:
				url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastsimilarity_2d/cid/{}/cids/XML?Threshhold={}".format(line,t_threshold)
                		res = urllib2.urlopen(url)
                		hits = re.findall(capt_cid,res.read())
                		for item in hits:
		       			if Ligand.objects.filter(chem_id=item).exists():
							print "Found match",item
							match_url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{}/JSON".format(item)
							pc_results = urllib2.urlopen(match_url)
							pc_results = json.load(pc_results)
							lig_obj = Ligand.objects.get(chem_id=item)
							for dummy in pc_results['PC_Compounds']:
								if dummy.has_key("props"):
									for item in dummy['props']:
										if item.has_key("urn"):
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
				inchi_url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/inchikey/{}/cids/TXT?name_type=word".format(ligand)
				response = urllib2.urlopen(inchi_url)
                		results = re.split("\n",response.read().rstrip())
                		capt_cid = "<CID>(.+)</CID>"
                		for line in results:
					url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastsimilarity_2d/cid/{}/cids/XML?Threshhold={}".format(line,t_threshold)
	                		res = urllib2.urlopen(url)
                        		hits = re.findall(capt_cid,res.read())
                        		for item in hits:
                                		if Ligand.objects.filter(chem_id=item).exists():
								match_url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{}/JSON".format(item)
                                                		pc_results = urllib2.urlopen(match_url)
								pc_results = json.load(pc_results)
					        		lig_obj = Ligand.objects.get(chem_id=item)
                                                		for dummy in pc_results['PC_Compounds']:
                                                        		if dummy.has_key("props"):
                                                                		for item in dummy['props']:
                                                                        		if item.has_key("urn"):
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
		if not LoadingHandler.objects.filter(name="handler").exists():
			loading_obj = LoadingHandler(name="handler")
			loading_obj.save()
		else:
			loading_obj = LoadingHandler.objects.get(name="handler")
			while loading_obj.handler:
				time.sleep(7)
				loading_obj = LoadingHandler.objects.get(name="handler")
		data = request.data
		print data
		if not data:
			results = {'error': 'Please make a selection above'}
			response = JsonResponse(results)
			return response
		if not data.has_key('protein') and not data.has_key('ligand'):
			results = {'error': 'Please make a selection above'}
			response = JsonResponse(results)
			return response
		if data.has_key('protein') and data.has_key('ligand') and data['ligand'].strip() != '' and data['protein'] != '':
			results = {'error': 'Please submit either a protein sequence or ligand, not both'}
			response = JsonResponse(results)
			pp.pprint(results)
			return response
		elif data.has_key('protein') and data['protein'].strip() !='':
			loading_obj = LoadingHandler.objects.get(name="handler")
			loading_obj.handler = True
			loading_obj.save()
			try:
				results = blast_all(data['protein'])
				loading_obj.handler = False
				loading_obj.save()
			except:
				results = {'error':'No match found for that protein query'}
				loading_obj.handler = False
				loading_obj.save()
			print results

                        if 'error' in results.keys():
                                #results = {'error': 'Protein input query not in FASTA format'}
				pass
			elif results['protein']['match'] == None:
				results = {'error':'No match found for that protein query'}
			else:
				q_name = results['protein']['name']
				q_seq = results['protein']['match']['seq']
				s_name = results['protein']['match']['name']
				s_seq = results['protein']['match']['domain_seq']
				with open(HOME_DIR+"/"+"msa.fa","w") as f:
					f.write(">Domain\n")
					f.write(s_seq+"\n")
					f.write(">Query\n")
					f.write(q_seq+"\n")
				print CLUSTAL_PATH+"clustalo"
				msa = check_output([CLUSTAL_PATH+"clustalo","-i",HOME_DIR+"/msa.fa"])
				os.remove(HOME_DIR+"/"+"msa.fa")
				results['msa'] = msa
			os.system("rm -f "+HOME_DIR+"/"+ "blastdb*")
			os.system("rm -f "+HOME_DIR+"/"+ "tmp*")
		elif data.has_key('ligand'):
			print "ligand search"
			loading_obj = LoadingHandler.objects.get(name="handler")
			loading_obj.handler = True
			loading_obj.save()
			#try:
			results = ligand_search(data['ligand'], data['t_score'])
			print(results)
			if results == None:
				results = {'error':'No match found for that ligand query'}
			loading_obj.handler = False
			loading_obj.save()
			#except:
			#	results = {'error': 'No match found for that ligand query'}
			#	loading_obj.handler = False
			#	loading_obj.save()
		pp.pprint(results)
		response = JsonResponse(results)
		return response
